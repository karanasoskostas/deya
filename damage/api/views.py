from rest_framework import generics
from damage.models import Damage
from .serializers import DamageSerializer

from django.utils import timezone
from django.utils.datetime_safe import datetime

# Retrieve
class DamageRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = DamageSerializer


    def get_queryset(self):
        return Damage.objects.all()

# Create
class DamageCreateApiView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = DamageSerializer


    def get_queryset(self):
        return Damage.objects.all()

    def perform_create(self, serializer):
        value = datetime.now(tz=timezone.utc)
        serializer.save(entry_date=value)

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return Damage.objects.get(pk=pk)