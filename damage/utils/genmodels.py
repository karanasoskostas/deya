from django.db import models


class LocationDetails(models.Model):
    latitude = models.CharField(max_length=20, null=True, default=None)
    longitude = models.CharField(max_length=20, null=True, default=None)
    place_id = models.CharField(max_length=300, null=True, default=None)
    formatted_address = models.CharField(max_length=250, null=True, default=None)
    street_number = models.CharField(max_length=10, null=True, default=None)
    route = models.CharField(max_length=50, null=True, default=None)
    locality = models.CharField(max_length=50, null=True, default=None)
    administrative_area_level_5 = models.CharField(max_length=50, null=True, default=None)
    administrative_area_level_4 = models.CharField(max_length=50, null=True, default=None)
    administrative_area_level_3 = models.CharField(max_length=50, null=True, default=None)
    country = models.CharField(max_length=50, null=True, default=None)
    postal_code = models.CharField(max_length=10, null=True, default=None)

    def __str__(self):
        return str(self.formatted_address)

    class Meta:
        db_table = 'locationdetails'
