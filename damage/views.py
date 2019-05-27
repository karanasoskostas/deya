import os

from django.template import context

from damage.appfunctions.exportexcel import export_list_xls
from .models import DamageType, DamageStatus, DamageHistoryStatus , Areas, DamageCategory
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, View
from damage.forms import DamageEntryForm, DamageTypeForm, DamageListForm, DamageListCriteriaForm, \
    ContactDetailsForm, ContactListForm, ContactListCriteriaForm, DamageStatusHistoryForm, \
    ContactManagementForm, AreasForm , DamageCategoryForm
from django.utils import timezone
import datetime
import pytz
from datetime import datetime, timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from damage.appfunctions.appfunctions import *
from django.db.models.functions import Lower
from django.db.models import Count, Exists, OuterRef, Q
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
import xlsxwriter
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib import messages
from django.contrib.auth import authenticate, login





#   CHART Views

class ChartsView(View):
    def get(self, request, *args, **kwargs):
        general = General.objects.get(pk=1)
        args = {'general': general,
                }
        return render(request, 'damage/charts/charts.html', args)


def get_data(request, *args, **kwargs):
    data = {
        'sales': 100,
        'customers': 10,
    }
    return JsonResponse(data)


#     ANA ΕΙΔΟΣ ΒΛΑΒΗΣ - ΟΛΕΣ ΟΙ ΒΛΑΒΕΣ
class ApiChartDataViewDamageType(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = list()
        default_items = list()
        background_colors = list()
        border_colors = list()
        damage = Damage.objects.all().values('damagetype').annotate(total=Count('damagetype')).values_list('damagetype__desc', 'total').order_by('damagetype')
        i = 1
        for d in damage:
            labels.append(d[0])
            default_items.append(d[1])
            if i == 1:
                bcolor = 'rgba(255, 99, 132, 0.2)'
                border = 'rgba(255,99,132,1)'
                i = i+1
            elif i == 2:
                bcolor = 'rgba(54, 162, 235, 0.2)'
                border = 'rgba(54, 162, 235, 1)'
                i = i + 1
            elif i == 3:
                bcolor = 'rgba(255, 206, 86, 0.2)'
                border = 'rgba(255, 206, 86, 1)'
                i = i + 1
            elif i == 4:
                bcolor = 'rgba(75, 192, 192, 0.2)'
                border = 'rgba(75, 192, 192, 1)'
                i = i + 1
            elif i == 5:
                bcolor = 'rgba(153, 102, 255, 0.2)'
                border = 'rgba(153, 102, 255, 1)'
                i = i + 1
            elif i == 6:
                bcolor = 'rgba(255, 159, 64, 0.2)'
                border = 'rgba(255, 159, 64, 1)'
                i = 1
            background_colors.append(bcolor)
            border_colors.append(border)

        #labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        #default_items = [12, 19, 3, 5, 1, 3]
        data = {
            'labels': labels,
            'default': default_items,
            'background': background_colors,
            'border': border_colors
        }
        return Response(data)


#     ANA STATUS ΒΛΑΒΗΣ - ΟΛΕΣ ΟΙ ΒΛΑΒΕΣ
class ApiChartDataViewDamageStatus(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = list()
        default_items = list()
        background_colors = list()
        border_colors = list()
        damage = Damage.objects.all().values('damagestatus').annotate(total=Count('damagestatus')).values_list('damagestatus__desc', 'total').order_by('damagestatus')
        i = 1
        for d in damage:
            labels.append(d[0])
            default_items.append(d[1])
            if i == 1:
                bcolor = 'rgba(255, 99, 132, 0.2)'
                border = 'rgba(255,99,132,1)'
                i = i+1
            elif i == 2:
                bcolor = 'rgba(54, 162, 235, 0.2)'
                border = 'rgba(54, 162, 235, 1)'
                i = i + 1
            elif i == 3:
                bcolor = 'rgba(255, 206, 86, 0.2)'
                border = 'rgba(255, 206, 86, 1)'
                i = i + 1
            elif i == 4:
                bcolor = 'rgba(75, 192, 192, 0.2)'
                border = 'rgba(75, 192, 192, 1)'
                i = i + 1
            elif i == 5:
                bcolor = 'rgba(153, 102, 255, 0.2)'
                border = 'rgba(153, 102, 255, 1)'
                i = i + 1
            elif i == 6:
                bcolor = 'rgba(255, 159, 64, 0.2)'
                border = 'rgba(255, 159, 64, 1)'
                i = 1
            background_colors.append(bcolor)
            border_colors.append(border)

        #labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        #default_items = [12, 19, 3, 5, 1, 3]
        data = {
            'labels': labels,
            'default': default_items,
            'background': background_colors,
            'border': border_colors
        }
        return Response(data)


# Carousel 1 chart
class ChartCarouselView(TemplateView):
    template_name = "damage/charts/carousel.html"

    def get(self, request):
        general = General.objects.get(pk=1)
        self.template_name = check_authentication(request, self.template_name)
        args = {
            'general': general,
        }

        return render(request, self.template_name, args)


# Carousel many charts
class ChartCarouselVariousView(TemplateView):

    template_name = "damage/charts/carousel/carousel_various.html"

    def get(self, request):
        general = General.objects.get(pk=1)

        args = {
            'general': general,
        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)


#   TEST Views
class TestView(TemplateView):
    template_name = "damage/test/test_carousel.html"
    #template_name = "damage/charts/carousel.html"

    def get(self, request):
        general = General.objects.get(pk=1)

        args = {
            'general': general,
        }

        return render(request, self.template_name, args)


class Test1View(TemplateView):
    #template_name = 'damage/test/sidebarmenu_test.html'
    template_name = 'damage/charts/chart_test.html'


def test_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


class DamageTypeTest(TemplateView):
    template_name = "damage/damagetypetest.html"

    def get(self, request):
        form = DamageTypeForm()
        args = {
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = DamageTypeForm(request.POST)

        form = DamageTypeForm()
        args = {'form': form}
        return render(request, self.template_name, args)


class HomeTest(TemplateView):
    template_name = "damage/hometest.html"

    def get(self,request):

        current_user = request.user
        if self.request.user.is_authenticated:
            print(current_user.id)
        else:
            print('not authonticated')

        return render(request, self.template_name)
#   INDEX Views


class IndexView(TemplateView):

    general = General.objects.get(pk=1)
    template_name = 'damage/index/index.html'

    def get(self, request):

        if not self.request.user.is_authenticated:
            user = authenticate(username='guest', password='deya1234')
            if user is not None:
                login(request, user)

        context = {
                    'general': self.general
                  }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'add' in request.POST:  # ανάλογα με ποιο button εχει πατήσει
            viewurl = 'damage-add'
        elif 'list' in request.POST:
            viewurl = 'damage-list-criteria'

        print(viewurl)
        return redirect(viewurl)


#   ΚENTΡIKH ΣΕΛΙΔΑ
class IndexDeyaView(TemplateView):
    template_name = 'damage/frontpage/frontpage-deya.html'

    def get(self, request):
        general = General.objects.get(pk=1)
        today = datetime.now(tz=timezone.utc)
        datetime_filter = datetime(today.year, today.month, today.day)

        new_damages = Damage.objects.filter(entry_date__startswith=datetime_filter.date()).count()
        damages_status_1 = Damage.objects.filter(damagestatus__code=1).count()
        # 10 ΕΠΙΒΕΒΑΙΩΜΕΝΗ ΒΛΑΒΗ
        damages_status_lt_10 = Damage.objects.filter(damagestatus__code__lt=10).count()
        # 50 ΣΕ ΕΠΙΣΚΕΥΗ
        damages_status_50 = Damage.objects.filter(damagestatus__code=50).count()
        new_messages = ContactDetails.objects.filter(entry_date__startswith=datetime_filter.date()).count()
        no_replay_messages = ContactDetails.objects.annotate(
            no_replay=Exists(ContactManagement.objects.filter(contact__pk=OuterRef('pk')))
        ).filter(no_replay=False,).count()



        args = { 'general': general,
                 'today': today,
                 'new_messages': new_messages,
                 'new_damages': new_damages,
                 'damages_status_1': damages_status_1,
                 'damages_status_lt_10': damages_status_lt_10,
                 'damages_status_50': damages_status_50,
                 'no_replay_messages': no_replay_messages,
               }

        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)


class FrontPageView(TemplateView):
    general = General.objects.get(pk=1)
    template_name = 'damage/frontpage/frontpage.html'

    def get(self, request):
        context = {
                    'general': self.general
                  }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'guest' in request.POST:  # ανάλογα με ποιο button εχει πατήσει
            viewurl = 'index'
        else:
            viewurl = 'login'

        return redirect(viewurl)


class DamageTypeCreate(CreateView):
    model = DamageType
    # δε χρειαζεται , απο default χρησιμοποιεί τη form με το ονομα του model
    #template_name = 'damage/damagetype_form.html'
    fields = ['code', 'desc']


def damagetype_add(request):
    general = General.objects.get(pk=1)
    template = loader.get_template('damage/damagetype_add.html')
    context = {
                'general': general
              }
    return HttpResponse(template.render(context, request))


class Map(TemplateView):
    template_name = "damage/map.html"

    def get(self, request):
        return render(request, self.template_name)

#--------------------------------------------------------------------------------------------------------------
#   ENTRY Views

#--------------------------------------------------------------------------------------------------------------
#   DAMAGE ENTRY View
class DamageEntryView(TemplateView):
    template_name = "damage/entry/damageadd.html"

    def get(self, request):
        general = General.objects.get(pk=1)
        form = DamageEntryForm()

        if not self.request.user.is_authenticated:
            user = 'guest'
        else:
            user = self.request.user.username

        if user == 'guest':
            load_template= 'damage/menus/menu.html'
        else:
            load_template = 'damage/menus/sidebarmenu.html'

        args = {'form': form,
                'general': general,
                'load_template': load_template
                }

        #self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.get(pk=1)
        form = DamageEntryForm(request.POST)
        form.non_field_errors()

        if form.is_valid():
            post = form.save(commit=False)

            if self.request.user.is_authenticated:  # κάποια στιγμή το is_authenticated() χτύπησε !!!!
                post.user = request.user

            post.userip = get_client_ip(request)  # το IP του χρήστη

            location = get_cocation(post.lat, post.lng)

            post.location = location
            post.formatted_address= location.formatted_address

            post.entry_date = datetime.now(tz=timezone.utc)
            post.save()

            damage_mail(post.id)

            if not self.request.user.is_authenticated:
                user = 'guest'
            else:
                user = self.request.user.username

            if user == 'guest':
                load_template = 'damage/menus/menu.html'
            else:
                load_template = 'damage/menus/sidebarmenu.html'

            form = DamageEntryForm()
            args = {'form': form,
                    'general': general,
                    'load_template': load_template
                    }
            user = self.request.user.username
            if user == 'guest':
                template_name = "damage/frontpage/ok.html"
                return render(request, template_name, args)
            else:
                return redirect(request.META.get('HTTP_REFERER'))
            # οχι reverse γιατί διαβάζει ολο το urls.py απο την αρχη και καθυστερεί σε μεγαλα projects !!!!!
            #return HttpResponseRedirect(reverse('damage-add'), args)
        else:
             print('form is not valid')
             print(form.errors)
            # form = DamageEntryForm()
             args = {'form': form,
                    'general': general
                    }
             print(request.build_absolute_uri())
             return render(request, self.template_name, args)


class DamageUpdateView(generic.UpdateView):
    model = Damage
    template_name = "damage/entry/damageadd.html"
    form_class = DamageEntryForm
    success_url = 'damage/list/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if  self.request.user == 'guest':
            load_template = 'damage/menus/menu.html'
        else:
            load_template = 'damage/menus/sidebarmenu.html'
        context['load_template'] = load_template

        general = General.objects.get(pk=1) # για να διαβασει τις συντεταγμενες κτλ.
        context['general'] = general

        return context

    def form_valid(self, form):
        redirect_url = super(DamageUpdateView, self).form_valid(form)
        next = self.request.POST.get('next')
        print(next)
#        print(form.cleaned_data['lastname'])
        lat = form.cleaned_data['lat']
        lng = form.cleaned_data['lng']

        self.object = form.save()

        damage = Damage.objects.get(pk=self.kwargs['pk'])

        location = get_cocation(lat, lng)

        damage.location = location
        damage.formatted_address = location.formatted_address

        damage.save()

        return HttpResponseRedirect(next)
        #return redirect_url


# Damage Criteria
class DamageListCriteriaView(TemplateView):
    template_name = "damage/criteria/damagelist_criteria.html"

    def get(self, request):
        form = DamageListCriteriaForm()
        general = General.objects.get(pk=1)
        if self.request.user.is_authenticated:
            load_template='damage/menus/sidebarmenu.html'
        else:
            load_template = 'damage/menus/menu.html'

        args = {
            'form': form,
            'general': general,
            'load_template': load_template
        }
        #self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.get(pk=1)
        form = DamageListCriteriaForm(request.POST)
        form.non_field_errors()

        if form.is_valid():

            fromdate = request.POST.get('fromdate')
            fdate = datetime.strptime(fromdate, '%d/%m/%Y')
            fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

            todate = form.cleaned_data['todate']
            #tdate = datetime.strptime(todate, '%d/%m/%Y') + timedelta(days=1)  #  και αυτό παίζει !!!!
            tdate = datetime.strptime(todate, '%d/%m/%Y') # string to datetime
            tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime

            fromdatetext = fdate.strftime('%d_%m_%Y')
            todatetext = tdate.strftime('%d_%m_%Y')

            damagestatus = request.POST.get('damagestatus')
            if damagestatus == "":
                damagestatus = "None"
            #damagestatus = form.damagestatus
            #print('damagestatus ', damagestatus)
            damagetype = request.POST.get('damagetype')
            if damagetype == "":
                damagetype = "None"
            #print('damagetype ',damagetype)

            #return render(request, template, args)
            if 'showlist' in request.POST:           # ανάλογα με ποιο button εχει πατήσει
                viewurl = 'damage-list-dates'
            elif 'history' in request.POST:
                viewurl = 'damage-list-history-dates'
            else:
                viewurl = 'damage-list-markers'

            return redirect(viewurl, pfromdate=fromdatetext, ptodate=todatetext,
                            pdamagestatus=damagestatus, pdamagetype=damagetype,
                            pkind=0)

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
            return render(request, self.template_name, args)


# ΒΛΑΒΕΣ ΗΜΕΡΑΣ
class DamageTodayView(TemplateView):
    viewurl = 'damage-list-dates'

    def get(self, request):
        fromdatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        todatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        return redirect(self.viewurl, pfromdate=fromdatetext, ptodate=todatetext, pdamagestatus="None", pdamagetype="None")

# MH ΕΠΙΒΕΒΑΙΩΜΕΝΕΣ ΒΛΑΒΕΣ Damage STATUS < 10
class DamageStatus10View(TemplateView):
    viewurl = 'damage-list-dates'

    def get(self, request):
        fromdatetext = (datetime.now(tz=timezone.utc) - timedelta(days=36500)).strftime('%d_%m_%Y')
        todatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        status = DamageStatus.objects.filter(code=10).values('id')[0]['id']
        return redirect(self.viewurl, pfromdate=fromdatetext, ptodate=todatetext, pdamagestatus=None, pdamagetype="None", pkind=1)

# ΧΩΡΙΣ ΕΠΙΚΟΙΝΩΝΙΑ Damage STATUS < 2
class DamageStatusLt2View(TemplateView):
    viewurl = 'damage-list-dates'

    def get(self, request):
        fromdatetext = (datetime.now(tz=timezone.utc) - timedelta(days=36500)).strftime('%d_%m_%Y')
        todatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        status = DamageStatus.objects.filter(code=2).values('id')[0]['id']
        return redirect(self.viewurl, pfromdate=fromdatetext, ptodate=todatetext, pdamagestatus=None, pdamagetype="None", pkind=2)



# ΣΕ ΕΠΙΣΚΕΥΗ Damage STATUS 50
class DamageStatus50View(TemplateView):
    viewurl = 'damage-list-dates'

    def get(self, request):
        fromdatetext = (datetime.now(tz=timezone.utc) - timedelta(days=36500)).strftime('%d_%m_%Y')
        todatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        status = DamageStatus.objects.filter(code=50).values('id')[0]['id']
        return redirect(self.viewurl, pfromdate=fromdatetext, ptodate=todatetext, pdamagestatus=status, pdamagetype="None", pkind=0)

#--------------------------------------------------------------------------------------------------------------
# ΠΡΟΒΟΛΗ ΒΛΑΒΩΝ ΣΤΟ ΧΑΡΤΗ
class DamageMarkersView(TemplateView):
    template_name = "damage/maps/markers.html"

    def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype , pkind):
        general = General.objects.get(pk=1)

        if pkind is None:
            pkind = 0

        if pfromdate is None:      # παντα is None oxi == None
            pfromdate = '01_01_2000'

        if ptodate is None:
            ptodate = '01_01_2100'

        fdate = datetime.strptime(pfromdate, '%d_%m_%Y')  # ερχεται με format dd_mm_yyyy
        fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

        tdate = datetime.strptime(ptodate, '%d_%m_%Y')  # string to datetime
        tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime
        # tdate = datetime.strptime(todate, '%d/%m/%Y') + timedelta(days=1)  #  και αυτό παίζει !!!!

        if pdamagestatus == '' or pdamagestatus =="None":
            fromdamagestatuspk = 0
            todamagestatuspk = 99999
            statusdesc = 'ΟΛΑ'
        else:
            fromdamagestatuspk = int(pdamagestatus)
            todamagestatuspk = fromdamagestatuspk
            statusdesc = DamageStatus.objects.get(pk=fromdamagestatuspk).desc

        if pdamagetype == '' or pdamagetype =="None":
            fromdamagetypepk = 0
            todamagetypepk = 99999
            typedesc = 'ΟΛΑ'
        else:
            fromdamagetypepk = int(pdamagetype)
            todamagetypepk = fromdamagetypepk
            typedesc = DamageType.objects.get(pk=fromdamagetypepk).desc

        damage = Damage.objects.filter(entry_date__range=(fdate, tdate),
                                       damagestatus__pk__range =(fromdamagestatuspk, todamagestatuspk),
                                       damagetype__pk__range=(fromdamagetypepk, todamagetypepk)).order_by('entry_date')

        my_list = list()
        l = list

        for d in damage:
            if d.lat is None:
                d.lat = str(general.deya_latitude)
            if d.lng is None:
                d.lng = str(general.deya_longitude)
            l= [d.formatted_address, d.lat, d.lng, d.damagetype.desc, d.pk, d.damagestatus.desc, d.entry_date.strftime('%d/%m/%Y %H:%M')]
            my_list.append(l)
            #print(d.damagetype.desc)


        # mylocations = [
        #     ['Bondi Beach', -33.890542, 151.274856],
        #     ['Coogee Beach', -33.923036, 151.259052],
        #     ['Cronulla Beach', -34.028249, 151.157507],
        #     ['Manly Beach', -33.80010128657071, 151.28747820854187],
        #     ['Maroubra Beach', -33.950198, 151.259302]
        # ]

        #lat = -33.92
        lat = general.deya_latitude
        lng = general.deya_longitude

        #print(my_list)
        #print(mylocations)
        #print(lat, lng)

        args = {
                'general': general,
                'mylocations': my_list,
                'lat': lat,
                'lng': lng
                }

        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

#--------------------------------------------------------------------------------------------------------------
# ΠΡΟΒΟΛΗ ΒΛΑΒΩΝ table
class DamageListView(TemplateView):
    template_name = "damage/entry/damagelist_table.html"

    def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype, pkind):
        form = DamageListForm()

        if pkind is None:
            pkind = 0

        if pfromdate is None:      # παντα is None oxi == None
            pfromdate = '01_01_2000'

        if ptodate is None:
            ptodate = '01_01_2100'

        fdate = datetime.strptime(pfromdate, '%d_%m_%Y')  # ερχεται με format dd_mm_yyyy
        fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

        tdate = datetime.strptime(ptodate, '%d_%m_%Y')  # string to datetime
        tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime
        # tdate = datetime.strptime(todate, '%d/%m/%Y') + timedelta(days=1)  #  και αυτό παίζει !!!!

        if pdamagestatus == '' or pdamagestatus =="None":
            fromdamagestatuspk = 0
            todamagestatuspk = 99999
            statusdesc = 'ΟΛΑ'
        else:
            fromdamagestatuspk = int(pdamagestatus)
            todamagestatuspk = fromdamagestatuspk
            statusdesc = DamageStatus.objects.get(pk=fromdamagestatuspk).desc

        if pdamagetype == '' or pdamagetype =="None":
            fromdamagetypepk = 0
            todamagetypepk = 99999
            typedesc = 'ΟΛΑ'
        else:
            fromdamagetypepk = int(pdamagetype)
            todamagetypepk = fromdamagetypepk
            typedesc = DamageType.objects.get(pk=fromdamagetypepk).desc

        order_by = request.GET.get('order_by', 'entry_date')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        d_list = Damage.objects.filter(entry_date__range=(fdate, tdate),
                                       damagestatus__pk__range =(fromdamagestatuspk, todamagestatuspk),
                                       damagetype__pk__range=(fromdamagetypepk, todamagetypepk)).order_by(order_by)

        if pkind == "1": # MH ΕΠΙΒΕΒΑΙΩΜΕΝΕΣ ΒΛΑΒΕΣ
            d_list = d_list.filter(damagestatus__code__lt=10)
        elif pkind == "2": # ΒΛΑΒΕΣ ΧΩΡΙΣ ΕΠΙΚΟΙΝΩΝΙΑ
            d_list = d_list.filter(damagestatus__code__lt=2)

        paginator = Paginator(d_list, 12)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
             damage_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            damage_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            damage_list = paginator.page(paginator.num_pages)

        general = General.objects.get(pk=1)
        fromdatetext = fdate.strftime('%d/%m/%Y')
        todatetext = tdate.strftime('%d/%m/%Y')


        args = {
            'form': form,
            'damage_list': damage_list,
            'page_obj': page_obj,
            'general': general,
            'fromdate': fromdatetext,
            'todate': todatetext,
            'statusdesc': statusdesc,
            'typedesc': typedesc

        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

#-----------------------------------------------------------------------------------------------------
# ΛΙΣΤΑ ΒΛΑΒΩΝ ΜΕ ΙΣΤΟΡΙΚΟ ΔΙΑΧΕΙΡΙΣΗΣ
class DamageListHistoryView(TemplateView):
    template_name = "damage/entry/damagelist_history_table.html"

    def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype, pkind):
        form = DamageListForm()

        if pkind is None:
            pkind = 0

        if pfromdate is None:      # παντα is None oxi == None
            pfromdate = '01_01_2000'

        if ptodate is None:
            ptodate = '01_01_2100'

        fdate = datetime.strptime(pfromdate, '%d_%m_%Y')  # ερχεται με format dd_mm_yyyy
        fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

        tdate = datetime.strptime(ptodate, '%d_%m_%Y')  # string to datetime
        tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime
        # tdate = datetime.strptime(todate, '%d/%m/%Y') + timedelta(days=1)  #  και αυτό παίζει !!!!

        if pdamagestatus == '' or pdamagestatus =="None":
            fromdamagestatuspk = 0
            todamagestatuspk = 99999
            statusdesc = 'ΟΛΑ'
        else:
            fromdamagestatuspk = int(pdamagestatus)
            todamagestatuspk = fromdamagestatuspk
            statusdesc = DamageStatus.objects.get(pk=fromdamagestatuspk).desc

        if pdamagetype == '' or pdamagetype =="None":
            fromdamagetypepk = 0
            todamagetypepk = 99999
            typedesc = 'ΟΛΑ'
        else:
            fromdamagetypepk = int(pdamagetype)
            todamagetypepk = fromdamagetypepk
            typedesc = DamageType.objects.get(pk=fromdamagetypepk).desc

        order_by = request.GET.get('order_by', 'entry_date')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        d_list = Damage.objects.filter(entry_date__range=(fdate, tdate),
                                       damagestatus__pk__range =(fromdamagestatuspk, todamagestatuspk),
                                       damagetype__pk__range=(fromdamagetypepk, todamagetypepk)).order_by(order_by)

        damage_history = DamageHistoryStatus.objects.filter(damage__entry_date__range=(fdate, tdate),
                                                            damage__damagestatus__pk__range=(fromdamagestatuspk, todamagestatuspk),
                                                            damage__damagetype__pk__range=(fromdamagetypepk, todamagetypepk)).order_by('-entry_date')

        paginator = Paginator(d_list, 5)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
             damage_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            damage_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            damage_list = paginator.page(paginator.num_pages)

        general = General.objects.get(pk=1)
        fromdatetext = fdate.strftime('%d/%m/%Y')
        todatetext = tdate.strftime('%d/%m/%Y')


        args = {
            'form': form,
            'damage_list': damage_list,
            'damage_history': damage_history,
            'page_obj': page_obj,
            'general': general,
            'fromdate': fromdatetext,
            'todate': todatetext,
            'statusdesc': statusdesc,
            'typedesc': typedesc

        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)
