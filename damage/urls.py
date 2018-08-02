from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # /damage/test/
    url(r'^test/$', views.Test.as_view(), name="test"),

    url(r'^damagetype_add/$', views.damagetype_add, name='damagetype_add'),

    # /damage/hometest/
    url(r'^hometest/$', views.HomeTest.as_view(), name="hometest"),

    # /damage/map/
    url(r'^map/$', views.Map.as_view(), name="map"),

    # /damage/damagetype/add/
    url(r'damagetype/add/$', views.DamageTypeCreate.as_view(), name="damagetype-add"),

    # /damage/damage/add/
    url(r'damage/add/$', views.DamageEntry.as_view(), name="damage-add"),

    # /damage/damage/list/
    url(r'damage/list/$', views.DamageList.as_view(), name="damage-list"),

    # /damage/damage/list/1
    url(r'damage/list/(?P<pk>[0-9]+)/$', views.DamageListEntry.as_view(), name="damage-by-id"),

    # /damage/damage/list/criteria/
    url(r'damage/list/criteria/$', views.DamageListCriteria.as_view(), name="damage-list-criteria"),

]
