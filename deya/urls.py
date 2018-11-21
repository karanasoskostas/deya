from django.conf.urls import include, url
from django.contrib import admin
from damage import views
from django.urls import path
from .router import router

urlpatterns = [

    url(r'^$', views.FrontPageView.as_view(), name='frontpage'),

    url(r'^admin/', admin.site.urls),
    url(r'^damage/', include('damage.urls')),

    url(r'^frontpage/', views.FrontPageView.as_view(), name='frontpage'),
    url(r'^contact/', views.ContactDetailsView.as_view(), name='contact'),


    url(r'^deyausers/$', views.IndexDeyaView.as_view(), name='index-deya'),


    url('accounts/', include('django.contrib.auth.urls')),


    #  api
    url(r'^api/damage/', include(('damage.api.urls', 'damage'), namespace='api-damage')),


    # εναλλακτικά για api
    path('api/', include(router.urls))



]
