from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_contacts.database import get_db, engine, Base
from fastapi_contacts.schemas import ContactCreate, ContactUpdate, ContactResponse
from fastapi_contacts.crud import create_contact, get_contacts, get_contact, update_contact, delete_contact, search_contacts, upcoming_birthdays
from fastapi_contacts.auth import auth_router
from fastapi_contacts.contacts import contacts_router
from fastapi_contacts.database import Base, engine
from middleware import RateLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Contacts API with Auth")

app.include_router(auth_router)
app.include_router(contacts_router)

app = FastAPI(title="Contacts API")

@app.post("/contacts/", response_model=ContactResponse)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)

@app.get("/contacts/", response_model=list[ContactResponse])
def read_contacts(db: Session = Depends(get_db)):
    return get_contacts(db)

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = update_contact(db, contact_id, contact)
    if updated_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@app.delete("/contacts/{contact_id}", response_model=ContactResponse)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted_contact = delete_contact(db, contact_id)
    if deleted_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact

@app.get("/search/", response_model=list[ContactResponse])
def search(query: str, db: Session = Depends(get_db)):
    return search_contacts(db, query)

@app.get("/birthdays/", response_model=list[ContactResponse])
def birthdays(db: Session = Depends(get_db)):
    return upcoming_birthdays(db)

app = FastAPI()
app.add_middleware(RateLimitMiddleware)

@app.post("/contacts/", dependencies=[Depends(limiter.limit("5/minute"))])
def create_contact():
    return {"message": "Contact created!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволити всі домени
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
