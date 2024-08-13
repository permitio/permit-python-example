from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from ..database import schemas, models, crud

from app.permit_dependency import check_feed_permission

router = APIRouter()

## Create Design ##

@router.post("/create-design")
async def create_design(design: schemas.DesignCreate, db: Session = Depends(get_db)):
    db_design= db.query(models.Design).filter(models.Design.user_email == design.user_email and models.Design.title == design.title).first()

    if db_design:
         raise HTTPException(status_code=400, detail="Design already Exists")

    return crud.create_design(db, design)

## Delete Design ##

@router.delete("/delete-design")
async def delete_design(deleteDesign: schemas.DesignDelete, db: Session = Depends(get_db)):

    return crud.delete_design(db, deleteDesign)

## Edit Design ##
@router.patch("/edit-design")
async def edit_design(editDesign: schemas.DesignEdit, db: Session = Depends(get_db)):
    return crud.edit_design()


## View Design ##




