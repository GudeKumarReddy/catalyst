from django.contrib import admin

from data_management.models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_code', 'name', 'domain', 'year_founded', 'industry', 'current_employee_estimate', 'total_employee_estimate']


admin.site.register(Company, CompanyAdmin)