from .models import ContactDetails


def lastcontacts(request):
    return {
        'lastcontacts': ContactDetails.objects.all()[:10]
    }