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
    url(r'damage/add/$', views.damage_entry_view.as_view(), name="damage-add"),

    # /damage/damage/list/15_08_2018/15_08_2018/1   το .* παιζει οταν θελω η παραμετρος να ειναι None
    url(r'damage/list_dates/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pdamagestatus>.*)/(?P<pdamagetype>.*)/$',
        views.DamageListView.as_view(), name="damage-list-dates"),

    # /damage/damage/list/1
    url(r'damage/list/(?P<pk>[0-9]+)/$', views.DamageUpdateView.as_view(), name="damage-by-id"),

    # /damage/damage/list/criteria/
    url(r'damage/list/criteria/$', views.DamageListCriteriaView.as_view(), name="damage-list-criteria"),

]
