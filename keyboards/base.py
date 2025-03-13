from keyboards.utils import InlineKBuilder, inline_keyboard, inline_kbuild
from keyboards.utils import reply_keyboard
from keyboards import buttons


BASE = reply_keyboard(buttons.MENU)
MENU = inline_keyboard(*buttons.Menu.all(), adjust=2)
CANCEL = inline_keyboard(buttons.CANCEL)


@inline_kbuild()
def confirm_or_cancel(*data: str, sep: str = '_', builder: InlineKBuilder):
    postfix = sep + sep.join(data)
    builder.button(text=buttons.CANCEL, callback_data=buttons.CANCEL + postfix)
    builder.button(text=buttons.CONFIRM, callback_data=buttons.CONFIRM + postfix)
