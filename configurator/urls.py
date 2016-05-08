from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'/run', views.run, name='run'),
    url(r'/get_design', views.get_design, name='get_design'),
    url(r'/generate', views.generate, name='generate'),
    url(r'^', views.index, name='index'),
]