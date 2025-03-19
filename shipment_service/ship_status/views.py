from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Shipment
from .serializers import ShipmentSerializer
import requests
import json
from rest_framework.generics import RetrieveAPIView


def verify_token(token):
    url = 'http://127.0.0.1:8002/api/user_service/verify_token/'
    headers = {'Authorization': f'Bearer {token}'}
    print(token)
    response = requests.post(url, headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json().get('user_id')
    return None


def check_order_item(order_item_id):
    url = f'http://127.0.0.1:8005/api/order_service/detail/{order_item_id}/'
    response = requests.get(url)
    return response.json()

class ShipmentCreateView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        print(user_id)
        if not user_id:
            return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if request.content_type == 'application/json':
            data = request.data
            order_item_id = data.get('order_item_id')
            if not check_order_item(order_item_id):
                return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid order item ID'},
                                status=status.HTTP_400_BAD_REQUEST)

            data['user_id'] = user_id
            data['shipment_status'] = 'Not ship'

            serializer = ShipmentSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                shipment = serializer.save()
                return Response({'shipment_id': shipment.id}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid content type.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ShipmentStatusView(APIView):
    def post(self, request):
        #         if request.content_type == 'application/json':
        #             data = json.loads(request.body)
        #             username = data.get("username")
        #             shipment_data = Shipment.objects.filter(username=username).values().first()
        #             if shipment_data:
        #                 return Response({'status': 'Success', 'status_code': 200, 'message': shipment_data},
        #                                 status=status.HTTP_200_OK)
        #             return Response({'status': 'Failed', 'status_code': 400, 'message': 'User data is not available.'},
        #                             status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid content type.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ShipmentDetailView(RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        # token = request.headers.get('Authorization').split()[1]
        # user_id = verify_token(token)
        # if not user_id:
        #     return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
        #                     status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)
