from django.shortcuts import render
from .models import Region

def region_lists(request):
    regions = Region.objects.all()
    return render(request, 'hostinfos/region_lists.html', {'regions': regions})