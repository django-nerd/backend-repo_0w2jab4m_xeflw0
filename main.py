import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from database import db, create_document
from schemas import User, Product  # keep examples importable

app = FastAPI(title="Flames Marketing Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Flames Marketing Agency API is running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


# ----- Services Endpoint -----
class Service(BaseModel):
    id: str
    name: str
    description: str
    category: str


SERVICES: List[Service] = [
    Service(id="marketing", name="Marketing Strategy", category="Marketing", description="Data-driven go-to-market, funnels, and conversion optimization."),
    Service(id="hosting", name="Website Hosting", category="Web", description="Fast, secure, and scalable hosting with 99.9% uptime."),
    Service(id="design", name="Brand & UI Design", category="Design", description="Brand identities, design systems, and pixel-perfect UI/UX."),
    Service(id="consulting", name="Consulting", category="Advisory", description="Workshops, audits, and fractional CMO support."),
    Service(id="social", name="Social Media Management", category="Marketing", description="Content calendars, community, and growth across platforms."),
    Service(id="ads", name="Advertising & Ad Creation", category="Marketing", description="Creative production and performance media buying."),
    Service(id="ai", name="AI Solutions", category="Technology", description="Automation, chatbots, and custom AI workflows."), 
    Service(id="web", name="Website Design & Development", category="Web", description="Modern, accessible, and lightning-fast websites."),
    Service(id="travel", name="Travel Concierge", category="Concierge", description="End-to-end planning for executive and team travel."),
    Service(id="property", name="Property Rental Management", category="Operations", description="Listing optimization, bookings, and guest experience."),
    Service(id="mobile", name="Mobile App Creation", category="Technology", description="iOS/Android apps from MVP to scale."),
]


@app.get("/api/services", response_model=List[Service])
def list_services():
    return SERVICES


# ----- Lead Capture Endpoint -----
class Lead(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service: Optional[str] = None
    message: Optional[str] = None
    source: str = "website"


@app.post("/api/leads")
def create_lead(lead: Lead):
    # Try to persist if DB configured; otherwise, still return success
    try:
        if db is not None:
            # Store under collection name "lead"
            create_document("lead", lead.model_dump())
            return {"ok": True, "stored": True}
    except Exception as e:
        # Log error but don't fail UX
        return {"ok": True, "stored": False, "error": str(e)[:200]}

    return {"ok": True, "stored": False}


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
        from database import db as _db
        if _db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = _db.name if hasattr(_db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = _db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
