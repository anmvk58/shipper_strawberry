import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render
import requests
from .utils import call_kiotviet, make_bill
from django.views.decorators.csrf import csrf_exempt

url = "https://6213945d89fad53b1ff9b5aa.mockapi.io/api/v1/shipper"
headers = {
    "Content-Type": "application/json",

}


# Create your views here.
def make_list_bill_for_ship(request):
    return render(request, 'shipper/make_bill.html')


def search_bill(request):
    bill_code = request.GET.get('bill', '')
    bill_code = make_bill(bill_code)
    return JsonResponse(call_kiotviet(bill_code), safe=False)

@csrf_exempt
def confirm_bill(request):
    data = json.loads(request.body)
    # print(json.dumps(request.body, indent=4, ensure_ascii=False))
    shipper = data.get("shipper")
    bills = data.get("bills")

    current_date = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f"{current_date}.txt"

    # Nội dung cần thêm vào file
    content_to_append = shipper + "\n"
    for index, item in enumerate(bills):
        content_to_append += item['bill_code']
        if item['transfer']:
            content_to_append += "/"
        if index < len(bills) - 1:
            content_to_append += "*"
    content_to_append += "\n\n"
    # Mở file với chế độ append (a), sẽ tạo file nếu chưa tồn tại
    with open(file_name, 'a', encoding="utf-8") as file:
        file.write(content_to_append)

    # make response to return
    result = {
        "message": "Success !"
    }

    return JsonResponse(result, safe=False)