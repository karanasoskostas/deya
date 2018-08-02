from .models import General, DamageType, Damage
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404 ,render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from damage.forms import HomeTestForm, DamageEntryForm, DamageTypeForm, DamageListForm, DamageListCriteriaForm
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
from damage.utils.genmodels import LocationDetails
from django.core.mail import send_mail


class Test(TemplateView):
    template_name = "damage/test.html"


class Mdb(TemplateView):
    template_name = "damage/mdb.html"


class HomeTest(TemplateView):
    template_name = "damage/hometest.html"
    #send_mail('test email', 'hello world', 'kpkmp34@gmail.com', ['karanasoskostas@yahoo.gr'], fail_silently=False)


class damage_entry_view(TemplateView):
    template_name = "damage/damageadd.html"


    def get(self, request: object) -> object:
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


def index(request):
    # all_albums = Album.objects.all()
    # template = loader.get_template('music/index.html')
    # context = {'all_albums': all_albums}

    #html = ''
    #for album in all_albums:
    #    url = '/music/' + str(album.id)
    #    html = html + '<a href="' + url + '">' + album.album_title + '</a><br>'
    general = General.objects.get(pk=1)
    template = loader.get_template('damage/index.html')
    context = {
                'general': general
              }
    return HttpResponse(template.render(context, request))


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

    def get(self, request: object) -> object:
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


class DamageListView(TemplateView):
    template_name = "damage/damagelist_table.html"

    def get(self, request, pfromdate: object = None, ptodate: object = None):
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

        d_list = Damage.objects.filter(entry_date__range=(fdate, tdate))
        paginator = Paginator(d_list, 10)

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

        general = General.objects.all()
        fromdatetext = fdate.strftime('%d/%m/%Y')
        todatetext = tdate.strftime('%d/%m/%Y')


        args = {
            'form': form,
            'damage_list': damage_list,
            'general': general,
            'fromdate': fromdatetext,
            'todate': todatetext,
            'page_obj': page_obj
        }
        return render(request, self.template_name, args)


class DamageListCriteriaView(TemplateView):
    template_name = "damage/damagelist_criteria.html"

    def get(self, request):
        form = DamageListCriteriaForm()
        general = General.objects.all()
        args = {
            'form': form,
            'general': general
        }
        return render(request, self.template_name, args)

    def post(self, request):
        general = General.objects.all()
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

            #return render(request, template, args)
            return redirect('damage-list-dates', pfromdate=fromdatetext, ptodate=todatetext)

        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
            return render(request, self.template_name, args)
