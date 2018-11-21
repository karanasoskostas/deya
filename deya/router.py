from damage.api.viewsets import DamageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('damage', DamageViewSet)