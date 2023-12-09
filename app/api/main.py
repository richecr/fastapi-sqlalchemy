from fastapi import APIRouter

from .notes.views import router as notes_router

router = APIRouter()
router.include_router(notes_router)
