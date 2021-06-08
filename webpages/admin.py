from django.contrib import admin
from .models import FaultDetail, Department, Station, Status
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter
from import_export.formats import base_formats
from import_export import resources

# Register your models here.


class FaultDetailResource(resources.ModelResource):
    class Meta:
        model = FaultDetail
        fields = ('id', 'station__name', 'department__dep_name', 'fault_no', 'fault_description',
                  'fault_date', 'current_status__status', 'rectification_date', 'remarks')
        export_order = ('id', 'station__name', 'department__dep_name',
                        'fault_no', 'fault_description', 'fault_date',
                        'current_status__status', 'rectification_date',
                        'remarks')


class FaultDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fault_no', 'station', 'department',
                    'fault_description', 'fault_date', 'current_status', 'rectification_date')

    search_fields = ('fault_no', 'station__name',
                     'current_status__status', 'fault_description',)

    list_filter = (
        ('station__name', DropdownFilter),
        ('department__dep_name', DropdownFilter),
        ('current_status__status', DropdownFilter)
    )

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    resource_class = FaultDetailResource


admin.site.register(FaultDetail, FaultDetailAdmin)
admin.site.register(Station)
admin.site.register(Status)
admin.site.register(Department)
