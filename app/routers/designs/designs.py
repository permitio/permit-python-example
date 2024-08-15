from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from app import permit
from app.database.database import get_db_session
from app.dependencies import authenticate
from app.permit.permit_api import permit
from app.database import crud
from app.routers.designs.schemas import DesignCreate, DesignDelete, DesignDeleteResponse, DesignEdit, DesignEditResponse, DesignView
from app.database.models import Design


router = APIRouter(
    prefix="/design",
    tags=["design"]
)

RESOURCE_NAME = 'design'

## Create Design ##

@router.post("", dependencies=[Depends(authenticate)], response_model=DesignCreate)
async def create_design(design: DesignCreate, db_session = Depends(get_db_session)):

    allowed = await permit.check(design.user_email, 'create',RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_design = (await db_session.execute(
    select(Design).where(
        Design.user_email == design.user_email,
        Design.title == design.title
    ))).scalars().first()

    if db_design:
         raise HTTPException(status_code=400, detail="Design already Exists")

    created_design: Design = await crud.create_design(db_session, design)

    await permit.api.create_resource()

    design_response = DesignCreate(
            user_email = created_design.user_email,
            title =  created_design.title,
            description = created_design.description
       )
    

    return design_response

## Delete Design ##

@router.delete("/{design-id}", response_model=DesignDeleteResponse)
async def delete_design(deleteDesign: DesignDelete, user=Depends(authenticate), db_session = Depends(get_db_session)):
    allowed = await permit.check(user, 'delete',RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    deleted_design_id: DesignDeleteResponse = await crud.delete_design(db_session, deleteDesign)
    return deleted_design_id

## Edit Design ##
@router.patch("/{design-id}", dependencies=[Depends(authenticate)], response_model=DesignEditResponse)
async def edit_design(editDesign: DesignEdit,user=Depends(authenticate), db_session = Depends(get_db_session)):

    allowed = await permit.check(user, 'edit' ,RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    edited_design_id =  await crud.edit_design()

    return edited_design_id






