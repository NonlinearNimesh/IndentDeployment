from sqlalchemy.orm import Session
from models import models
from schema import schema

def add_details_to_db(db: Session, users: schema.DetailsBase):
    mv_details = models.Users(
        name=users.name,
        username=users.username,
        password=users.password,
        email=users.email,
        role=users.role,
        secret_key=users.secret_key,
        key_expires=users.key_expires,
        created_on=users.created_on,
    )
    db.add(mv_details)
    db.commit()
    return models.Users(**users.dict())