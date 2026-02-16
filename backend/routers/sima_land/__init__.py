from fastapi import APIRouter

from .loader import router as loader_router
from .search import router as search_router
from .ai_generate import router as ai_router
from .getters import router as getters_router
from .edit import router as edit_router

router = APIRouter(tags=["sima-land"])

router.include_router(loader_router)
router.include_router(search_router)
router.include_router(ai_router)
router.include_router(getters_router)
router.include_router(edit_router)