from django.db import models
from django.contrib.auth.models import User
from damage.utils.genmodels import LocationDetails


class DamageType(models.Model):
    code = models.IntegerField()
    desc = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.desc

    class Meta:
        db_table = 'damagetype'


class DamageStatus(models.Model):
    code = models.IntegerField()
    desc = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.desc

    class Meta:
        db_table = 'damagestatus'


class Areas(models.Model):
    code = models.IntegerField()
    desc = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.desc

    class Meta:
        db_table = 'areas'


class DamageCategory(models.Model):
    code = models.IntegerField( unique=True)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.desc

    class Meta:
        db_table = 'damagecategory'


class Damage(models.Model):
    entry_date = models.DateTimeField()
    firstname = models.CharField(max_length=50, blank=False, default=None)
    lastname = models.CharField(max_length=50, blank=False, default=None)
    address = models.CharField(max_length=100, null=True , default=None)
    zipcode = models.CharField(max_length=6, null=True , default=None)
    town = models.CharField(max_length=50, null=True , default=None)
    area = models.CharField(max_length=50, null=True , default=None)
    email = models.EmailField(max_length=150, null=True , default=None)
    thl = models.CharField(max_length=100, null=True , default=None)
    mobile = models.CharField(max_length=50, blank=False, default=None)
    damagetype = models.ForeignKey(DamageType, on_delete=models.DO_NOTHING)
    damageaddress = models.CharField(max_length=100, null=True, default=None)
    damagezipcode = models.CharField(max_length=6, null=True, default=None)
    damagetown = models.CharField(max_length=50, null=True, default=None)
    damagearea = models.CharField(max_length=50, null=True, default=None)
    damagecom = models.CharField(max_length=1000, null=True, default=None)
    damagestatus = models.ForeignKey(DamageStatus, default=1, on_delete=models.DO_NOTHING)
    lng = models.CharField(max_length=100, null=True, default=None)
    lat = models.CharField(max_length=100, null=True, default=None)
    formatted_address = models.CharField(max_length=150, null=True, default=None)
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    userip = models.CharField(max_length=100, null=True, default=None)
    location = models.ForeignKey(LocationDetails, blank=True, null=True , default=None, on_delete=models.CASCADE)
    areas = models.ForeignKey(Areas, on_delete=models.DO_NOTHING, null=True, default=None)
    category = models.ForeignKey(DamageCategory, on_delete=models.DO_NOTHING, null=True, default=None)

    def __str__(self):
        return str("{:%d/%m/%Y  %H:%M:%S}".format(self.entry_date)) + '    -    ' + self.lastname + ' ' + self.firstname

    class Meta:
        db_table = 'damage'


class DamageHistoryStatus(models.Model):
    entry_date = models.DateTimeField()
    damage = models.ForeignKey(Damage, on_delete=models.DO_NOTHING)
    damagestatus = models.ForeignKey(DamageStatus, on_delete=models.DO_NOTHING)
    com = models.CharField(max_length=500, null=True, default=None)
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    userip = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return str("{:%d/%m/%Y  %H:%M:%S}".format(self.entry_date)) + '    -    ' + self.damagestatus.desc

    class Meta:
        db_table = 'damagehistorystatus'


class General(models.Model):
    deya_aa = models.IntegerField()
    deya_name = models.CharField(max_length=100)
    deya_longitude = models.DecimalField(max_digits=13, decimal_places=10, null=True , default=0)
    deya_latitude = models.DecimalField(max_digits=13, decimal_places=10, null=True, default=0)
    deya_mapaddress = models.CharField(max_length=150,null=True, default=None)
    google_api_key = models.CharField(max_length=150,null=True, default=None)

    def __str__(self):
        return str(self.deya_aa) + ' - ' + self.deya_name

    class Meta:
        db_table = 'general'


class ContactDetails(models.Model):
    entry_date = models.DateTimeField()
    name = models.CharField(max_length=50, blank=False, default=None)
    email = models.EmailField(max_length=150, null=True, default=None)
    thl = models.CharField(max_length=100, null=True, default=None)
    com = models.CharField(max_length=1000, null=True, default=None)
    userip = models.CharField(max_length=100, null=True, default=None)


    def __str__(self):
        return str("{:%d/%m/%Y  %H:%M:%S}".format(self.entry_date)) + '    -    ' + self.name + ' ' + self.email

    class Meta:
        db_table = 'contactdetails'


class ContactManagement(models.Model):
    entry_date = models.DateTimeField()
    contact = models.ForeignKey(ContactDetails, on_delete=models.DO_NOTHING)
    com = models.CharField(max_length=1000, null=True, default=None)
    deyacom = models.CharField(max_length=500, null=True, default=None)
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    userip = models.CharField(max_length=100, null=True, default=None)


    def __str__(self):
        return str("{:%d/%m/%Y  %H:%M:%S}".format(self.entry_date)) + '    -    ' + self.com

    class Meta:
        db_table = 'contactmanagement'
