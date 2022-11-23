import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV

# Чтобы каждый раз при запросе не читать csv файл, вынес его в переменную - список словарей. Файл небольшой 5 Мбайт.
all_bus_stations = []
with open(BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        all_bus_stations.append(row)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(all_bus_stations, 10)
    context = {'page': paginator.get_page(page_num)}
    return render(request, 'stations/index.html', context)
