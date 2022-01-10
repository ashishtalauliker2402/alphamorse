from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from texttomorse import settings
from pydub import AudioSegment
import os;

# Create your views here.
@csrf_protect 
def main_show(request):
    return render(request, 'morse/index.html')

@csrf_protect 
def convert_to_morse(request):
    alphamorse = {
        "A" : ".-",
        "B" : "-...",
        "C" : "-.-.",
        "D" : "-..",
        "E" : ".",
        "F" : "..-.",
        "G" : "--.",
        "H" : "....",
        "I" : "..",
        "J" : ".---",
        "K" : "-.-",
        "L" : ".-..",
        "M" : "--",
        "N" : "-.",
        "O" : "---",
        "P" : ".--.",
        "Q" : "--.-",
        "R" : ".-.",
        "S" : "...",
        "T" : "-",
        "U" : "..-",
        "V" : "...-",
        "W" : ".--",
        "X" : "-..-",
        "Y" : "-.--",
        "Z" : "--.."
    }

    dotpath = "\\morse\\static\\dot.wav"
    dashpath = "\\morse\\static\\dash.wav"

    text = request.POST.get('words')
    text_array = text.split()
    sounds = []

    for word in text_array:
        for char in word:
            for morse in alphamorse[char.upper()]:
                if morse == ".":
                    sounds.append(AudioSegment.from_wav(settings.BASE_DIR + "\\morse\\static\\dot.wav"))
                elif morse == "-":
                    sounds.append(AudioSegment.from_wav(settings.BASE_DIR + "\\morse\\static\\dash.wav"))
                sounds.append(AudioSegment.silent(duration=100))
            sounds.append(AudioSegment.silent(duration=300))
        sounds.append(AudioSegment.silent(duration=700))

    playlist = AudioSegment.empty()

    for sound in sounds:
        playlist += sound

    playlist.export(settings.BASE_DIR + "\\morse\\static\\uploads\\output.wav", format="wav")

    return HttpResponse(request.POST.get('words'))
