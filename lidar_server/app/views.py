from django.shortcuts import render
from django.template import loader
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse

from django.conf import settings
import os
from os import system
import glob

def index(request):
    return render(request, 'index.html')

def run_script(request):
    path = settings.BASE_DIR / '3rdparty'
    system(f"python {path / 'lidar.py'}")
    png_files = glob.glob(f"{settings.BASE_DIR / 'media' / 'png'}/*")
    latest_png = max(png_files, key=os.path.getctime).split('\\')[-1]

    svg_files = glob.glob(f"{settings.BASE_DIR / 'media' / 'svg'}/*")
    latest_svg = max(svg_files, key=os.path.getctime).split('\\')[-1]
    # return JsonResponse({"path": f"/media/image.png"})
    return JsonResponse({
        "path": f'/media/png/{latest_png}',
        "svg_path": f'/media/svg/{latest_svg}',
    })
