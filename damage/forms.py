from django import forms
from .models import DamageType, Damage , DamageStatus, ContactDetails, DamageHistoryStatus, \
    ContactManagement, Areas , DamageCategory


class DamageTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.desc

class DamageStatusChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.desc


class AreaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.desc


class DamageCategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.desc


class HomeTestForm(forms.ModelForm):
    code = forms.IntegerField()
    desc = forms.CharField(max_length=100)

    class Meta:
        model = DamageType
        fields = ('code', 'desc',)


class DamageEntryForm(forms.ModelForm):
    firstname = forms.CharField(max_length=50, required=False)
    lastname = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=100, required=False,
                                widget = forms.TextInput(
                                    attrs={
                                        'placeholder': ''
                                    }
                                )
                             )
    zipcode = forms.CharField(max_length=6, required=False)
    town = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(max_length=100, required=False)
    thl = forms.CharField(max_length=100, required=False)
    mobile = forms.CharField(max_length=50, required=False)
    damagetype = DamageTypeChoiceField(queryset=DamageType.objects.all(),
                                  widget=forms.Select(attrs={'class': 'select2_single form-control', 'blank': 'True'}))
    damageaddress = forms.CharField(max_length=150, required=False)
    damagezipcode = forms.CharField(max_length=6, required=False)
    damagetown = forms.CharField(max_length=50, required=False)
    damagearea = forms.CharField(max_length=50, required=False)
    damagecom = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
                                                                                'placeholder': 'Περιγράψτε τη Βλάβη',
                                                                                'rows': 8
                                                                          }), required=False)
    selected = "selected"
    lat = forms.CharField(max_length=100, required=False)
    formatted_address = forms.CharField(max_length=100, required=False)
    areas = AreaChoiceField(queryset=Areas.objects.all(),
                                  widget=forms.Select(attrs={'class': 'select2_single form-control', 'blank': 'True'}))
    category = DamageCategoryChoiceField(queryset=DamageCategory.objects.all(),
                                  widget=forms.Select(attrs={'class': 'select2_single form-control', 'blank': 'True'}))


    class Meta:
      model = Damage
      fields = ('firstname', 'lastname', 'address', 'zipcode', 'town', 'area', 'email', 'thl', 'mobile', 'damagetype',
                'damageaddress', 'damagezipcode', 'damagetown', 'damagearea', 'damagecom', 'formatted_address',
                'lat', 'lng', 'areas', 'category')

    # def __init__(self, *args, **kwargs):
    #     super(DamageEntryForm, self).__init__(*args, **kwargs)
    #     self.fields['damagetype']=forms.ModelChoiceField(queryset=DamageType.objects.all(), empty_label='Επιλέξτε Βλάβη')


class DamageTypeForm(forms.ModelForm):
    code = forms.IntegerField()
    desc = forms.CharField(max_length=100, required=True,
                                widget = forms.TextInput(
                                    attrs={
                                        'style': 'border-color: blue;',
                                        'placeholder': 'Write your name here'
                                    }
                                )
                           )
    source = forms.CharField(  # A hidden input for internal use
                max_length=50,  # tell from which page the user sent the message
                widget=forms.HiddenInput(),
                required=True
            )

    class Meta:
        model = DamageType
        fields = ['code', 'desc']


class DamageListForm(forms.ModelForm):

    class Meta:
      model = Damage
      fields = ('firstname', 'lastname', 'address', 'zipcode', 'town', 'area', 'email', 'thl', 'mobile', 'damagetype',
                'damageaddress', 'damagezipcode', 'damagetown', 'damagearea', 'damagecom', 'entry_date')


class DamageListCriteriaForm(forms.Form):
    fromdate = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    todate = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    damagestatus = DamageStatusChoiceField(queryset=DamageStatus.objects.all(),
                                           widget=forms.Select(attrs={'class': 'select2_single form-control',
                                                                      'blank': 'True'}), required=False)
    damagetype = DamageTypeChoiceField(queryset=DamageType.objects.all(),
                                       widget=forms.Select(attrs={'class': 'select2_single form-control',
                                                                  'blank': 'True'}), required=False)

    #########################################################################
    #  στη clean_damagestatus(self) to field εει τιμη '1 - Kαταχώρηση Βλαβης '
    ###########################################################################
    # def clean_damagestatus(self):
    #     field = self.cleaned_data['damagestatus']
    #     print('def clean_damagestatus', field)
    #     return field
    #
    # def clean_damagetype(self):
    #     field = self.cleaned_data['damagetype']
    #     print('def clean_damagetype', field)
    #     return field

    ###############################################################################
    #         multiple select drop down
    #############################################################################
    # my_list = list()
    # damagetype_list = DamageType.objects.all()
    # for d in damagetype_list:
    #     l = [d.pk, d.desc]
    #     my_list.append(l)
    #
    #     print(my_list)
    #
    #
    # damagetype = forms.MultipleChoiceField(choices=my_list, widget=forms.SelectMultiple(),
    #                                             required=False)
    #
    # def clean_damagetype(self):
    #     field = ""
    #     for data in self.cleaned_data['damagetype']:
    #         field += str(data) + ","
    #         print('data', str(data))
    #     return field.lstrip(",")

class ContactDetailsForm(forms.ModelForm):
    entrydate = forms.CharField(widget=forms.HiddenInput(attrs={'type': 'datetime-local'}), required=False),
    name = forms.CharField(max_length=100, required=True,
                                widget = forms.TextInput(
                                    attrs={
                                        'style': 'border-color: blue;',
                                        'placeholder': 'Write your name here'
                                    }
                                )
                           )
    email = forms.EmailField(max_length=100, required=True)
    thl = forms.CharField(max_length=100, required=True)
    com = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
        'placeholder': '',
        'rows': 10,
    }), required=True)

    class Meta:
        model = ContactDetails
        fields = ['name', 'email','thl','com']


class ContactListForm(forms.ModelForm):

    class Meta:
        model = ContactDetails
        fields = ['entry_date', 'name', 'email','thl','com']


class ContactListCriteriaForm(forms.Form):
    fromdate = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    todate = forms.CharField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)


class DamageStatusHistoryForm(forms.ModelForm):
    entry_date = forms.CharField(widget=forms.HiddenInput(attrs={'type': 'datetime-local'}), required=False)
    damagestatus = DamageStatusChoiceField(queryset=DamageStatus.objects.all(),
                                  widget=forms.Select(attrs={'class': 'select2_single form-control', 'blank': 'True'}))
    com = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
        'placeholder': '',
        'rows': 2,
    }))

    class Meta:
        model = DamageHistoryStatus
        fields = ['entry_date', 'damagestatus', 'com']

class ContactManagementForm(forms.ModelForm):
    entry_date = forms.CharField(widget=forms.HiddenInput(attrs={'type': 'datetime-local'}), required=False)
    com = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={
        'placeholder': '',
        'rows': 2,
    }))
    deyacom = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
        'placeholder': '',
        'rows': 2,
        })
    )

    class Meta:
        model = ContactManagement
        fields = ['entry_date', 'deyacom', 'com']


class AreasForm(forms.ModelForm):
    code = forms.IntegerField()
    desc = forms.CharField(max_length=100)

    class Meta:
        model = Areas
        fields = ('code', 'desc',)


class DamageCategoryForm(forms.ModelForm):
    code = forms.IntegerField()
    desc = forms.CharField(max_length=100)

    class Meta:
        model = DamageCategory
        fields = ('code', 'desc',)
