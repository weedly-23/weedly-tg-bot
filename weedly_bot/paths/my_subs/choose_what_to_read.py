from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators

from weedly_bot.paths.my_subs.calldata import feeds_calldata


@dp.message_handler(text_contains='Читать подписки')
async def choose_source(message: types.Message):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[

            [InlineKeyboardButton(text='Выбрать один источник', callback_data='show_user_feeds')],
            [InlineKeyboardButton(text='Выбрать катеогорию', callback_data='read_category')],
            [InlineKeyboardButton(text='Читать все в одной ленте', callback_data='read_all')],
            [InlineKeyboardButton(text='< Назад', callback_data='back_to_start')],

        ]

    )
    await message.answer('Как читать?', reply_markup=kb)


@dp.callback_query_handler(text_contains='back_to_choosing_source')
async def choose_source_callback(call: types.CallbackQuery):

    kb = InlineKeyboardMarkup(
        inline_keyboard=[

            [InlineKeyboardButton(text='Выбрать один источник', callback_data='show_user_feeds')],
            [InlineKeyboardButton(text='Выбрать катеогорию', callback_data='read_category')],
            [InlineKeyboardButton(text='Читать все в одной ленте', callback_data='read_all')],
            [InlineKeyboardButton(text='< Назад', callback_data='back_to_start')]

        ]

    )
    await call.message.answer('Как читать?', reply_markup=kb)


@dp.callback_query_handler(text_contains='show_user_feeds')
async def what_to_read(call: types.CallbackQuery):
    current = 1
    if '#' in call.data:
        current = int(call.data.split('#')[1])

    all_sources = api_client.users.get_user_feeds(uid=call.from_user.id)
    kb_generator = generators.KeyboardGenerator()
    kb = kb_generator.generate_feeds(feeds=all_sources, current=current, feeds_calldata=feeds_calldata,
                                     data_for_return='back_to_choosing_source',
                                     data_for_pagination='show_user_feeds')
    await call.message.edit_text(text='Выбери источник:', reply_markup=kb)