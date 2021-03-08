from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    response = render(request,'index.html')
    try:
        coop = request.GET['coop']

        if (coop == 'True'):
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
            response['Cross-Origin-Embedder-Policy'] = 'require-corp'
    except:
        pass
    return response

def hit_miss(request):
    response = render(request,'hit_miss.html')
    try:
        coop = request.GET['coop']

        if (coop == 'True'):
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
            response['Cross-Origin-Embedder-Policy'] = 'require-corp'
    except:
        pass
    return response

def distribution(request):
    response = render(request,'distribution.html')
    try:
        coop = request.GET['coop']

        if (coop == 'True'):
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
            response['Cross-Origin-Embedder-Policy'] = 'require-corp'
    except:
        pass
    return response

def rdtsc(request):
    response = render(request,'rdtsc.html')
    try:
        coop = request.GET['coop']

        if (coop == 'True'):
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
            response['Cross-Origin-Embedder-Policy'] = 'require-corp'
    except:
        pass
    return response
