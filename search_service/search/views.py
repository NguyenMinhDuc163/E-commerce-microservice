from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from search_service.settings import PRODUCT_SERVICE_BOOK_URL, PRODUCT_SERVICE_CLOTHES_URL, PRODUCT_SERVICE_MOBILE_URL


@api_view(['GET'])
def search_all(request):
    key = request.query_params.get('key', '')
    book_response = requests.get(PRODUCT_SERVICE_BOOK_URL + f'/search_books?key={key}')
    clothes_response = requests.get(PRODUCT_SERVICE_CLOTHES_URL + f'/search_clothes?key={key}')
    mobile_response = requests.get(PRODUCT_SERVICE_MOBILE_URL + f'/search_mobiles?key={key}')
    result = []
    if book_response.status_code == 200:
        result += book_response.json()
    if clothes_response.status_code == 200:
        result += clothes_response.json()
    if mobile_response.status_code == 200:
        result += mobile_response.json()
    return Response(result)


@api_view(['GET'])
def search_books(request):
    key = request.query_params.get('key', '')
    response = requests.get(PRODUCT_SERVICE_BOOK_URL + f'/search_books?key={key}')
    return Response(response.json())


@api_view(['GET'])
def search_clothes(request):
    key = request.query_params.get('key', '')
    response = requests.get(PRODUCT_SERVICE_CLOTHES_URL + f'/search_clothes?key={key}')
    return Response(response.json())


@api_view(['GET'])
def search_mobiles(request):
    key = request.query_params.get('key', '')
    response = requests.get(PRODUCT_SERVICE_MOBILE_URL + f'/search_mobiles?key={key}')
    return Response(response.json())
