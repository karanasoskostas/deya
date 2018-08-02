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


class DamageEntry(TemplateView):
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

            if self.request.user.is_authenticated():
                post.user = request.user


            post.userip = get_client_ip(request)  # το IP του χρήστη

            location = get_cocation(post.lat, post.lng)

            post.location = location
            post.formatted_address= location.formatted_address


            post.entry_date = datetime.datetime.now(tz=timezone.utc)
            post.save()

            form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
            return http.HttpResponseRedirect('damage/add/')
            # οχι reverse γιατί διαβάζει ολο το urls.py απο την αρχη και καθυστερεί σε μεγαλα projects !!!!!
            #return HttpResponseRedirect(reverse('damage-add'), args)
        else:
             print('form is not valid')
             print(form.errors)
            # form = DamageEntryForm()
             args = {'form': form,
                    'general': general
                    }
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


class DamageListEntry(generic.UpdateView):
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
        redirect_url = super(DamageListEntry, self).form_valid(form)
#        print(form.cleaned_data['lastname'])
        lat = form.cleaned_data['lat']
        lng = form.cleaned_data['lng']

        self.object = form.save()

        damage = Damage.objects.get(pk=self.kwargs['pk'])

        location = get_cocation(lat, lng)

        damage.location = location
        damage.formatted_address = location.formatted_address

        damage.save()

        return redirect_url


class DamageList(TemplateView):
    template_name = "damage/damagelist_table.html"

    def get(self, request):
        form = DamageListForm()
        damage_list = Damage.objects.all()
        general = General.objects.get(pk=1)
        request.session['']
        args = {
            'form': form,
            'damage_list': damage_list,
            'general': general
        }
        return render(request, self.template_name, args)


class DamageListCriteria(TemplateView):
    template_name = "damage/damagelist_criteria.html"

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
            fdate = datetime.combine(fdate, datetime.min.time(), tzinfo=pytz.UTC)
            print('fdate ', fdate)
            todate = form.cleaned_data['todate']
            #tdate = datetime.strptime(todate, '%d/%m/%Y') + timedelta(days=1)
            tdate = datetime.strptime(todate, '%d/%m/%Y')
            tdate = datetime.combine(tdate, datetime.max.time(), tzinfo=pytz.UTC)
            print('tdate ', tdate)

            d_list = Damage.objects.filter(entry_date__range=(fdate, tdate))
            paginator = Paginator(d_list, 1)

            page = request.GET.get('page')
            try:
                damage_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                damage_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                damage_list = paginator.page(paginator.num_pages)

            template = "damage/damagelist_table.html"
            form = DamageListForm()
            general = General.objects.get(pk=1)

            fromdatetext = fdate.strftime('%d/%m/%Y')
            todatetext = tdate.strftime('%d/%m/%Y')

            args = {
                'form': form,
                'damage_list': damage_list,
                'general': general,
                'fromdate': fromdatetext,
                'todate': todatetext
            }
            return render(request, template, args)


        else:
            print('form is not valid')
            print(form.errors)
            # form = DamageEntryForm()
            args = {'form': form,
                    'general': general
                    }
            return render(request, self.template_name, args)
