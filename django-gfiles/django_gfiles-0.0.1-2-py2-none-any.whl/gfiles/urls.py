from django.conf.urls import url
from gfiles import views
# from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


from django.urls import reverse_lazy
from django.contrib.auth.views import(
    LoginView,
    LogoutView
)




urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', LoginView.as_view(
        template_name='gfiles/login.html',
        success_url='/',
        redirect_authenticated_user=True
    ), name='login'),
    url(r'^logout/$', LogoutView.as_view(
        next_page=reverse_lazy('login'),
    ), name='logout'),
    url(r'^register/$', CreateView.as_view(
        template_name='gfiles/register.html',
        form_class=UserCreationForm,
        success_url='/'
    ), name='register'),
    url(r'^upload_gfile/$', views.GFileCreateView.as_view(), name='upload_gfile'),
    url(r'^gfile_summary/$', views.GFileListView.as_view(), name='gfile_summary'),
    url(r'^update/$', views.status_update, name='status_update'),
    url(r'^success/$', views.success, name='success'),
]

