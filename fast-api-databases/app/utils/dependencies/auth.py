from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

auth_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
