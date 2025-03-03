import requests

URL = "https://api-man1.kiotviet.vn/api/invoices/list"

HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IndYYSJ9.eyJpc3MiOiJrdnNzand0Iiwic3ViIjoxMDAxNDg0ODgwLCJpYXQiOjE3Mzk5ODE4NzYsImV4cCI6MTc0MjQwMTA3NiwicHJlZmVycmVkX3VzZXJuYW1lIjoiMDU4ODU4MjcxNSIsInJvbGVzIjpbIlVzZXIiXSwia3Zzb3VyY2UiOiJSZXRhaWwiLCJrdnVzZXRmYSI6MCwia3Z3YWl0b3RwIjowLCJrdnNlcyI6IjllNDczM2UwZDM3NjQ1N2E4ZGFjNTY0YzVkOGQwY2VlIiwia3Z1aWQiOjEwMDE0ODQ4ODAsImt2bGFuZyI6InZpLVZOIiwia3Z1dHlwZSI6MCwia3Z1bGltaXQiOiJGYWxzZSIsImt2dWFkbWluIjoiVHJ1ZSIsImt2dWFjdCI6IlRydWUiLCJrdnVsaW1pdHRyYW5zIjoiRmFsc2UiLCJrdnVzaG93c3VtIjoiVHJ1ZSIsImt2YmkiOiJGYWxzZSIsImt2YmlkIjoxMDAwMDE4MzQyLCJrdnJpbmRpZCI6OSwia3ZyY29kZSI6IjA1ODg1ODI3MTUiLCJrdnJpZCI6NTAwNjg5NzMxLCJrdnVyaWQiOjUwMDY4OTczMSwia3ZyZ2lkIjozNiwicGVybXMiOiIifQ.pHtVjCz0egRM9DfAcnfa8ei6q_OA9GWp_YUzincyCu2Nr_SuHCqgHZ3fnrMvIQbKBr2A-5uBOzESukVmd7rm25Ce1XF6d3UX4ud-iFEw7RUlMqr02HhYXSV1IyZ-W0ORcRB0Dra7x_2WdNxVrJizYqPt2fH24CraA7NDIHNvFpjZjorDgb3Iyn7fZD3BzDleXVEFz27Htl1DNtc51XCRGEmA8nUtdWOFsA4TpI_TWiiOA66JduhNnNbnILRnw7p5Jj1GR9BiEz5QuCkYMG0blnm92lRvta70QAkkGFaM8GCXvtnXEFQ4rRDt1ludxYJhWGmth6Qbmg24aQlRgF0OnQ",
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
        result = {
            'code': data['Data'][1]['Code'],
            'customer_name': data['Data'][1]['Customer']['Name'],
            'customer_phone': data['Data'][1]['Customer']['ContactNumber'],
            'address': data['Data'][1]['Customer']['Address'],
            'bill': data['Data'][1]['Total']
        }
        return result
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None