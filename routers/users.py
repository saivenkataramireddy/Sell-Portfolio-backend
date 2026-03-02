from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from datetime import timedelta
import shutil
import os
import uuid
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/login")
async def login(admin_data: schemas.AdminLogin, db: Session = Depends(get_db)):

    print("Incoming email:", admin_data.email)
    print("Incoming password:", admin_data.password)

    admin = db.query(models.Admin).filter(
        models.Admin.email == admin_data.email
    ).first()

    print("Admin found:", admin)

    if admin:
        print("Stored hash:", admin.hashed_password)
        result = auth.verify_password(admin_data.password, admin.hashed_password)
        print("Verify result:", result)

    if not admin or not auth.verify_password(admin_data.password, admin.hashed_password):
        print("LOGIN FAILED")
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    print("LOGIN SUCCESS")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "email": admin.email}

@router.post("/forgot-password")
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == request.email).first()
    if not admin:
        # We return 200 even if email not found for security reasons
        return {"message": "If the email is registered, a password reset link will be sent."}
    
    # In a real app, generate a reset token and send an email
    # For now, we simulate the logic
    return {"message": "Password reset functionality is prepared. Check server logs for simulation."}

@router.post("/reset-password")
async def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    # Verify token logic would go here
    # For now, just update the password for the specific admin (simulation)
    # This needs a real token verification system to be secure
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Password reset verification not fully implemented.")

@router.get("/me", response_model=schemas.AdminSchema)
async def get_me(current_admin: models.Admin = Depends(auth.get_current_admin)):
    return current_admin

@router.post("/upload-profile-pic")
async def upload_profile_pic(
    file: UploadFile = File(...),
    current_admin: models.Admin = Depends(auth.get_current_admin)
):
    # Ensure static/uploads exists
    upload_dir = os.path.join("backend", "static", "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Return relative URL
    url = f"/static/uploads/{filename}"
    return {"url": url}

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin)
):
    # Ensure static/uploads exists
    upload_dir = os.path.join("backend", "static", "uploads")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    # Delete old resume if it exists
    if current_admin.resume_url:
        old_file_path = os.path.join("backend", current_admin.resume_url.lstrip("/"))
        if os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except Exception as e:
                print(f"Error deleting old resume: {e}")
        
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"resume_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Update admin record
    url = f"/static/uploads/{filename}"
    current_admin.resume_url = url
    db.commit()
    
    return {"url": url}

@router.put("/me", response_model=schemas.AdminSchema)
async def update_me(
    admin_update: schemas.AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(auth.get_current_admin)
):
    update_data = admin_update.dict(exclude_unset=True)
    
    # If email is being updated, check if it already exists
    if "email" in update_data and update_data["email"] != current_admin.email:
        existing = db.query(models.Admin).filter(models.Admin.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for key, value in update_data.items():
        setattr(current_admin, key, value)
    
    db.commit()
    db.refresh(current_admin)
    return current_admin
