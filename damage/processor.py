from .models import ContactDetails, Damage


def lastcontacts(request):
    return {
        'lastcontacts': ContactDetails.objects.all()[:10]
    }


def lastdamagesstatus_1(request):
    return {
        'laststatus_1': Damage.objects.filter(damagestatus__code=1).order_by('-entry_date')[:10]
    }
