from bson import ObjectId
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Brand, Clothes
from .serializers import ClothesSerializer, BrandSerializer


@api_view(['GET'])
def get_clothes(request):
    clothes = Clothes.objects.all()
    serializer = ClothesSerializer(clothes, many=True)
    data = serializer.data
    for cloth in data:
        cloth['brand'] = Brand.objects.get(pk=ObjectId(cloth['brand'])).name
    return Response(data)


@api_view(['GET'])
def get_cloth(request, pk):
    try:
        cloth = Clothes.objects.get(pk=ObjectId(pk))
        serializer = ClothesSerializer(cloth)
        data = serializer.data
        data['brand'] = Brand.objects.get(pk=ObjectId(cloth.brand)).name
        return Response(data)
    except Clothes.DoesNotExist:
        return Response({'error': 'Cloth not found'}, status=404)


@api_view(['GET'])
def search_clothes(request):
    key = request.query_params.get('key', '')
    if key:
        brands = Brand.objects.filter(
            Q(name__icontains=key)
        )
        clothes = Clothes.objects.filter(
            Q(name__icontains=key) |
            Q(brand__in=[str(brand.pk) for brand in brands])
        )
        clothes = list(clothes)
    else:
        clothes = Clothes.objects.all()

    serializer = ClothesSerializer(clothes, many=True)
    data = serializer.data
    for cloth in data:
        cloth['brand'] = Brand.objects.get(pk=ObjectId(cloth['brand'])).name
    return Response(data)

