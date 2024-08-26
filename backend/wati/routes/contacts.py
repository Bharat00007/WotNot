from fastapi import APIRouter,Depends,HTTPException
from ..models import Contacts
from ..Schemas import contacts,user
from ..database import database
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user

router=APIRouter(tags=['Contacts'])

@router.post("/contacts/", response_model=contacts.ContactRead)
def create_contact(contact: contacts.ContactCreate, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    existing_contact = db.query(Contacts.Contact).filter(
        (Contacts.Contact.email == contact.email) | (Contacts.Contact.phone == contact.phone)
    ).first()

    if existing_contact:
        raise HTTPException(
            status_code=400, detail="Contact with this email or phone already exists"
        )

    db_contact = Contacts.Contact(
        user_id=get_current_user.id,
    name = contact.name,
    email = contact.email,
    phone = contact.phone,
    tags = contact.tags
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/contacts/", response_model=list[contacts.ContactRead])
def read_contacts(skip: int = 0, limit: int = 10, tag: str = None, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    query = db.query(Contacts.Contact).filter(Contacts.Contact.user_id==get_current_user.id)
    if tag:
        query = query.filter(Contacts.Contact.tags.contains([tag]))
    contacts = query.offset(skip).limit(limit).all()
    return contacts

@router.get("/contacts/{phone_no}", response_model=contacts.ContactRead)
def read_contact(phone_no: str, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    contact = db.query(Contacts.Contact).filter(Contacts.Contact.phone == phone_no,Contacts.Contact.user_id==get_current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.delete("/contacts/{phone}")
def delete_contact(phone: str, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    contact = db.query(Contacts.Contact).filter(Contacts.Contact.phone == phone,Contacts.Contact.user_id==get_current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"ok": True}

@router.put("/contacts/{contact_id}", response_model=contacts.ContactRead)
def update_contact(contact_id: int, contact: contacts.ContactCreate, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    db_contact = db.query(Contacts.Contact).filter(Contacts.Contact.id == contact_id,Contacts.Contact.user_id==get_current_user.id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    existing_contact = db.query(Contacts.Contact).filter(
        (Contacts.Contact.id != contact_id) &
        ((Contacts.Contact.email == contact.email) | (Contacts.Contact.phone == contact.phone))
    ).first()

    if existing_contact:
        raise HTTPException(
            status_code=400, detail="Contact with this email or phone already exists"
        )
    
    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact



