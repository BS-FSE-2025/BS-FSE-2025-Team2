from django.shortcuts import render, redirect
from django.contrib.auth import logout
from locations.models import SportsFieldLocation
from .models import Event
from locations.models import Favorite# noqa 
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def favorites_list(request):
    if not request.user.is_authenticated:
        return render(request, 'pages/guest_message.html', {
            'message': 'you are guest'})
    favorites = request.user.favorite_sports_fields.all()
    return render(request, 'pages/favorites.html', {'favorites': favorites})


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'pages/home.html')


def main(request):
    return render(request, 'pages/main.html')


def About_us(request):
    return render(request, 'pages/about_us.html')


def popular_fields(request):
    # جلب الحقول بترتيب متوسط التقييم أو عدد الحجوزات
    fields = SportsFieldLocation.objects.order_by('-average_rating')[:10]
    return render(request, 'pages/popular_fields.html', {'fields': fields})


def upcoming_events(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'pages/upcoming_events.html', {'events': events})