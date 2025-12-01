import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.teacher_profile import TeacherProfile
from app.models.user import User
from app.schemas.teacher_profile import TeacherProfileResponse

router = APIRouter()
