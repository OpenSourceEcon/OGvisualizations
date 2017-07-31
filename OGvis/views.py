from django.shortcuts import render
from django.http import HttpResponse
from surf3Dtime import main


def vis(request):
    context = {'div': main.div, 'js': main.js, 'cdn_js': main.cdn_js,
               'cdn_css': main.cdn_css}
    return render(request, 'OGvis/vis.html', context=context)
