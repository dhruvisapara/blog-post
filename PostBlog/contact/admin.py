from django.contrib.admin import AdminSite

from contact.models import Contact, Measurement, DataSet


class ContactAdminSite(AdminSite):
    """

    """
    site_header = "UMSRA Events Admin"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"


contact_admin_site = ContactAdminSite(name='contact_admin')

contact_admin_site.register(Contact)

from django.contrib import admin


class MembershipInline(admin.TabularInline):
    model = Measurement.sets.through


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ['sets']
