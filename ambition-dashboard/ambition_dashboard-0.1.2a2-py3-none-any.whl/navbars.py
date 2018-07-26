from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'ambition_dashboard' else False

ambition_dashboard = Navbar(name='ambition_dashboard')

ambition_dashboard.append_item(
    NavbarItem(
        name='screened_subject',
        title='Screening',
        label='screening',
        fa_icon='fas fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES['screening_listboard_url'],
        no_url_namespace=no_url_namespace))

ambition_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Subjects',
        label='subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES['subject_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(ambition_dashboard)
