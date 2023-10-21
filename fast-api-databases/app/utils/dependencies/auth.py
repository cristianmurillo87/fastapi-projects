from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

auth_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
auth_token_dependency = Annotated[str, Depends(_oauth2_bearer)]
