from django.contrib import admin
from .models import Bird

@admin.register(Bird)

class BirdAdmin(admin.ModelAdmin):

    list_display = (
        'common_name',
        'scientific_name',
        'category',
        'migratory_status'
    )

    search_fields = (
        'common_name',
        'scientific_name'
    )

    list_filter = (
        'category',
        'migratory_status'
    )