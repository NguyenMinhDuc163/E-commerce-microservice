from django.shortcuts import render
from payment.models import PaymentStatus
import requests
import json


def shipment_details_update(user_id, order_item_id):
    shipment_update_url = 'http://127.0.0.1:5000/shipment_updates/'
    shipment_response = requests.post(shipment_update_url)
    if shipment_response.status_code == 200:
        return shipment_response.json()
