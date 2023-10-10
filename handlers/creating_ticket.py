from asyncio.streams import FlowControlMixin
from itertools import cycle

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    reply_keyboard_remove,
)

from services import jira_client, ticket_service
import services.template_service as tmplt_s
from main import default_keyboard

router = Router()


class TicketChoice(StatesGroup):
    choose_template_name = State()
    choose_title = State()
    insert_text = State()
    choose_org = State()


def template_name_keyboard(templates, page_num, page_size=4):
    pages = [templates[i : i + page_size] for i in range(0, len(templates), page_size)]
    pages = cycle(pages)
    page = [next(pages) for _ in range(page_num + 1)][-1]
    page = cycle(page)
    return cycleable_buttons(page)


def cycleable_buttons(l):
    kb = [
        [KeyboardButton(text=next(l)), KeyboardButton(text=next(l))],
        [KeyboardButton(text=next(l)), KeyboardButton(text=next(l))],
        [KeyboardButton(text="Отмена")],
        [KeyboardButton(text="Далее")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите шаблон"
    )


@router.message(F.text.lower() == "тикет")
async def cmd_template_name(msg: Message, state: FSMContext):
    print("I was here")
    await msg.answer(
        text="Choose temlate",
        reply_markup=template_name_keyboard(tmplt_s.template_names(), 0),
    )
    await state.update_data(page=1)
    await state.set_state(TicketChoice.choose_template_name)


@router.message(F.text.lower() == "отмена")
async def cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text="Отмена операции", reply_markup=default_keyboard())


@router.message(TicketChoice.choose_template_name, F.text.in_(tmplt_s.template_names()))
async def template_chosen(msg: Message, state: FSMContext):
    await state.set_state(TicketChoice.choose_title)
    await state.update_data(template_name=msg.text)
    text = next(filter(lambda row: row[2], tmplt_s.find_all()))[2]
    await msg.answer(text=f"Template text:\n\n{text}")
    await msg.answer(
        text="Enter title for the ticket", reply_markup=ReplyKeyboardRemove()
    )


@router.message(TicketChoice.choose_template_name, F.text.lower() == "далее")
async def next_templates(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(
        text="Choose template",
        reply_markup=template_name_keyboard(tmplt_s.template_names(), data["page"]),
    )
    await state.update_data(page=data["page"] + 1)


@router.message(TicketChoice.choose_template_name)
async def wrong_tempalate_name(msg: Message, state: State):
    await msg.answer(text="Don't know this template")


def org_buttons(org_names, page_num, page_size=4):
    pages = [org_names[i : i + page_size] for i in range(0, len(org_names), page_size)]
    pages = cycle(pages)
    page = [next(pages) for _ in range(page_num + 1)][-1]
    page = cycle(page)
    return cycleable_buttons(page)


@router.message(TicketChoice.choose_title)
async def choose_title(msg: Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await state.set_state(TicketChoice.choose_org)
    await state.update_data(page=1)
    await msg.answer(
        text="Choose organization",
        reply_markup=org_buttons(ticket_service.db_org_names(), 0),
    )


@router.message(TicketChoice.choose_org, F.text.lower() == "далее")
async def next_org(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(
        text="Choose organization",
        reply_markup=org_buttons(ticket_service.db_org_names(), data["page"]),
    )
    await state.update_data(page=data["page"] + 1)


@router.message(TicketChoice.choose_org, F.text.in_(ticket_service.db_org_names()))
async def org_chosen(msg: Message, state: FSMContext):
    await state.update_data(org=msg.text)
    await state.set_state(TicketChoice.insert_text)
    await msg.answer(text="Enter text", reply_markup=ReplyKeyboardRemove())


@router.message(TicketChoice.insert_text)
async def text_inserted(msg: Message, state: FSMContext):
    data = await state.get_data()
    organizations = jira_client.get_organizations()["values"]
    org_id = ticket_service.find_ord_by_name(data["org"])
    jira_resp = jira_client.create_ticket(data["title"], msg.text, int(org_id))
    print(jira_resp)
    if "key" in jira_resp:
        url = "https://starfish24.atlassian.net/browse/" + jira_resp["key"]
        await msg.answer(
            parse_mode=ParseMode.HTML,
            text=url,
            reply_markup=default_keyboard(),
        )
    else:
        await msg.answer(
            parse_mode=ParseMode.HTML,
            text="\n".join(jira_resp["errorMessages"]),
            reply_markup=default_keyboard(),
        )
    await state.clear()
