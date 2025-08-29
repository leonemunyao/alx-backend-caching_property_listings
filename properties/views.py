from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse

@cache_page(60 * 15)
def property_list(request):
	properties = Property.objects.all()
	if request.headers.get('Accept') == 'application/json':
		return JsonResponse({'properties': list(properties.values())})
	return render(request, 'properties/property_list.html', {'properties': properties})
