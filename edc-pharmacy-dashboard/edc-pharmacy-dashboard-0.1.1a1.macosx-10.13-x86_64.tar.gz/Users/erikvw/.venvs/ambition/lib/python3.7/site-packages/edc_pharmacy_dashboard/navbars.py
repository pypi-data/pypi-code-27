from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar

no_url_namespace = True if settings.APP_NAME == 'edc_pharmacy_dashboard' else False

pharmacy_dashboard = Navbar(name='pharmacy_dashboard')


pharmacy_dashboard.append_item(
    NavbarItem(name='prescribe',
               title='prescribe',
               label='Prescribe',
               glyphicon='glyphicon-edit',
               no_url_namespace=no_url_namespace,
               url_name='edc_pharmacy_dashboard:prescribe_listboard_url'))

pharmacy_dashboard.append_item(
    NavbarItem(name='dispense',
               title='dispense',
               label='Dispense',
               glyphicon='glyphicon-share',
               no_url_namespace=no_url_namespace,
               url_name='edc_pharmacy_dashboard:dispense_listboard_url'))

pharmacy_dashboard.append_item(
    NavbarItem(name='pharmacy',
               fa_icon='fa-medkit',
               no_url_namespace=no_url_namespace,
               url_name='edc_pharmacy_dashboard:home_url'))


site_navbars.register(pharmacy_dashboard)
