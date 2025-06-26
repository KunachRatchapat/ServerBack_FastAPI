from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from sqlmodel import select, Session
from db.models import favorite_model
from db.database import get_session



