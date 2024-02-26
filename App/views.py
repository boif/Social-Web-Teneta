from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def news(request):
    return render(request, 'news.html')