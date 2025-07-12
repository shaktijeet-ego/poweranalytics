from django.contrib import admin
from .models import Region, Province, Branch , Outlet, Host, PowerInfo
from django.http import HttpResponse
import csv


@admin.action(description='Export selected to CSV')
def export_to_csv(modeladmin, request, queryset):
    # Create the HttpResponse with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=branches.csv'

    writer = csv.writer(response)
    # Write header
    writer.writerow(['Branch ID', 'Branch Name', 'Region'])

    # Write data rows
    for branch in queryset:
        writer.writerow([branch.branch_id, branch.branch_name, branch.region.region_name])

    return response


class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_id', 'branch_name', 'region')  # Show these columns in admin list view
    actions = [export_to_csv]  # Add CSV export action

class OutletAdmin(admin.ModelAdmin):
    list_display = ('outlet_id', 'outlet_name', 'branch','get_region')  # Show these columns in admin list view
    actions = [export_to_csv]  # Add CSV export action
    def get_region(self, obj):
        return obj.branch.region.region_name
    get_region.short_description = 'Region'


class HostAdmin(admin.ModelAdmin):
    list_display = ('host_id', 'host_name', 'host_type','outlet', 'get_branch', 'get_region')
    actions = [export_to_csv]

    def get_branch(self, obj):
        return obj.outlet.branch.branch_name
    get_branch.short_description = 'Branch'

    def get_region(self, obj):
        return obj.outlet.branch.region.region_name
    get_region.short_description = 'Region'

class PowerAdmin(admin.ModelAdmin):
    list_display = (
        'power_id',
        'get_host_name',
        'get_host_type',
        'get_outlet',
        'get_branch',
        'get_region',
        'no_of_batteries',
        'damaged_batteries',
        'last_installed',
        'backup_duration',
        'solar_available',
        'generator_available',
        'last_maintainance_date',
        'ups_status',
        'batteries_changed',
        'no_of_batteries_changed',
        'changed_date',
    )
    actions = [export_to_csv]

    def get_host_name(self, obj):
        return obj.host.host_name
    get_host_name.short_description = 'Host Name'

    def get_host_type(self, obj):
        return obj.host.host_type
    get_host_type.short_description = 'Host Type'

    def get_outlet(self, obj):
        return obj.host.outlet.outlet_name
    get_outlet.short_description = 'Outlet'

    def get_branch(self, obj):
        return obj.host.outlet.branch.branch_name
    get_branch.short_description = 'Branch'

    def get_region(self, obj):
        return obj.host.outlet.branch.region.region_name
    get_region.short_description = 'Region'

admin.site.register(Branch, BranchAdmin)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Outlet,OutletAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(PowerInfo, PowerAdmin)


