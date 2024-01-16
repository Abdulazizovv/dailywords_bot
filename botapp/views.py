from django.shortcuts import render
from .models import Words
from wrapper import read_words


def add_word_to_database():
    words = read_words()
    for word in words:
        Words.objects.create(uzbek=word['uzbek'], english=word['english'])

    return True

def index(request):
    random_word = Words.objects.order_by('?').first()
    return render(request, 'index.html', {'word': random_word})