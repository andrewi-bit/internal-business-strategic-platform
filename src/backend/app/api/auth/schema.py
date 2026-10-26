from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class RegisterResponse(BaseModel):
    message: str
    email: EmailStr

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    otp: str = Field(pattern=r"^\d{6}$")

class VerifyEmailResponse(BaseModel):
    message: str
    email: EmailStr

class ResendOTPRequest(BaseModel):
    email: EmailStr

class ResendOTPResponse(BaseModel):
    message: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role_id: str | None = None
    role_name: str | None = None
    role_code: str | None = None

class CurrentUserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role_id: str | None = None
    role_name: str | None = None
    role_code: str | None = None
    is_active: bool

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str

class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=8, max_length=128)

class ResetPasswordResponse(BaseModel):
    message: str

