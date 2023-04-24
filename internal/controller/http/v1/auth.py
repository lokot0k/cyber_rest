from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from internal.dto.user import UserFilter
from internal.service.user import UserService
from internal.usecase.auth.auth import oauth2_scheme, ALGORITHM, SECRET_KEY, \
    ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from internal.usecase.auth.model import TokenData, Token

router = APIRouter()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           user_service: UserService = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_filter = UserFilter(username=token_data.username)
    user = await user_service.find(user_filter)
    if len(user) == 0:
        raise credentials_exception
    return user[0]


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: UserService = Depends()
):
    user = await user_service.authenticate_user(form_data.username,
                                                form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
