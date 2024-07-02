from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VolunteeringEvent, Like, Donation
from .forms import DonationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# render the home page, no authentication or authoristation is needed for this page.  All other views required user to be logged in.


def home(request):
    return render(request, 'home.html')

# return all the events the logged in user has created / is the event organizer for.


class EventListView(LoginRequiredMixin, ListView):
    model = VolunteeringEvent
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        # Get the events created by the logged in user and order them by date and time.
        return VolunteeringEvent.objects.filter(organizer=self.request.user).order_by('date', 'time')

# return the details for a specific event the logged in user has created / is the event organizer for.


class EventDetailView(LoginRequiredMixin, DetailView):
    model = VolunteeringEvent
    template_name = 'event_detail.html'
    context_object_name = 'event'

    # Raise a 403 no permission error if the event was not created by the logged in user.
    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if self.request.user != event.organizer:
            return self.handle_no_permission()
        return event

# enable an event to be created by a logged in user.


class EventCreateView(LoginRequiredMixin, CreateView):
    model = VolunteeringEvent
    template_name = 'event_form.html'
    fields = ['title', 'description', 'date', 'time',
              'location', 'volunteers_needed', 'donation_goal']
    success_url = reverse_lazy('event_list')

# make sure the form is valid and add the logged in user id to the data.
    def form_valid(self, form):
        event_datetime = form.cleaned_data['date']

        if event_datetime < timezone.now().date():
            form.add_error('date', 'The event date cannot be in the past.')
            messages.error(
                self.request, 'The event date cannot be in the past.')
            return self.form_invalid(form)

        form.instance.organizer = self.request.user
        return super().form_valid(form)

# enable a specific event to be updated only by the user that created the event.


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = VolunteeringEvent
    template_name = 'event_form.html'
    fields = ['title', 'description', 'date', 'time',
              'location', 'volunteers_needed', 'donation_goal']
    success_url = reverse_lazy('event_list')

# if the event has not be created by the logged in user return a 403 error.
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# enable a specific event to be deleted only by the user that created the event.


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = VolunteeringEvent
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

# if the event has not be created by the logged in user return a 403 error.
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# show all the events the logged in user has volunteered for, not limted to the events the logged in user has created.


class MyVolunteeringEventsListView(LoginRequiredMixin, ListView):
    model = VolunteeringEvent
    template_name = 'my_volunteering_events.html'
    context_object_name = 'my_events'

# order data by date and time
    def get_queryset(self):
        my_events = self.request.user.volunteering_events.all()
        my_events = my_events.order_by('date', 'time')
        return my_events

# show all the volunteering events in the application, not limited to the events the logged in user has created or volunteered for.


class AllVolunteeringEventsListView(LoginRequiredMixin, ListView):
    model = VolunteeringEvent
    template_name = 'all_events.html'
    context_object_name = 'events'
    ordering = ['date', 'time']

# get the events the logged in user has liked, not limited to just the events they have created.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['liked_events'] = set(user.like_set.values_list(
            'event_id', flat=True)) if user.is_authenticated else set()
        return context

# show the details of a specific volunteering event, not limited to the events the logged in user has created or volunteered for.


class VolunteeringEventDetailView(LoginRequiredMixin, DetailView):
    model = VolunteeringEvent
    template_name = 'volunteering_event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['donation_form'] = DonationForm()
        return context

# method for logged in user to volunteer for an event. Redirect back to the current page.


@login_required
def add_volunteer(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    if not request.user in event.volunteers.all():
        event.volunteers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# method for logged in user to withdraw as a volunteer for an event they previously volunteered for. Redirect back to the current page.


@login_required
def withdraw_volunteer(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    if request.user in event.volunteers.all():
        event.volunteers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# method for logged in user to like an event. Redirect back to the current page.


@login_required
def like_event(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    Like.objects.get_or_create(user=request.user, event=event)
    return redirect(request.META.get('HTTP_REFERER', '/'))

# method for logged in user to unlike an event they previously liked. Redirect back to the current page.


@login_required
def unlike_event(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    Like.objects.filter(user=request.user, event=event).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# method for logged in user to donate money to an event. Redirect back to the current page.


@login_required
def add_donation(request, event_id):
    event = get_object_or_404(VolunteeringEvent, id=event_id)
    form = DonationForm(request.POST)
    if form.is_valid():
        Donation(user=request.user, event=event,
                 amount=form.cleaned_data["amount"]).save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# signup to use the application. Successful sign up will redirect to the list of all volunteering events.


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/all-events')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
