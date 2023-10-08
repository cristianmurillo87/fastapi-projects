from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.auth.oauth2 import create_access_token
from app.database.database import get_db
from app.database.hashing import Hash
from app.database.user import User

router = APIRouter(tags=["authentication"])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    token_data = dict(username=user.username)
    access_token = create_access_token(token_data)
    return dict(
        access_token=access_token, token_type="bearer", user_id=user.id, username=user.username
    )
