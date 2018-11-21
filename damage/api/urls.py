from .views import DamageRudView, DamageCreateApiView

from django.conf.urls import url

urlpatterns = [

    url(r'^$', DamageCreateApiView.as_view(), name="api-create"),

    url(r'(?P<pk>[0-9]+)^$', DamageRudView.as_view(), name="damage-rud"),

]