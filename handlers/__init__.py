from aiogram import Router
from .start import router as start_router
from .getlink import router as getlink_router
from .revoke import router as revoke_router
from .mylink import router as mylink_router
from .help import router as help_router
from .stats import router as stats_router
from .anon_message import router as anon_message_router
from .reply import router as reply_router
from .chat import router as chat_router  # Новый роутер

router = Router()
router.include_routers(
    start_router,
    getlink_router,
    revoke_router,
    mylink_router,
    help_router,
    stats_router,
    anon_message_router,
    reply_router,
    chat_router,
)

__all__ = ["router"]
