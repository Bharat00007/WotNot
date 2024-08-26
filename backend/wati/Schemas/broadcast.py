from pydantic import BaseModel, HttpUrl , Field
from typing import List, Optional



class input(BaseModel):
    recipients: list[str]
    template:str

class BroadcastListCreate(BaseModel): 
    name:str
    template:str
    contacts:list[str]
    success:int
    failed:int
    status:str


















class Button(BaseModel):
    type: str = Field(..., description="The type of the button, e.g., 'URL' or 'QUICK_REPLY'")
    text: str = Field(..., description="The text of the button")
    url: Optional[HttpUrl] = None

class Component(BaseModel):
    type: str
    format: Optional[str] = None  # Allowed only for certain component types
    text: Optional[str] = None
    buttons: Optional[List[Button]] = None  # Optional list of Button objects

    @classmethod
    def validate_component(cls, component: dict):
        # Ensure 'BODY' type component does not have 'format' field
        if component['type'] == 'BODY':
            component.pop('format', None)  # Remove the format field if it exists

        # Ensure 'BODY' type component has 'text' field
        if component['type'] == 'BODY' and not component.get('text'):
            raise ValueError("Component of type BODY must have 'text' field")

        # Validate buttons if present
        if component.get('buttons'):
            for button in component['buttons']:
                Button(**button)  # Validate using the Button model

class TemplateCreate(BaseModel):
    name: str
    category: str
    components: List[Component]
    language: str
    sub_category: Optional[str] = None

    @classmethod
    def validate_template(cls, template: dict):
        for component in template.get('components', []):
            Component.validate_component(component)

class TemplateResponse(BaseModel):
    id: str
    status: str
    category: str






