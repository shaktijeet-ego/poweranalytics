from django.contrib import admin
from .models import Region, Province, Branch #Outlet
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

admin.site.register(Branch, BranchAdmin)
admin.site.register(Region)
admin.site.register(Province)
#admin.site.register(Branch)
#admin.site.register(Outlet)
#admin.site.register(Host)


