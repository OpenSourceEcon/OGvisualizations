from django.shortcuts import render
from django.http import HttpResponse
from surf3Dtime import main as main_surf3Dtime
#from taxrates import main as main_taxrates
from bubbleplot import main as main_bubbleplot
from increase_decrease import main as main_increase
from lockdown.decorators import lockdown

from django.contrib.auth import authenticate
import base64


def vis(request):
    context = {'div': main_surf3Dtime.div, 'js': main_surf3Dtime.js,
               'cdn_js': main_surf3Dtime.cdn_js,
               'cdn_css': main_surf3Dtime.cdn_css}
    return render(request, 'OGvis/vis.html', context=context)


def bubble(request):
    context = {'div': main_bubbleplot.div, 'js': main_bubbleplot.js,
               'cdn_js': main_bubbleplot.cdn_js,
               'cdn_css': main_bubbleplot.cdn_css}
    return render(request, 'OGvis/bubbleplot.html', context=context)


def increase(request):
    context = {'div': main_increase.div, 'js': main_increase.js,
               'cdn_js': main_increase.cdn_js,
               'cdn_css': main_increase.cdn_css,
               'widget_js': main_increase.widget_js,
               'widget_css': main_increase.widget_css}
    return render(request, 'OGvis/increase-decrease.html', context=context)


@lockdown()
def tax(request):
    request.session.set_expiry(1)
    # context = {'div': main_taxrates.div, 'js': main_taxrates.js,
    #            'cdn_js': main_taxrates.cdn_js,
    #            'cdn_css': main_taxrates.cdn_css}
    return render(request, 'OGvis/simple_taxrates.html')
