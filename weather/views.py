from django.shortcuts import render,redirect
import requests
import json
from .models import City 
from .forms import CityForm 
from django.http import JsonResponse,HttpResponse
from django.forms.models import model_to_dict   
# Create your views here.

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=baadfadef1d79048676ca9e548451944'
    
    
    error_message=''
    message=''
    message_class=''
    if request.method=='POST':
        print(request.POST)
        form=CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            city_count=City.objects.filter(name=new_city).count()
            
            r=requests.get(url.format(new_city)).json()
            if r['cod']==200:
                r=requests.get(url.format(new_city)).json()

                city_weather={
                    'city_count':city_count,
                    'city':new_city,
                    'temperature':r['main']['temp'],
                    'description':r['weather'][0]['description'],
                    'icon':r['weather'][0]['icon'],
                    }
                    
                if city_count==0:
                    form.save()
                data={
                        'weather_report':city_weather
                    }

                return JsonResponse(data)  
            
            else:
                error_message='City already exists in database'
    
        
    form=CityForm()

    context={'form':form}
    

    return render(request,'weather/weather.html',context)


def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

