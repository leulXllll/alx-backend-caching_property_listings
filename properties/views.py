from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from .models import Property
from .serializers import PropertySerializer
from .utils import get_all_properties

@api_view(['GET'])
def property_list(request):
    properties = get_all_properties()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)
