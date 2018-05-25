import random
import string
import logging
import json
import requests
import urllib.parse
import os
import zipfile
import shutil
from io import StringIO
from io import BytesIO
from bs4 import BeautifulSoup
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

log = logging.getLogger(__name__)

def download_files(request):
    # log.debug(request.POST)
    if request.method != 'POST' or 'url[]' not in request.POST:
        return HttpResponse('Invalid request.', content_type="text/plain", status=400)

    urls = request.POST.getlist('url[]')

    log.debug(urls)

    in_memory_file = BytesIO()

    with zipfile.ZipFile(in_memory_file, 'w') as myzip:
        for url in urls:
            r = requests.get(url)
            name = url.split('/')[-1]

            myzip.writestr(name, r.content)

    response = HttpResponse(in_memory_file.getvalue(), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    return response

def home(request):
    """
    Home, sweet home.
    """
    if request.method == 'POST' and 'url' in request.POST:
        url = request.POST['url']
        try:
            urls = get_images(url)
        except InvalidUrlError:
            return HttpResponse('Invalid url.', content_type="text/plain", status=400)
        return JsonResponse({'urls': urls})
    return render(request, 'imagedownloader/home.html')

def get_images(url_in):
    page = get_content(url_in)
    soup = BeautifulSoup(page['content'])

    url = page['url']

    images = []
    for img in soup.select('img[src]'):
        if not img['src'].startswith('http'):
            src = urllib.parse.urljoin(url, img['src'])
        else:
            src = img['src']
        images.append(src)

    return images

def get_content(url):
    if url.startswith('http'):
        page = get_page(url)
        return page
    try:
        page = get_page('https://{}'.format(url))
        return page
    except requests.exceptions.RequestException:
        pass
    try:
        page = get_page('http:/{}'.format(url))
        return page
    except requests.exceptions.RequestException:
        pass
    raise InvalidUrlError()

def get_page(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise InvalidUrlError()

    return {'content': r.content, 'url': r.url}


class InvalidUrlError(ValueError): pass