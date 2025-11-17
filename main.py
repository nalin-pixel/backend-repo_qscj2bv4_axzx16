import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import GrainProduct, Inquiry, PhotographyService, Booking

app = FastAPI(title="Business API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

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

# Helper to convert ObjectId to string

def serialize_doc(doc: dict):
    if not doc:
        return doc
    doc["id"] = str(doc.get("_id"))
    doc.pop("_id", None)
    return doc

# -------------------- Grain Business Endpoints --------------------

@app.post("/api/products", response_model=dict)
async def create_product(product: GrainProduct):
    try:
        inserted_id = create_document("grainproduct", product)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products", response_model=List[dict])
async def list_products(limit: Optional[int] = 50):
    try:
        docs = get_documents("grainproduct", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inquiries", response_model=dict)
async def create_inquiry(inquiry: Inquiry):
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/inquiries", response_model=List[dict])
async def list_inquiries(limit: Optional[int] = 100):
    try:
        docs = get_documents("inquiry", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- Photography/Videography Endpoints --------------------

@app.post("/api/services", response_model=dict)
async def create_service(service: PhotographyService):
    try:
        inserted_id = create_document("photographyservice", service)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/services", response_model=List[dict])
async def list_services(limit: Optional[int] = 50):
    try:
        docs = get_documents("photographyservice", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bookings", response_model=dict)
async def create_booking(booking: Booking):
    try:
        inserted_id = create_document("booking", booking)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bookings", response_model=List[dict])
async def list_bookings(limit: Optional[int] = 100):
    try:
        docs = get_documents("booking", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/services/seed", response_model=dict)
async def seed_services():
    try:
        # If any services already exist, skip seeding
        existing = list(db["photographyservice"].find({}).limit(1)) if db else []
        if existing:
            return {"status": "ok", "seeded": False}
        defaults = [
            {
                "name": "Free Style",
                "category": "photography",
                "price": None,
                "duration_hours": None,
                "description": "Creative freestyle photoshoot for personal branding and portfolios.",
                "image_url": None,
            },
            {
                "name": "Pre-Wedding Shoot",
                "category": "photography",
                "price": None,
                "duration_hours": 4,
                "description": "Romantic pre-wedding session at scenic locations.",
                "image_url": None,
            },
            {
                "name": "Candid Photography",
                "category": "photography",
                "price": None,
                "duration_hours": 6,
                "description": "Natural candid coverage capturing real moments.",
                "image_url": None,
            },
            {
                "name": "Wedding Photography",
                "category": "photography",
                "price": None,
                "duration_hours": 10,
                "description": "Full-day wedding coverage with edited album delivery.",
                "image_url": None,
            },
        ]
        inserted = []
        for item in defaults:
            res_id = create_document("photographyservice", item)
            inserted.append(res_id)
        return {"status": "ok", "seeded": True, "count": len(inserted)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
