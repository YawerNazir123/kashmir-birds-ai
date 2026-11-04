from django.contrib import admin
from .models import Bird, ContactMessage

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


@admin.register(ContactMessage)

class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'subject',
        'created_at'
    )

    search_fields = (
        'name',
        'email',
        'subject'
    )

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )