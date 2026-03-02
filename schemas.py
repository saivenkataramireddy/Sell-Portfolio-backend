from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

# Admin Schemas
class AdminBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    profile_picture: Optional[str] = None

class AdminCreate(AdminBase):
    password: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    profile_picture: Optional[str] = None
    resume_url: Optional[str] = None
    email: Optional[EmailStr] = None

class AdminSchema(AdminBase):
    id: int
    class Config:
        from_attributes = True

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    level: int
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillSchema(SkillBase):
    id: int
    class Config:
        from_attributes = True

# Journey Schemas
class JourneyBase(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class JourneyCreate(JourneyBase):
    pass

class JourneySchema(JourneyBase):
    id: int
    class Config:
        from_attributes = True

# Certification Schemas
class CertificationBase(BaseModel):
    name: str
    issuer: Optional[str] = None
    date: Optional[date] = None
    link: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationSchema(CertificationBase):
    id: int
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    link: Optional[str] = None
    image_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectSchema(ProjectBase):
    id: int
    class Config:
        from_attributes = True

# Contact Schemas
class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessageSchema(ContactMessageBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# Password Reset
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