#--------------------------------------------------------------------------------------------------------------
# ΚΑΤΑΧΩΡΗΣΗ ΜΥΝΗΜΑΤΟΣ
class ContactDetailsView(TemplateView):
    template_name = "damage/contact/contactdetails.html"

    def get(self, request):
        form = ContactDetailsForm()
        args = {
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.get(pk=1)

        form = ContactDetailsForm(request.POST)
        form.non_field_errors()

        if form.is_valid():

            post = form.save(commit=False)
            post.userip = get_client_ip(request)  # το IP του χρήστη
            post.entry_date = datetime.now(tz=timezone.utc)
            post.save()

            contactdetails_mail(post.id)

            #viewurl = 'frontpage'
            #return redirect(viewurl)
            message_template = "damage/messages/contactmessage.html"

            args = {
                    'general': general,
                    'deya': general.deya_name
                   }

            return render(request, message_template, args)

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form
                    }
            return render(request, self.template_name, args)

# ΠΡΟΒΟΛΗ ΜΥΝΗΜΑΤΩΝ table contactlist_table.html
class ContactDetailsListView(TemplateView):
    template_name = "damage/contact/contactlist_table.html"

    #def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype):
    def get(self, request, pfromdate, ptodate, pkind):
        form = ContactListForm()

        if pfromdate is None:  # παντα is None oxi == None
            pfromdate = '01_01_2000'

        if ptodate is None:
            ptodate = '01_01_2100'

        fdate = datetime.strptime(pfromdate, '%d_%m_%Y')  # ερχεται με format dd_mm_yyyy
        fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

        tdate = datetime.strptime(ptodate, '%d_%m_%Y')  # string to datetime
        tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime

        order_by = request.GET.get('order_by', 'entry_date')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        d_list = ContactDetails.objects.filter(entry_date__range=(fdate, tdate)).order_by(order_by)

        if pkind == '1':  # Μυνήματα χωρίς Απάντηση pkind=1
            d_list = d_list.annotate(
                        no_replay=Exists(ContactManagement.objects.filter(contact__pk=OuterRef('pk')))
                    ).filter(no_replay=False,)


        search_string = request.GET.get('search_box', None)
        if search_string not in [None, '']:
            d_list = d_list.filter(Q(name__contains=search_string) | Q(email__contains=search_string)|
                                   Q(thl__contains=search_string) | Q(com__contains=search_string))

        #excel export
        excel_string = request.GET.get('excel_input', None)
        #if request.GET.get('excelbutton'):
        if excel_string not in ['0', None]:
            response = export_list_xls(request, d_list, 'contactlist.xlsx')
            return response
            #return your_view(request)


        paginator = Paginator(d_list, 8)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
             contact_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contact_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contact_list = paginator.page(paginator.num_pages)

        general = General.objects.get(pk=1)
        fromdatetext = fdate.strftime('%d/%m/%Y')
        todatetext = tdate.strftime('%d/%m/%Y')

        args = {
            'form': form,
            'contact_list': contact_list,
            'page_obj': page_obj,
            'general': general,
            'fromdate': fromdatetext,
            'todate': todatetext

        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    # def post(self, request, **kwargs):
    #
    #     print(kwargs['fromdate'])
    #
    #     return render(request, self.template_name)




# ΜΥΝΗΜΑΤΑ ΗΜΕΡΑΣ
class ContactDetailsTodayView(TemplateView):
    viewurl = 'contact-list-dates'

    def get(self, request):
        fromdatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        todatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        return redirect(self.viewurl, pfromdate=fromdatetext, ptodate=todatetext, pkind=0)


# ΜΥΝΗΜΑΤΑ ΧΩΡΙΣ ΑΠΑΝΤΗΣΗ
class ContactDetailsNoReplayView(TemplateView):
    viewurl = 'contact-list-dates'

    def get(self, request):
        fromdatetext = (datetime.now(tz=timezone.utc) - timedelta(days=36500)).strftime('%d_%m_%Y')
        todatetext = datetime.now(tz=timezone.utc).strftime('%d_%m_%Y')
        return redirect(self.viewurl, pfromdate=fromdatetext, ptodate=todatetext, pkind=1)


# ΕΠΙΛΟΓΗ ΜΥΝΗΜΑΤΩΝ ΚΡΙΤΗΡΙΑ
class ContactListCriteriaView(TemplateView):
    template_name = "damage/criteria/contactlist_criteria.html"

    def get(self, request):
        form = ContactListCriteriaForm()
        general = General.objects.get(pk=1)

        args = {
            'form': form,
            'general': general
        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.get(pk=1)
        form = ContactListCriteriaForm(request.POST)
        form.non_field_errors()

        if form.is_valid():

            fromdate = request.POST.get('fromdate')
            fdate = datetime.strptime(fromdate, '%d/%m/%Y')
            fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

            todate = form.cleaned_data['todate']
            #tdate = datetime.strptime(todate, '%d/%m/%Y') + timedelta(days=1)  #  και αυτό παίζει !!!!
            tdate = datetime.strptime(todate, '%d/%m/%Y') # string to datetime
            tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime

            fromdatetext = fdate.strftime('%d_%m_%Y')
            todatetext = tdate.strftime('%d_%m_%Y')

            if 'showlist' in request.POST:           # ανάλογα με ποιο button εχει πατήσει
                viewurl = 'contact-list-dates'
                return redirect(viewurl, pfromdate=fromdatetext, ptodate=todatetext, pkind=0)
            else:           # ανάλογα με ποιο button εχει πατήσει
                viewurl = 'contact-list-history-dates'
                return redirect(viewurl, pfromdate=fromdatetext, ptodate=todatetext)

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
            return render(request, self.template_name, args)


class DamageStatusView(TemplateView):
    template_name = "damage/entry/damagestatus.html"

    def get(self, request, pk):
        #form = ContactDetailsForm()
        general = General.objects.get(pk=1)
        damage = Damage.objects.get(pk=pk)
        form = DamageStatusHistoryForm()

        status_list = DamageHistoryStatus.objects.filter(damage=damage).order_by('-entry_date')

        args = {
            'general': general,
            'damage': damage,
            'form': form,
            'status_list': status_list
        }
        return render(request, self.template_name, args)

    def post(self, request, pk):
        general = General.objects.get(pk=1)

        form = DamageStatusHistoryForm(request.POST)
        form.non_field_errors()

        if form.is_valid():

            post = form.save(commit=False)
            post.userip = get_client_ip(request)  # το IP του χρήστη
            if self.request.user.is_authenticated:  # κάποια στιγμή το is_authenticated() χτύπησε !!!!
                post.user = request.user
            post.entry_date = datetime.now(tz=timezone.utc)
            #damage = request.POST.get('damage')
            damage = Damage.objects.get(pk=pk)
            damage.damagestatus = post.damagestatus
            post.damage = damage
            post.save()
            damage.save()

            status_list = DamageHistoryStatus.objects.filter(damage=damage).order_by('-entry_date')

            args = {
                'general': general,
                'damage': damage,
                'form': form,
                'status_list': status_list
            }

            return redirect(request.META.get('HTTP_REFERER'))

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form
                    }
            return render(request, self.template_name, args)


# ΚΑΤΑΧΩΡΗΣΗ ΑΠΑΝΤΗΣΕΩΝ ΜΥΝΗΜΑΤΩΝ
class ContactManagementView(TemplateView):
    template_name = "damage/contact/contactmanagement.html"

    def get(self, request, pk):
        general = General.objects.get(pk=1)
        contact = ContactDetails.objects.get(pk=pk)
        form = ContactManagementForm()

        contact_list = ContactManagement.objects.filter(contact=contact).order_by('-entry_date')

        args = {
            'general': general,
            'contact': contact,
            'form': form,
            'contact_list': contact_list
        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    def post(self, request, pk):
        general = General.objects.get(pk=1)

        form = ContactManagementForm(request.POST)
        form.non_field_errors()

        if form.is_valid():

            post = form.save(commit=False)
            post.userip = get_client_ip(request)  # το IP του χρήστη
            if self.request.user.is_authenticated:  # κάποια στιγμή το is_authenticated() χτύπησε !!!!
                post.user = request.user
            post.entry_date = datetime.now(tz=timezone.utc)
            #damage = request.POST.get('damage')
            contact = ContactDetails.objects.get(pk=pk)
            post.contact = contact
            post.save()

            contactdetails_mail(post.id)

            contact_list = ContactManagement.objects.filter(contact=contact).order_by('-entry_date')

            args = {
                'general': general,
                'contact': contact,
                'form': form,
                'contact_list': contact_list
            }

            return redirect(request.META.get('HTTP_REFERER'))

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form
                    }
            return render(request, self.template_name, args)


# ΜΥΝΗΜΑΤΑ ΜΕ ΑΠΑΝΤΗΣΕΙΣ table
class ContactDetailsHistoryListView(TemplateView):
    #template_name = "damage/contact/contactlist_table.html"
    template_name = "damage/contact/contact_masterdetail_table.html"

    #def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype):
    def get(self, request, pfromdate, ptodate):
        form = ContactListForm()

        if pfromdate is None:  # παντα is None oxi == None
            pfromdate = '01_01_2000'

        if ptodate is None:
            ptodate = '01_01_2100'

        fdate = datetime.strptime(pfromdate, '%d_%m_%Y')  # ερχεται με format dd_mm_yyyy
        fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)  # min time to datetime

        tdate = datetime.strptime(ptodate, '%d_%m_%Y')  # string to datetime
        tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)  # add max time to datetime

        order_by = request.GET.get('order_by', 'entry_date')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        d_list = ContactDetails.objects.filter(entry_date__range=(fdate, tdate)).order_by(order_by)
        contact_history = ContactManagement.objects.filter(contact__entry_date__range=(fdate, tdate)).order_by('-entry_date')

        paginator = Paginator(d_list, 3)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
             contact_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contact_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contact_list = paginator.page(paginator.num_pages)

        general = General.objects.get(pk=1)
        fromdatetext = fdate.strftime('%d/%m/%Y')
        todatetext = tdate.strftime('%d/%m/%Y')

        args = {
            'form': form,
            'contact_list': contact_list,
            'page_obj': page_obj,
            'general': general,
            'fromdate': fromdatetext,
            'todate': todatetext,
            'contact_history': contact_history

        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)


