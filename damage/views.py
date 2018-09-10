from .models import General, DamageType, Damage , DamageStatus
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404 ,render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from damage.forms import HomeTestForm, DamageEntryForm, DamageTypeForm, DamageListForm, DamageListCriteriaForm, \
    ContactDetailsForm, ContactListForm
from django.utils import timezone
import datetime
import pytz
from datetime import datetime, date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
import requests
from django import http
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from damage.utils.utils import *
from damage.appfunctions.appfunctions import *
from django.db.models.functions import Lower
from damage.utils.genmodels import LocationDetails
from django.core.mail import send_mail

class TestView(TemplateView):
    template_name = "damage/test/test_list.html"

class Mdb(TemplateView):
    template_name = "damage/mdb.html"


class HomeTest(TemplateView):
    template_name = "damage/hometest.html"

    def get(self,request):

        current_user = request.user
        if self.request.user.is_authenticated:
            print(current_user.id)
        else:
            print('not authonticated')

        return render(request, self.template_name)

class damage_entry_view(TemplateView):
    template_name = "damage/damageadd.html"


    def get(self, request):
        general = General.objects.get(pk=1)
        form = DamageEntryForm()
        args = {'form': form,
                'general': general,
                }
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



            form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
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


class IndexView(TemplateView):

    general = General.objects.get(pk=1)
    template_name = 'damage/index/index.html'

    def get(self, request):
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


class IndexDeyaView(TemplateView):

    general = General.objects.get(pk=1)
    template_name = 'damage/index/index_deya.html'

    def get(self, request):
        context = {
                    'general': self.general
                  }
        return render(request, self.template_name, context)

    def post(self, request):
         if 'contact' in request.POST:  # ανάλογα με ποιο button εχει πατήσει
             viewurl = 'contact-list'
         elif 'list' in request.POST:
             viewurl = 'damage-list-criteria'
        #
        # print(viewurl)
         return redirect(viewurl)



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


class DamageUpdateView(generic.UpdateView):
    model = Damage
    template_name = "damage/damageadd.html"
    form_class = DamageEntryForm
    success_url = 'damage/list/'
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     print(form.cleaned_data['lastname'])
    #
    #     return response

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



class DamageListCriteriaView(TemplateView):
    template_name = "damage/criteria/damagelist_criteria.html"

    def get(self, request):
        form = DamageListCriteriaForm()
        general = General.objects.get(pk=1)

        args = {
            'form': form,
            'general': general
        }
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
            #damagestatus = form.damagestatus
            #print('damagestatus ', damagestatus)
            damagetype = request.POST.get('damagetype')

            #print('damagetype ',damagetype)

            #return render(request, template, args)
            if 'showlist' in request.POST:           # ανάλογα με ποιο button εχει πατήσει
                viewurl = 'damage-list-dates'
            else:
                viewurl = 'damage-list-markers'

            return redirect(viewurl, pfromdate=fromdatetext, ptodate=todatetext,
                            pdamagestatus=damagestatus, pdamagetype=damagetype)

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
            return render(request, self.template_name, args)


class DamageMarkersView(TemplateView):
    template_name = "damage/maps/markers.html"

    def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype):
        general = General.objects.get(pk=1)

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
        return render(request, self.template_name, args)



class DamageListView(TemplateView):
    template_name = "damage/damagelist_table.html"

    def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype):
        form = DamageListForm()

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
        return render(request, self.template_name, args)


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
        print( general.deya_name)

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


class ContactDetailsListView(TemplateView):
    template_name = "damage/contact/contactlist_table.html"

    #def get(self, request, pfromdate, ptodate, pdamagestatus, pdamagetype):
    def get(self, request):
        form = ContactListForm()

        order_by = request.GET.get('order_by', 'entry_date')
        direction = request.GET.get('direction', 'ASC')
        if Lower(direction) == Lower('DESC'):
            order_by = '-{}'.format(order_by)

        d_list = ContactDetails.objects.all().order_by(order_by)


        paginator = Paginator(d_list, 12)

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

        args = {
            'form': form,
            'contact_list': contact_list,
            'page_obj': page_obj,
            'general': general,

        }
        return render(request, self.template_name, args)