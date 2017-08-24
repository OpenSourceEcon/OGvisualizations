from django.shortcuts import render
from django.http import HttpResponse
from surf3Dtime import main as main_surf3Dtime
from taxrates import main as main_taxrates


def vis(request):
    context = {'div': main_surf3Dtime.div, 'js': main_surf3Dtime.js,
               'cdn_js': main_surf3Dtime.cdn_js,
               'cdn_css': main_surf3Dtime.cdn_css}
    return render(request, 'OGvis/vis.html', context=context)


def tax(request):
    context = {'div': main_taxrates.div, 'js': main_taxrates.js,
               'cdn_js': main_taxrates.cdn_js,
               'cdn_css': main_taxrates.cdn_css}
    return render(request, 'OGvis/taxrates.html', context=context)
