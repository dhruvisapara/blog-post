from django.http import Http404
from django.shortcuts import render, redirect
from channels.generic.websocket import AsyncWebsocketConsumer

def index(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        char_choice = request.POST.get("character_choice")
        return redirect(
            '/game/play/%s?&choice=%s'
            % (room_code, char_choice)
        )
    return render(request, "game/index.html", {})


def game(request, room_code):
    choice = request.GET.get("choice")
    if choice not in ['X', 'O']:
        raise Http404("Choice does not exists")
    context = {
        "char_choice": choice,
        "room_code": room_code
    }
    return render(request, "game/game.html", context)
