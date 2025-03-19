from bson import ObjectId
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Mobile, Producer
from .serializers import MobileSerializer, ProducerSerializer


@api_view(['GET'])
def get_mobiles(request):
    mobiles = Mobile.objects.all()
    serializer = MobileSerializer(mobiles, many=True)
    data = serializer.data
    for mobile in data:
        mobile['producer'] = Producer.objects.get(pk=ObjectId(mobile['producer'])).name
    return Response(data)


@api_view(['GET'])
def get_mobile(request, pk):
    try:
        mobile = Mobile.objects.get(pk=ObjectId(pk))
        serializer = MobileSerializer(mobile)
        data = serializer.data
        data['producer'] = Producer.objects.get(pk=ObjectId(mobile.producer)).name
        return Response(data)
    except Mobile.DoesNotExist:
        return Response({'error': 'Mobile not found'}, status=404)


@api_view(['GET'])
def search_mobiles(request):
    key = request.query_params.get('key', '')
    if key:
        producers = Producer.objects.filter(
            Q(name__icontains=key)
        )
        mobiles = Mobile.objects.filter(
            Q(name__icontains=key) |
            Q(producer__in=[str(producer.pk) for producer in producers])
        )
        mobiles = list(mobiles)
    else:
        mobiles = Mobile.objects.all()

    serializer = MobileSerializer(mobiles, many=True)
    data = serializer.data
    for mobile in data:
        mobile['producer'] = Producer.objects.get(pk=ObjectId(mobile['producer'])).name
    return Response(data)
