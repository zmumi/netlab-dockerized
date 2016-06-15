from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'/run', views.run, name='run'),
    url(r'/stop', views.stop, name='stop'),
    url(r'/get_project', views.get_project, name='get_project'),
    url(r'/get_design', views.get_design, name='get_design'),
    url(r'/set_design', views.set_design, name='set_design'),
    url(r'/reset_design', views.reset_design, name='reset_design'),
    url(r'/sample_design', views.sample_design, name='sample_design'),
    url(r'/generate', views.generate, name='generate'),
    url(r'^', views.index, name='index'),
]