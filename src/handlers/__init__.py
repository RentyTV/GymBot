from aiogram import Router


def setup_message_routers() -> Router:
    from . import start
    from . import admin
    from . import user

    router = Router()
    router.include_router(start.router)
    router.include_router(admin.router)
    router.include_router(user.router)
    return router