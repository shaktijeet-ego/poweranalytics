from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import HostForm,PowerInfoForm
from .models import Region, Branch, Outlet, Host, PowerInfo
from datetime import date, timedelta


def region_lists(request):
    regions = Region.objects.all()
    return render(request, 'hostinfos/region_lists.html', {'regions': regions})


from datetime import date, timedelta

def home_view(request):
    region_count = Region.objects.exclude(region_name__in=["Unknown", "Test"]).count()
    branch_count = Branch.objects.exclude(branch_name="NA").count()
    outlet_count = Outlet.objects.exclude(outlet_name="NA").count()
    host_count = Host.objects.filter(host_type='OLT').count()

    # Chart data
    region_olt_data = (
        Region.objects
        .annotate(olt_count=Count('branch__outlet__host'))
        .order_by('-olt_count')
        .values_list('region_name', 'olt_count')
    )
    labels = [row[0] for row in region_olt_data]
    data = [row[1] for row in region_olt_data]

    # Battery backup duration groups
    duration_filters = [
        ('≤ 30 minutes', timedelta(minutes=30)),
        ('≤ 1 hour', timedelta(hours=1)),
        ('≤ 1 hour 30 minutes', timedelta(hours=1, minutes=30)),
        ('≤ 2 hours', timedelta(hours=2)),
    ]
    duration_groups = []
    for label, max_duration in duration_filters:
        powers = PowerInfo.objects.filter(backup_duration__lte=max_duration).select_related('host')
        duration_groups.append({'label': label, 'powers': powers})

    # Battery last installed age groups (non-overlapping)
    today = date.today()
    year_filters = [
        ('> 3 years', timedelta(days=365*3)),
        ('> 2 years', timedelta(days=365*2)),
        ('> 1 year', timedelta(days=365)),
    ]
    already_included = set()
    last_installed_groups = []

    for label, min_age in year_filters:
        cutoff_date = today - min_age
        powers = (
            PowerInfo.objects
            .filter(last_installed__lte=cutoff_date)
            .exclude(pk__in=already_included)
            .select_related('host')
        )
        powers_with_age = []
        for p in powers:
            age_years = (today - p.last_installed).days // 365 if p.last_installed else None
            powers_with_age.append({
                'host': p.host,
                'last_installed': p.last_installed,
                'age_years': age_years,
            })
            already_included.add(p.pk)
        last_installed_groups.append({'label': label, 'powers': powers_with_age})

    context = {
        'region_count': region_count,
        'branch_count': branch_count,
        'outlet_count': outlet_count,
        'host_count': host_count,
        'labels': labels,
        'data': data,
        'duration_groups': duration_groups,
        'last_installed_groups': last_installed_groups,
    }

    return render(request, 'hostinfos/home.html', context)


def host_list_view(request):
    search_query = request.GET.get('search', '')
    # Convert to int or None to avoid filtering errors
    try:
        selected_region = int(request.GET.get('region', '') or 0)
    except ValueError:
        selected_region = 0
    try:
        selected_branch = int(request.GET.get('branch', '') or 0)
    except ValueError:
        selected_branch = 0
    try:
        selected_outlet = int(request.GET.get('outlet', '') or 0)
    except ValueError:
        selected_outlet = 0

    hosts = Host.objects.filter(is_deleted=False).select_related('outlet__branch__region')

    if search_query:
        hosts = hosts.filter(
            Q(host_name__icontains=search_query) |
            Q(outlet__outlet_name__icontains=search_query) |
            Q(outlet__branch__branch_name__icontains=search_query) |
            Q(outlet__branch__region__region_name__icontains=search_query)
        )

    if selected_region:
        hosts = hosts.filter(outlet__branch__region__region_id=selected_region)

    if selected_branch:
        hosts = hosts.filter(outlet__branch__branch_id=selected_branch)

    if selected_outlet:
        hosts = hosts.filter(outlet__outlet_id=selected_outlet)

    paginator = Paginator(hosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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



