import requests
from damage.utils.genmodels import LocationDetails
from damage.models import General
from django.conf import settings


def get_general():
    general = General.objects.get(pk=1)
    return general


def get_client_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_cocation(lat, lng):
    api_key = "AIzaSyDmdCbjHSXuma43DN3X8ihHuyU-rI3KKZY"

    # print(lat + ',' + lng)
    api_response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}&language={2}'.format(lat + ',' + lng, api_key, 'el'))
    #print('after api_response '+ lat + ',' + lng)
    if api_response:
        api_response_dict = api_response.json()
        # print('api_response_dict', api_response_dict)
        location = LocationDetails()

        location.latitude = lat
        location.longitude = lng

        if api_response_dict['status'] == 'OK':

            location.formatted_address = api_response_dict['results'][0]['formatted_address']
            # print('api_response', api_response_dict['results'][0]['formatted_address'])
            # print('location.formatted_adress', location.formatted_adress)
            location.place_id = api_response_dict['results'][0]['place_id']

            # for i in api_response_dict['results'][0]['address_components']:
            #     if i['types'] == 'place_id':
            #         location.place_id = i['long_name']
            #location.place_id = api_response_dict['results']['place_id']
            # print('place_id', location.place_id)

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'route' in field:
                    location.route = types['long_name']

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'street_number' in field:
                    location.street_number = types['long_name']


            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'locality' in field:
                    location.locality = types['long_name']

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'administrative_area_level_5' in field:
                    location.administrative_area_level_5 = types['long_name']

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'administrative_area_level_4' in field:
                    location.administrative_area_level_4 = types['long_name']

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'administrative_area_level_3' in field:
                    location.administrative_area_level_3 = types['long_name']

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'country' in field:
                    location.country = types['long_name']

            for types in api_response_dict['results'][0]['address_components']:
                field = types.get('types', [])
                if 'postal_code' in field:
                    location.postal_code = types['long_name']

            location.save()

    return location
