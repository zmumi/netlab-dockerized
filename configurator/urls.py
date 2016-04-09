from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'/generate', views.generate, name='generate'),
    url(r'^', views.index, name='index'),
]