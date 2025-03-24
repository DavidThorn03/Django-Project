from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Hotel
from .models import Client
from .models import Room


def index(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'holidays/index.html', context)

def hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    return render(request, 'holidays/hotel.html', {'hotel': hotel})

def profile(request, client_id):
    user = get_object_or_404(Client, pk=client_id)
    return render(request, 'holidays/profile.html', {'client': user})

def book(request, room_id, user_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'holidays/book.html', {'room': room, 'user_id': user_id})

def vote(request, room_id, user_id):
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))