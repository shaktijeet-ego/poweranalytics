from django.contrib import admin
from .models import Region, Province, Branch , Outlet, Host
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
    list_display = ('host_id', 'host_name', 'outlet', 'get_branch', 'get_region')
    actions = [export_to_csv]

    def get_branch(self, obj):
        return obj.outlet.branch.branch_name
    get_branch.short_description = 'Branch'

    def get_region(self, obj):
        return obj.outlet.branch.region.region_name
    get_region.short_description = 'Region'

admin.site.register(Branch, BranchAdmin)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(Outlet,OutletAdmin)
admin.site.register(Host,HostAdmin)


