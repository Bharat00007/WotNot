from fastapi import APIRouter,Depends,HTTPException, File, UploadFile , Request
from ..models import Broadcast,Contacts
from ..Schemas import broadcast,user
from ..database import database
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from pydantic import BaseModel , HttpUrl
import requests
import json
from fastapi.responses import JSONResponse
import csv
import io
from ..oauth2 import get_current_user
from typing import Optional , List
import httpx

from ..crud.template import send_template_to_whatsapp

# Replace with your actual WhatsApp Business API endpoint and token


router=APIRouter( tags=['Broadcast'])

# access_token = "EAAXZCr1Or3lkBO9B0ZA84JDwoXgYd2BFqYA0Vn6BU2ZBk31OFEy3RPOwn68HWkabINs8y7OF2D2iDT5Uf8wwhcL51jlGANLZBUpGl26ezAAUM4f7pa3a80GUHVGQrP3n1z9dOGi54tZC3bXuK6kGcCsregUdZCl0y6c2oeBgRlw2ZBkSJFZCKuAtmbz1N9lk3uyZA5ZAU1KzXN1KZCeh1UJRgZDZD"
# BUSINESS_ACCOUNT_ID = '362091573648558'


# Broadcast 2 routes

@router.post("/send-template-message/")
async def send_template_message(request:broadcast.input,get_current_user: user.newuser=Depends(get_current_user)):
    print(request)
    API_url=f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {get_current_user.PAccessToken}",
        "Content-Type": "application/json"
    }

    success_count = 0
    errors = []

    for recipient in request.recipients:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type":"template",
            "template": {
                "name": request.template,
                "language": {
                    "code": "en_US"
                }
            }
        }

        response = requests.post(API_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            success_count += 1
        else:
            errors.append({"recipient": recipient, "error": response.json()})
    
    
    return {
        "status": "completed",
        "successful_messages": success_count,
        "errors": errors
    }





@router.get("/templates")
def get_templates(get_current_user: user.newuser=Depends(get_current_user)):

    API_URL = f'https://graph.facebook.com/v15.0/{get_current_user.WABAID}/message_templates'
    headers = {
        'Authorization': f'Bearer {get_current_user.PAccessToken}'
    }

    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

  

    # Extract template names
    template_names = [template['name'] for template in data.get('data', [])]

    

    return JSONResponse(content=template_names)


# route for fetchlist in Template management



@router.post("/broadcast")
def broadcastList(request:broadcast.BroadcastListCreate,db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    broadcastList=Broadcast.BroadcastList(
        user_id=get_current_user.id,
        name=request.name,
        template=request.template,
        contacts=request.contacts,
        success=request.success,
        failed=request.failed,
        status=request.status
    )
    db.add(broadcastList)
    db.commit()
    db.refresh(broadcastList)
    return("logged")

   


@router.get('/broadcast')
def fetchbroadcastList(skip: int = 0, limit: int = 10, tag: str = None, db: Session = Depends(database.get_db),
                      get_current_user: user.newuser=Depends(get_current_user) ):
    broadcastList=db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.user_id==get_current_user.id).order_by(Broadcast.BroadcastList.id.desc()).all()
    return broadcastList



@router.post("/import-contacts")
def import_contacts(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    contents = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(contents))

    contacts = []
    for row in reader:
        contact = Contacts.Contact(name=row['name'], phone=row['phone'])
        contacts.append(contact)
       

    return {"contacts": contacts}
   
# Broadcast 1 routes

@router.get("/template")
def get_templates( get_current_user: user.newuser=Depends(get_current_user)):

    API_URL = f'https://graph.facebook.com/v15.0/{get_current_user.WABAID}/message_templates'
    headers = {
        'Authorization': f'Bearer {get_current_user.PAccessToken}'
    }

    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    return data




# class Button(BaseModel):
#     type: str
#     text: str
#     phone_number: Optional[str] = None
#     url: Optional[str] = None

# class Component(BaseModel):
#     type: str
#     text: Optional[str] = None
#     format: Optional[str] = None
#     example: Optional[dict] = None
#     buttons: Optional[List[Button]] = None

# class CreateTemplateRequest(BaseModel):
#     name: str
#     category: str
#     allow_category_change: Optional[bool] = None
#     language: str
#     components: List[Component]

# class CreateTemplateResponse(BaseModel):
#     id: str
#     status: str
#     category: str




# @router.post("/create-template/", response_model=CreateTemplateResponse)
# async def create_template(request: CreateTemplateRequest , get_current_user: user.newuser=Depends(get_current_user) ):
#     API_URL = f"https://graph.facebook.com/v20.0/{get_current_user.WABAID}/message_templates" 
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             API_URL,
#             headers={
#                 "Authorization": f"Bearer {get_current_user.PAccessToken}",
#                 "Content-Type": "application/json"
#             },
#             json=request.dict()
#         )

#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise HTTPException(status_code=response.status_code, detail=response.text)








@router.post("/create-template", response_model=broadcast.TemplateResponse)
async def create_template(template: broadcast.TemplateCreate , request : Request , get_current_user: user.newuser=Depends(get_current_user)):
    try:
        template = await request.json()
        broadcast.TemplateCreate.validate_template(template)

        response = await send_template_to_whatsapp(template , get_current_user.PAccessToken , get_current_user.WABAID )
        return response
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.get("/create-template")
async def trial() :
    return "Create Template"















