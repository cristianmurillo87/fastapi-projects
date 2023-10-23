from typing import Annotated

from app.config.databases.mongodb import get_mongo_collection
from app.config.databases.postgres import get_db
from fastapi import Depends
from pymongo.collection import Collection
from sqlalchemy.orm import Session

db_dependency = Annotated[Session, Depends(get_db)]
mongo_dependency = Annotated[Collection, Depends(get_mongo_collection)]
