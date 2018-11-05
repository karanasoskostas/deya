from django.conf.urls import url, include
from . import views

urlpatterns = [
# /damage/test/

    url(r'^api/data/$', views.get_data, name="api-data"),

    url(r'^api/chart/data/damagetype/$', views.ApiChartDataViewDamageType.as_view(), name="api-chart-data-damagetype"),
    url(r'^api/chart/data/damagestatus/$', views.ApiChartDataViewDamageStatus.as_view(), name="api-chart-data-damagestatus"),

    url(r'^charts/bar/eidos/$', views.ChartsView.as_view(), name="chart-bar-eidos"),
    url(r'^charts/carousel/$', views.ChartCarouselView.as_view(), name="chart-carousel"),
    url(r'^charts/carousel/various/$', views.ChartCarouselVariousView.as_view(), name="chart-carousel-various"),


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
    url(r'damage/add/$', views.DamageEntryView.as_view(), name="damage-add"),

    url(r'damage/status/(?P<pk>[0-9]+)/$', views.DamageStatusView.as_view(), name="damage-status"),

    url(r'contact/management/(?P<pk>[0-9]+)/$', views.ContactManagementView.as_view(), name="contact-management"),

    # /damage/damage/list/15_08_2018/15_08_2018/1   το .* παιζει οταν θελω η παραμετρος να ειναι None
    url(r'damage/list_dates/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pdamagestatus>.*)/(?P<pdamagetype>.*)/$',
        views.DamageListView.as_view(), name="damage-list-dates"),

    url(r'damage/list_history_dates/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pdamagestatus>.*)/(?P<pdamagetype>.*)/$',
        views.DamageListHistoryView.as_view(), name="damage-list-history-dates"),

    # /damage/damage/list/1
    url(r'damage/list/(?P<pk>[0-9]+)/$', views.DamageUpdateView.as_view(), name="damage-by-id"),

    # /damage/damage/list/criteria/
    url(r'damage/list/criteria/$', views.DamageListCriteriaView.as_view(), name="damage-list-criteria"),

    url(r'damage/list/today/$', views.DamageTodayView.as_view(), name="today-damage-list"),
    url(r'damage/list/status10/$', views.DamageStatus10View.as_view(), name="damage-status10"),
    url(r'damage/list/status50/$', views.DamageStatus50View.as_view(), name="damage-status50"),

    # /damage/damage/list/15_08_2018/15_08_2018/1   το .* παιζει οταν θελω η παραμετρος να ειναι None
    url(r'damage/markers/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pdamagestatus>.*)/(?P<pdamagetype>.*)/$',
        views.DamageMarkersView.as_view(), name="damage-list-markers"),

    # /damage/contact/
    url(r'damage/contact/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/(?P<pkind>[0-9]+)/$',
        views.ContactDetailsListView.as_view(), name="contact-list-dates"),

    url(r'damage/contact/history/(?P<pfromdate>[-\w]+)/(?P<ptodate>[-\w]+)/$',
        views.ContactDetailsHistoryListView.as_view(), name="contact-list-history-dates"),

    # /damage/damage/list/criteria/
    url(r'contact/list/criteria/$', views.ContactListCriteriaView.as_view(), name="contact-list-criteria"),

    url(r'damage/contact/today/$',views.ContactDetailsTodayView.as_view(), name="today-contact-list"),
    url(r'damage/contact/noreplay/$',views.ContactDetailsNoReplayView.as_view(), name="noreplay-contact-list"),


    #----------------  ΠΑΡΑΜΕΤΡΙΚΑ
    url(r'damage/areas/$',views.AreasView.as_view(), name="areas"),
]
