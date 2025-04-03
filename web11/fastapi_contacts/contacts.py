from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from database import get_db
from models import Contact, User
from schemas import ContactCreate, ContactResponse

contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])

@contacts_router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    user = db.query(User).filter(User.email == current_user).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    new_contact = Contact(**contact.dict(), owner_id=user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact
