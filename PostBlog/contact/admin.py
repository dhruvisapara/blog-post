from django.contrib import admin

from contact.models import Contact
from django.contrib.admin import AdminSite


class ContactAdminSite(AdminSite):
    site_header = "UMSRA Events Admin"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"


contact_admin_site = ContactAdminSite(name='contact_admin')

contact_admin_site.register(Contact)
