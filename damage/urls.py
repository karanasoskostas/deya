from django.conf.urls import url, include
from . import views

urlpatterns = [
# /damage/test/

    url(r'^api/data/$', views.get_data, name="api-data"),

    url(r'^api/chart/data/$', views.ApiChartDataView.as_view(), name="api-chart-data"),

    url(r'^charts/bar/eidos/$', views.ChartsView.as_view(), name="chart-bar-eidos"),



    url(r'^test/$', views.TestView.as_view(), name="test"),
    url(r'^test1/$', views.Test1View.as_view(), name="test1"),
    url(r'^testpdf/$', views.test_pdf, name="testpdf"),

    url(r'^guest/$', views.IndexView.as_view(), name='index'),




    url(r'^damagetype_add/$', views.damagetype_add, name='damagetype_add'),

    # /damage/hometest/
    url(r'^hometest/$', views.HomeTest.as_view(), name="hometest"),

    # /damage/map/
    url(r'^map/$', views.Map.as_view(), name="map"),

    # /damage/damagetype/add/
    url(r'damagetype/add/$', views.DamageTypeCreate.as_view(), name="damagetype-add"),

    # /damage/damage/add/
    url(r'damage/add/$', views.damage_entry_view.as_view(), name="damage-add"),

    url(r'damage/status/(?P<pk>[0-9]+)/$', views.DamageStatusView.as_view(), name="damage-status"),

    url(r'contact/management/(?P<pk>[0-9]+)/$', views.ContactManagementView.as_view(), name="contact-management"),

    # /damage/damage/list/15_08_2018/15_08_2018/1   το .* παιζει οταν θελω η παραμετρος να ειναι None
    url(r'damage/list_dates/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pdamagestatus>.*)/(?P<pdamagetype>.*)/$',
        views.DamageListView.as_view(), name="damage-list-dates"),

    # /damage/damage/list/1
    url(r'damage/list/(?P<pk>[0-9]+)/$', views.DamageUpdateView.as_view(), name="damage-by-id"),

    # /damage/damage/list/criteria/
    url(r'damage/list/criteria/$', views.DamageListCriteriaView.as_view(), name="damage-list-criteria"),

    # /damage/damage/list/15_08_2018/15_08_2018/1   το .* παιζει οταν θελω η παραμετρος να ειναι None
    url(r'damage/markers/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pdamagestatus>.*)/(?P<pdamagetype>.*)/$',
        views.DamageMarkersView.as_view(), name="damage-list-markers"),

    # /damage/contact/
        url(r'damage/contact/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/$',
            views.ContactDetailsListView.as_view(), name="contact-list-dates"),

    url(r'damage/contact/history/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/$',
        views.ContactDetailsHistoryListView.as_view(), name="contact-list-history-dates"),

    # /damage/damage/list/criteria/
    url(r'contact/list/criteria/$', views.ContactListCriteriaView.as_view(), name="contact-list-criteria"),


]
