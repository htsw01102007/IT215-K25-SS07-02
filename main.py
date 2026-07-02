from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# 1. Định nghĩa Enum để loại bỏ Magic String
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"

class StatusUpdate(BaseModel):
    status: OrderStatus  # Pydantic sẽ tự động validate input

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    # Tìm kiếm đơn hàng
    order = next((o for o in orders_db if o["id"] == order_id), None)
    
    # 2. "Fail Fast": Nếu không tìm thấy, dừng lại ngay tại đây với 404
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Cập nhật trạng thái (vì đã qua validate bởi Pydantic, ta yên tâm dữ liệu hợp lệ)
    order["status"] = data.status
    
    return {"message": "Cập nhật thành công", "data": order}
