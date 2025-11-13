import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import MenuItem, Order, OrderItem, CustomerInfo

app = FastAPI(title="Abbey Bites API", description="Backend for Abbey Bites online restaurant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Abbey Bites API is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


# ----- Menu Endpoints -----
@app.post("/api/menu", response_model=dict)
def create_menu_item(item: MenuItem):
    item_id = create_document("menuitem", item)
    return {"id": item_id}


@app.get("/api/menu", response_model=List[dict])
def list_menu_items(category: Optional[str] = None):
    filter_q = {"category": category} if category else {}
    docs = get_documents("menuitem", filter_q)
    # map ObjectId to string
    result = []
    for d in docs:
        d["id"] = str(d.pop("_id"))
        result.append(d)
    return result


# ----- Order Endpoints -----
@app.post("/api/orders", response_model=dict)
def create_order(order: Order):
    order_id = create_document("order", order)
    return {"id": order_id}


@app.get("/api/orders", response_model=List[dict])
def list_orders(status: Optional[str] = None, limit: int = 50):
    filter_q = {"status": status} if status else {}
    docs = get_documents("order", filter_q, limit=limit)
    result = []
    for d in docs:
        d["id"] = str(d.pop("_id"))
        result.append(d)
    return result


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
