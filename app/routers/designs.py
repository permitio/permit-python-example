from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import authenticate, get_db
from app.permit.permit_dependencies import permit_authorize

from ..database import schemas, models, crud


router = APIRouter(
    prefix="/design",
    tags=["design"]
)

## Create Design ##

@router.post("", dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def create_design(design: schemas.DesignCreate, db: Session = Depends(get_db)):
    db_design= db.query(models.Design).filter(models.Design.user_email == design.user_email and models.Design.title == design.title).first()

    if db_design:
         raise HTTPException(status_code=400, detail="Design already Exists")

    created_design =  crud.create_design(db, design)

    return {
        "message": "Design created successfully",
        "design": created_design  # You can include the created design object if needed
    }

## Delete Design ##

@router.delete("/{design-id}", dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def delete_design(deleteDesign: schemas.DesignDelete, db: Session = Depends(get_db)):

    return crud.delete_design(db, deleteDesign)

## Edit Design ##
@router.patch("/{design-id}", dependencies=[Depends(authenticate), Depends(permit_authorize)])
async def edit_design(editDesign: schemas.DesignEdit, db: Session = Depends(get_db)):
    return crud.edit_design()


## View Design ##




