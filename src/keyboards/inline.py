from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class WahlAction(CallbackData, prefix="trn"):
    action: str


class Sset_Add(CallbackData, prefix="set"):
    set_action: str
    set_id: str
    repetitions: int


def traning_frage(training):
    actions = {
        'arme': training.arme,
        'rucken': training.rucken,
        'bauch': training.bauch,
        'beine': training.beine,
        'brust': training.brust
    }

    builder = InlineKeyboardBuilder()
    for action, value in actions.items():
        icon = '✅' if value else '❌'
        builder.button(
            text=f'{icon} {action.title()}', callback_data=WahlAction(action=f'{action}')
        )
    builder.button(
        text="Bestätigen", callback_data=WahlAction(action="confirm")
    )
    builder.adjust(5)
    return builder.as_markup()


def sset_create(user_training_data, set_id, repetitions):
    builder = InlineKeyboardBuilder()
    attributes = ['arme', 'rucken', 'bauch', 'beine', 'brust']
    for attribute in attributes:
        if getattr(user_training_data, attribute):
            builder.button(text=f'{attribute.capitalize()}', callback_data=Sset_Add(set_action=f'{attribute}_sets', set_id=set_id, repetitions=repetitions))
    return builder.as_markup()


einstellungen = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚙️ Einstellungen", callback_data='einstellungen')
        ]
    ]
)


einstellungen_frage = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ja", callback_data='einstell_yes')
        ],
        [
            InlineKeyboardButton(text="Nein", callback_data='einstell_no')
        ]
    ])