class AreasView(TemplateView):
    template_name = "damage/files/areas.html"
    pagerows = 6

    def get(self, request):
        general = General.objects.get(pk=1)

        order_by = request.GET.get('order_by', 'desc')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        areas_list = Areas.objects.all().order_by(order_by)
        form = AreasForm()

        #contact_list = ContactManagement.objects.filter(contact=contact).order_by('-entry_date')

        paginator = Paginator(areas_list, self.pagerows)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
            areas_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            areas_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            areas_list = paginator.page(paginator.num_pages)


        args = {
            'general': general,
            'form': form,
            'areas_list': areas_list,
            'page_obj': page_obj
        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.get(pk=1)
        form = AreasForm(request.POST)
        form.non_field_errors()

        if 'delete' in request.POST:
            pk = request.POST.get("pk", "")
            item = Areas.objects.get(id=pk)
            item.delete()

        if 'save' in request.POST:

            edit_flag = request.POST.get("edit_flag", "")
            if edit_flag == "1":  #  UPDATE
                code = request.POST.get("code", "")
                desc = request.POST.get("desc", "")
                area = Areas.objects.get(code=code)
                area.desc = desc
                area.save()
            else:                 # ΝΕΑ ΕΓΓΡΑΦΗ

                if form.is_valid():
                    post = form.save(commit=False)
                    #post.userip = get_client_ip(request)  # το IP του χρήστη
                    # if self.request.user.is_authenticated:  # κάποια στιγμή το is_authenticated() χτύπησε !!!!
                    #     post.user = request.user
                    #post.entry_date = datetime.now(tz=timezone.utc)
                    #damage = request.POST.get('damage')

                    code = request.POST.get("code", "")
                    area = Areas.objects.filter(code=code)
                    if area:
                        messages.error(request, 'Ο Κωδικός '+ code +' Υπάρχει ήδη !!')
                    else:
                        post.save()
                else:
                    print('form is not valid')
                    print(form.errors)
                    # form = DamageEntryForm()
                    args = {'form': form
                            }
                    return render(request, self.template_name, args)


        areas_list = Areas.objects.all().order_by('desc')

        paginator = Paginator(areas_list, self.pagerows)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
            areas_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            areas_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            areas_list = paginator.page(paginator.num_pages)

        args = {
            'general': general,
            'form': form,
            'areas_list': areas_list,
            'page_obj': page_obj,

        }

        return redirect(request.META.get('HTTP_REFERER'))


class DamageCategoryView(TemplateView):
    template_name = "damage/files/damagecategory.html"
    pagerows = 6

    def get(self, request):
        general = General.objects.get(pk=1)

        order_by = request.GET.get('order_by', 'desc')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        items_list = DamageCategory.objects.all().order_by(order_by)
        form = DamageCategoryForm()

        paginator = Paginator(items_list, self.pagerows)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
            items_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items_list = paginator.page(paginator.num_pages)


        args = {
            'general': general,
            'form': form,
            'items_list': items_list,
            'page_obj': page_obj
        }
        self.template_name = check_authentication(request, self.template_name)
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.get(pk=1)
        form = DamageCategoryForm(request.POST)
        form.non_field_errors()

        if 'delete' in request.POST:
            pk = request.POST.get("pk", "")
            item = DamageCategory.objects.get(id=pk)
            item.delete()

        if 'save' in request.POST:

            edit_flag = request.POST.get("edit_flag", "")
            if edit_flag == "1":  #  UPDATE
                code = request.POST.get("code", "")
                desc = request.POST.get("desc", "")
                area = DamageCategory.objects.get(code=code)
                area.desc = desc
                area.save()
            else:                 # ΝΕΑ ΕΓΓΡΑΦΗ

                if form.is_valid():
                    post = form.save(commit=False)
                    #post.userip = get_client_ip(request)  # το IP του χρήστη
                    # if self.request.user.is_authenticated:  # κάποια στιγμή το is_authenticated() χτύπησε !!!!
                    #     post.user = request.user
                    #post.entry_date = datetime.now(tz=timezone.utc)
                    #damage = request.POST.get('damage')

                    code = request.POST.get("code", "")
                    area = DamageCategory.objects.filter(code=code)
                    if area:
                        messages.error(request, 'Ο Κωδικός '+ code +' Υπάρχει ήδη !!')
                    else:
                        post.save()
                else:
                    print('form is not valid')
                    print(form.errors)
                    # form = DamageEntryForm()
                    args = {'form': form
                            }
                    return render(request, self.template_name, args)


        items_list = DamageCategory.objects.all().order_by('desc')

        paginator = Paginator(items_list, self.pagerows)

        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        try:
            items_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items_list = paginator.page(paginator.num_pages)

        args = {
            'general': general,
            'form': form,
            'items_list': items_list,
            'page_obj': page_obj,

        }

        return redirect(request.META.get('HTTP_REFERER'))


