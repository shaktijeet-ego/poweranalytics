from .forms import HostForm
from django.shortcuts import render,get_object_or_404, redirect
from .models import Region,Branch,Outlet,Host
from django.db.models import Count
from django.http import JsonResponse


def region_lists(request):
    regions = Region.objects.all()
    return render(request, 'hostinfos/region_lists.html', {'regions': regions})

def home_view(request):
    # Dashboard summary counts
    region_count = Region.objects.count()
    branch_count = Branch.objects.count()
    outlet_count = Outlet.objects.count()
    host_count = Host.objects.count()

    # Get OLT count per region
    region_olt_data = (
        Region.objects
        .annotate(olt_count=Count('branch__outlet__host'))
        .order_by('-olt_count')  # Sort by OLT count descending
        .values_list('region_name', 'olt_count')
    )

    # Convert to 2 separate lists for Chart.js
    labels = [row[0] for row in region_olt_data]
    data = [row[1] for row in region_olt_data]

    context = {
        'region_count': region_count,
        'branch_count': branch_count,
        'outlet_count': outlet_count,
        'host_count': host_count,
        'labels': labels,
        'data': data,
    }
    return render(request, 'hostinfos/home.html', context)



from django.core.paginator import Paginator
from django.db.models import Q

def host_list_view(request):
    search_query = request.GET.get('search', '')
    selected_region = request.GET.get('region', '')
    selected_branch = request.GET.get('branch', '')
    selected_outlet = request.GET.get('outlet', '')

    hosts = Host.objects.filter(is_deleted=False).select_related('outlet__branch__region')


    # Filter by search text
    if search_query:
        hosts = hosts.filter(
            Q(host_name__icontains=search_query) |
            Q(outlet__outlet_name__icontains=search_query) |
            Q(outlet__branch__branch_name__icontains=search_query) |
            Q(outlet__branch__region__region_name__icontains=search_query)
        )

    # Filter by Region
    if selected_region:
        hosts = hosts.filter(outlet__branch__region__region_id=selected_region)

    # Filter by Branch
    if selected_branch:
        hosts = hosts.filter(outlet__branch__branch_id=selected_branch)

    # Filter by Outlet
    if selected_outlet:
        hosts = hosts.filter(outlet__outlet_id=selected_outlet)

    # Pagination
    paginator = Paginator(hosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all Regions, Branches, and Outlets for dropdowns
    regions = Region.objects.all()
    branches = Branch.objects.all()
    outlets = Outlet.objects.all()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'regions': regions,
        'branches': branches,
        'outlets': outlets,
        'selected_region': selected_region,
        'selected_branch': selected_branch,
        'selected_outlet': selected_outlet,
    }
    return render(request, 'hostinfos/host_list.html', context)



from django.http import JsonResponse
from django.template.loader import render_to_string

def ajax_host_list(request):
    search_query = request.GET.get('search', '')

    hosts = Host.objects.filter(is_deleted=False).select_related('outlet__branch__region')


    if search_query:
        hosts = hosts.filter(
            Q(host_name__icontains=search_query) |
            Q(outlet__outlet_name__icontains=search_query) |
            Q(outlet__branch__branch_name__icontains=search_query) |
            Q(outlet__branch__region__region_name__icontains=search_query)
        )

    # For live search, no pagination (or you can add later)
    html = render_to_string('hostinfos/host_table_rows.html', {'hosts': hosts})

    return JsonResponse({'html': html})


def host_edit_view(request, host_id):
    host = get_object_or_404(Host, pk=host_id)

    if request.method == 'POST':
        form = HostForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return redirect('host_list')
    else:
        form = HostForm(instance=host)

    return render(request, 'hostinfos/host_edit.html', {'form': form, 'host': host})


def host_delete_view(request, host_id):
    host = get_object_or_404(Host, pk=host_id)

    if request.method == 'POST':
        host.is_deleted = True
        host.save()
        return redirect('host_list')

    return render(request, 'hostinfos/host_confirm_delete.html', {'host': host})


def deleted_hosts_view(request):
    deleted_hosts = Host.objects.filter(is_deleted=True).select_related('outlet__branch__region')
    return render(request, 'hostinfos/deleted_hosts.html', {'deleted_hosts': deleted_hosts})

def recover_host_view(request, host_id):
    host = get_object_or_404(Host, pk=host_id, is_deleted=True)

    if request.method == 'POST':
        host.is_deleted = False
        host.save()
        return redirect('host_list')

    return render(request, 'hostinfos/host_confirm_recover.html', {'host': host})
