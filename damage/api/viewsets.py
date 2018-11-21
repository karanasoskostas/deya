from damage.models import Damage
from .serializers import DamageSerializer
from rest_framework import viewsets


class DamageViewSet(viewsets.ModelViewSet):
    queryset = Damage.objects.all()
    serializer_class = DamageSerializer