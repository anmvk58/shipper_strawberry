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
        print(json.dumps(data, indent=4, ensure_ascii=False))
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


def generate_zero(n):
    """
    Hàm này chỉ để generate mỗi chuỗi gồm n số 0 với n được truyền vào
    :param n: số length chuỗi cần gen
    :type n: int
    :return:
    """
    result = ''
    for i in range(n):
        result += '0'
    return result

def make_bill(bill):
    """
    Chuyển đổi thành mã bill đúng với Kiot Việt. định dạng là HD000107 (length = 8)
    Đối với mã đã được update -> sẽ có thêm hậu tố .01 ví dụ HD000107.01, HD000107.02 tùy vào update bao nhiêu lần
    Đối với mã đã được chuyển khoản -> sẽ có thêm hậu tố / để đánh dấu làm bước xử lý tính toán tiền
    :param bill: mã bill được nhập từ input txt
    :type bill: str
    :return: mã bill đã được chuẩn hóa
    """
    # nếu bắt đầu = HD thì return luôn
    if bill.startswith("HD"):
        return bill

    # nếu length >= 9 thì return luôn
    if "." in bill or "/" in bill:
        if len(bill[:bill.find('.')]) >= 8:
            return bill
    else:
        if len(bill) >= 9:
            return bill

    # 1.check có phải đơn chỉnh sửa hay không:
    modify_flag = False
    if '.' in bill:
        modify_flag = True

    # 2.tính ra mã bill gốc nhập từ txt (bỏ qua đơn sửa . và đơn chuyển khoản /)
    if modify_flag:
        org_bill_code = bill[:bill.find('.')]
    else:
        org_bill_code = bill.replace('/', '')

    # 3.tính ra mã bill chuẩn với hệ thống kiotviet:
    kiot_bill = 'HD' + generate_zero(6 - len(org_bill_code)) + org_bill_code

    # 4.thêm vào hậu tố đơn sửa và đơn chuyển khoản nếu có:
    if modify_flag:
        kiot_bill += bill[bill.find('.'):bill.find('.') + 3]
    if '/' in bill:
        kiot_bill += '/'

    return kiot_bill