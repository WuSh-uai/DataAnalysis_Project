from django.contrib import admin
from .models import Consumption


@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    """消费数据后台管理"""

    list_display = ['student_id', 'name', 'consumption_type', 'amount', 'consumption_time', 'location']
    list_filter = ['consumption_type', 'location', 'consumption_time']
    search_fields = ['student_id', 'name']
    list_per_page = 20
    date_hierarchy = 'consumption_time'

    fieldsets = (
        ('基本信息', {
            'fields': ('student_id', 'name')
        }),
        ('消费信息', {
            'fields': ('consumption_type', 'amount', 'consumption_time', 'location')
        }),
    )