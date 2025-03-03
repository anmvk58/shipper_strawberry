from django.http import JsonResponse
from django.shortcuts import render
import requests
from .utils import call_kiotviet

url = "https://6213945d89fad53b1ff9b5aa.mockapi.io/api/v1/shipper"
headers = {
    "Content-Type": "application/json",

}


# Create your views here.
def make_list_bill_for_ship(request):
    return render(request, 'shipper/make_bill.html')


def search_bill(request):
    global data
    bill_code = request.GET.get('bill', '')
    return JsonResponse(call_kiotviet(bill_code), safe=False)

