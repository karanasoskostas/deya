
from django.conf.urls import include, url
from django.contrib import admin
from damage import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^damage/', include('damage.urls')),
    url(r'^frontpage/', views.FrontPageView.as_view(), name='frontpage'),
]
