from . import adding_event
from . import base
from . import registering
from . import events_list
from . import reports

from aiogram import Router


router = Router()

router.include_routers(
    base.router,
    adding_event.router,
    registering.router,
    events_list.router,
    reports.router,
)