from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from user-api.routes import users
from common.middleware.auth_middleware import AuthMiddleware
from config.settings import JWT_SECRET_KEY
from common.auth.jwt import encode_access_token, decode_access_token

app = FastAPI()

# Add authentication middleware
app.add_middleware(AuthMiddleware)

app.include_router(users.router)

# Login route example
@app.post("/login")
async def login(email: str, password: str):
    user_id = await users.authenticate_user(email, password)
    if user_id:
        token = encode_access_token(user_id, role="user")  # Assuming 'user' role for now
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid credentials")
