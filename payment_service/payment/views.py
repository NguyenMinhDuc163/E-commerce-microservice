from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentStatus
from .serializers import PaymentStatusSerializer
from shipment_update.views import shipment_details_update
import requests
from django.utils.timezone import now

def verify_token(token):
    url = 'http://127.0.0.1:8002/api/user_service/verify_token/'
    headers = {'Authorization': f'Bearer {token}'}
    print(token)
    response = requests.post(url, headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json().get('user_id')
    return None

#Hàm kiểm tra order_item_id
def check_order_item(order_item_id):
    url = f'http://127.0.0.1:8005/api/order_service/detail/{order_item_id}/'
    response = requests.get(url)
    return response.json()


def check_shipment(shipment_id):
    url = f'http://127.0.0.1:8006/api/shipment_service/detail/{shipment_id}/'
    response = requests.get(url)
    return response.json()

class CreatePaymentView(APIView):
    @csrf_exempt
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        order_item_id = data.get('order_item_id')
        order_item = check_order_item(order_item_id)
        print(order_item)
        if not order_item:
            return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid order item ID.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data['user_id'] = user_id
        data['order_item_id'] = order_item_id
        data['status'] = 'Success'
        data['payment_date'] = now().date().isoformat()
        shipment = check_shipment(order_item.get('shipment_id'))
        if not shipment:
            return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid shipment ID.'},
                            status=status.HTTP_400_BAD_REQUEST)
        data['price'] = shipment.get('price') + order_item.get('total')
        serializer = PaymentStatusSerializer(data=data)
        print("Data to be stored:", data)
        if serializer.is_valid():
            payment = serializer.save()
            print("Data stored successfully")
        else:
            print("Errors:", serializer.errors)
            return False
        # shipment_response = shipment_details_update(data['user_id'], data['order_item_id'])
        # if shipment_response.get('status') == 'Success':
        return Response({'payment_id': payment.id}, status=status.HTTP_200_OK)
        # else:
            # return Response({'status': 'Failed', 'status_code': 400, 'message': 'Transaction failed.'},
            #                 status=status.HTTP_400_BAD_REQUEST)


