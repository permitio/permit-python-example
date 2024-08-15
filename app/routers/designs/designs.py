from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app import permit
from app.dependencies import DBSessionDep, authenticate
from app.permit.permit_api import permit
from app.database import  models, crud
from app.routers.designs.schemas import DesignCreate, DesignDelete, DesignDeleteResponse, DesignEdit, DesignEditResponse, DesignView


router = APIRouter(
    prefix="/design",
    tags=["design"]
)

RESOURCE_NAME = 'design'

## Create Design ##

@router.post("", dependencies=[Depends(authenticate)], response_model=DesignCreate)
async def create_design(design: DesignCreate, db: Any = DBSessionDep):

    allowed = await permit.check('m', 'create',RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_design= db.query(models.Design).filter(models.Design.user_email == design.user_email and models.Design.title == design.title).first()

    if db_design:
         raise HTTPException(status_code=400, detail="Design already Exists")

    created_design = await crud.create_design(db, design)

    return created_design

## Delete Design ##

@router.delete("/{design-id}", dependencies=[Depends(authenticate)], response_model=DesignDeleteResponse)
async def delete_design(deleteDesign: DesignDelete, db: Any = DBSessionDep):

    allowed = await permit.check('m', 'delete',RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    deleted_design_id: DesignDeleteResponse = await crud.delete_design(db, deleteDesign)
    return deleted_design_id

## Edit Design ##
@router.patch("/{design-id}", dependencies=[Depends(authenticate)], response_model=DesignEditResponse)
async def edit_design(editDesign: DesignEdit, db: Any= DBSessionDep):

    allowed = await permit.check('m', 'edit' ,RESOURCE_NAME)

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    edited_design_id =  await crud.edit_design()

    return edited_design_id


## View Design ##




