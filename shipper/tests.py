import datetime
from typing import List
from fastapi import Body, FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


# Định nghĩa lớp cho từng hóa đơn (bill)
class Bill(BaseModel):
    code: str
    transfer: bool


# Định nghĩa lớp cho dữ liệu đầu vào chính
class RequestListBill(BaseModel):
    shipper: str
    bills: List[Bill]


@app.post("/shipper/confirm_bills")
async def make_list_bill_for_shipper(request: RequestListBill):
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f"{current_date}.txt"
    # Nội dung cần thêm vào file
    content_to_append = request.shipper + "\n"
    for index, item in enumerate(request.bills):
        content_to_append += item.code
        if item.transfer:
            content_to_append += "\\"
        if index < len(request.bills) - 1:
            content_to_append += "*"
    content_to_append += "\n\n"
    # Mở file với chế độ append (a), sẽ tạo file nếu chưa tồn tại
    with open(file_name, 'a') as file:
        file.write(content_to_append)
    print(request)
    return 'Success'
