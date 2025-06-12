from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Location
from .forms import QueryForm, AddUrlDataForm
import csv
import traceback
import requests

def import_data(request):
    try:
        with open(settings.IMPORT_PATH, 'r', newline='\n', encoding="UTF-8") as csvfile:
            Location.objects.all().delete()
            reader = csv.DictReader(csvfile)
            locations = []
            for row in reader:
                if row['CONDOMINIUM_EXPENSES'] != '':
                    locations.append(Location(city = row['CITY'], dept_code = row['DEPT_CODE'], zip_code = row['ZIP_CODE'], condominium_expenses = row['CONDOMINIUM_EXPENSES']))
            Location.objects.bulk_create(locations)
            return HttpResponse("Collection succesfully imported")
    except Exception:
        return HttpResponse('Something went wrong, it is likely the path to the import file is incorrect')
    
def overall_stats(request):
    try:
        locations_stats = get_locations_stats()
        return HttpResponse('10% quantile: {}€, Mean value: {}€, 90% quantile: {}€'.format(locations_stats[0], locations_stats[1], locations_stats[2]))
    except NoLocationException:
        return HttpResponse('No locations were found in database')
    
def query_stats(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                
                locations_stats = get_locations_stats(query_city= form_data['city'], query_dept_code= form_data['dept_code'], query_zip_code= form_data['zip_code'])
                HttpResponseRedirect('')
                return HttpResponse('10% quantile: {}€, Mean value: {}€, 90% quantile: {}€'.format(locations_stats[0], locations_stats[1], locations_stats[2]))
            except NoLocationException:
                 return HttpResponse('No locations were found in database')
    
    context= {}
    context['form'] = QueryForm()
    return render(request, "generic_form.html", context)

def add_url(request):
    if request.method == 'POST':
        form = AddUrlDataForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                url = form_data['url']
                id = url.split('/')[-1]
                response = requests.get(url='https://www.bienici.com/realEstateAd.json?id={}'.format(id))
                if response.status_code != 200:
                    return HttpResponse('No location found with this URL')
                response_content = response.json()
                if 'annualCondominiumFees' not in response_content:
                    return HttpResponse('No condominium fees found in with this URL')
                location = Location(city = response_content['city'], dept_code = response_content['departmentCode'], zip_code=response_content['postalCode'], condominium_expenses = response_content['annualCondominiumFees'])
                location.save()
                return HttpResponse('Location has been successfully added to database')
            except Exception:
                return HttpResponse('Something went wrong: {}'.format(traceback.format_exc()))

    context= {}
    context['form'] = AddUrlDataForm()
    return render(request, "generic_form.html", context)


class NoLocationException(Exception):
    pass

def get_locations_stats(query_city= '', query_dept_code = '', query_zip_code = ''):
    locations = Location.objects.all()
    if query_city != '':
        locations = locations.filter(city = query_city)
    if query_dept_code != '':
        locations = locations.filter(dept_code = query_dept_code)
    if query_zip_code != '':
        locations = locations.filter(zip_code = query_zip_code)
    total_locations = locations.count()
    if total_locations == 0:
        raise NoLocationException
    ordered_locations =locations.order_by('condominium_expenses')
    quantile_ten_percents = ordered_locations[total_locations // 10].condominium_expenses
    quantile_ninety_percents = ordered_locations[total_locations * 9 // 10].condominium_expenses
    total_condominium_expenses = 0
    for location in ordered_locations:
        total_condominium_expenses += location.condominium_expenses
    return quantile_ten_percents, round(total_condominium_expenses / total_locations, 2), quantile_ninety_percents