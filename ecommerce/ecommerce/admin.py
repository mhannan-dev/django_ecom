from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'QCommerce Title'
    site_title = 'QCommerce subtitle'
    index_title = 'Welcome to My QCommerce Panel'

admin_site = CustomAdminSite(name='custom_admin')
