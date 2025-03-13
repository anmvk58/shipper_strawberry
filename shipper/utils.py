import json

import requests
from decouple import config

URL = config('API')

HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer " + config('TOKEN'),
        "branchid": "1000018342",
        "content-type": "application/json; charset=utf-8",
        "fingerprintkey": "211d1f5bb8cc08a94863d2291f1c866d_Chrome_Desktop_Máy tính Windows",
        "isusekvclient": "1",
        "origin": "https://0588582715.kiotviet.vn",
        "priority": "u=1, i",
        "referer": "https://0588582715.kiotviet.vn/",
        "retailer": "0588582715",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133")',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "x-group-id": "36",
        "x-language": "vi-VN",
        "x-retailer-code": "0588582715",
        "x-timezone": "",
    }

PARAMS = {
        "format": "json",
        "Includes": [
            "Customer", "Payments", "User"
        ],
        "ForSummaryRow": "true",
        "UsingTotalApi": "true",
        "UsingStoreProcedure": "false",
    }

DATA = '{"$inlinecount":"allpages","$format":"json","CustomerKey":"","UserNameKey":"","CreateUserName":"","SerialKey":"","BatchExpireKey":"","DescriptionProductKey":"","DeliveryCode":"","ExpectedDeliveryFilterType":"alltime","OrderCode":"","FiltersForOrm":"{\\"Code\\":\\"BILL_CODE\\",\\"Description\\":\\"\\",\\"DescriptionProduct\\":\\"\\",\\"BranchIds\\":[1000018342],\\"PriceBookIds\\":[],\\"FromDate\\":null,\\"ToDate\\":null,\\"FromDateStr\\":null,\\"ToDateStr\\":null,\\"TimeRange\\":\\"thisweek\\",\\"InvoiceStatus\\":[3,1],\\"UsingCod\\":[],\\"TableIds\\":[],\\"SalechannelIds\\":[],\\"StartDeliveryDate\\":null,\\"EndDeliveryDate\\":null,\\"StartDeliveryDateStr\\":null,\\"EndDeliveryDateStr\\":null,\\"UsingPrescription\\":2,\\"Prescription\\":\\"\\",\\"Patient\\":\\"\\",\\"Diagnosis\\":\\"\\"}","InvoiceStatus":"[3,1]","$top":15,"$filter":"(substringof(\'BILL_CODE\',Code) and PurchaseDate eq \'thisweek\')"}'


def call_kiotviet(bill_code):
    input_data = DATA.replace('BILL_CODE', bill_code)
    response = requests.post(URL, headers=HEADERS, params=PARAMS, data=input_data)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        # print(json.dumps(data, indent=4, ensure_ascii=False))
        result = {}

        try:
            result = {
                'code': data['Data'][1]['Code'],
                'customer_name': data['Data'][1]['CustomerName'] if data['Data'][1]['CustomerName'] != '' else 'Khách Lẻ',
                'customer_phone': data['Data'][1]['CustomerContactNumber'],
                'address': data['Data'][1]['CustomerAddress'] if "CustomerAddress" in data['Data'][1] else "---",
                'bill': data['Data'][1]['Total'],
                'error': ''
            }

        except IndexError:
            print("Error: lỗi dữ liệu từ kiotviet trả về")
            result = {
                'error': 'lỗi dữ liệu từ kiotviet trả về'
            }
        except Exception as e:
            print("Error: " + str(e))
            result = {
                'error': e
            }
        return result
    else:
        print(f"Error {response.status_code}: {response.text}")
        return {
                'error': 'Lỗi Mã HTTP <> 200 ! Call API Thất bại'
            }