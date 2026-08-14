from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import add_channel, get_one_channel_by_telegram_id


# -------------------------------------------------------------------
# 📌 FSM STATES
# -------------------------------------------------------------------
class ChannelManagementStates(StatesGroup):
    waiting_for_channel_name = State()
    waiting_for_channel_id = State()
    waiting_for_channel_url = State()


# -------------------------------------------------------------------
# 🔀 ROUTER SETUP
# -------------------------------------------------------------------
channel_management_router = Router()


# -------------------------------------------------------------------
# 🛠️ HANDLERS
# -------------------------------------------------------------------

@channel_management_router.callback_query(F.data == "admin:add_channel")
async def start_add_channel_process(callback: CallbackQuery, state: FSMContext) -> None:
    """➕ Yangi kanal qo'shish jarayonini boshlaydi."""
    await callback.answer("📢 Kanal qo'shish jarayoni boshlandi.")
    await state.clear()

    await callback.message.answer(
        "📝 <b>Yangi kanal qo'shish</b>\n\n"
        "Kanal nomini kiriting:",
        parse_mode="HTML"
    )

    await state.set_state(ChannelManagementStates.waiting_for_channel_name)


@channel_management_router.message(ChannelManagementStates.waiting_for_channel_name)
async def process_channel_name(message: Message, state: FSMContext) -> None:
    """📥 Kanal nomini qabul qiladi."""

    channel_name = message.text.strip()

    if not channel_name:
        return await message.answer(
            "⚠️ <b>Kanal nomi bo'sh bo'lishi mumkin emas!</b>\n"
            "🔄 Qaytadan kiriting:",
            parse_mode="HTML"
        )

    await state.update_data(channel_name=channel_name)

    await message.answer(
        "🆔 <b>Kanal ID sini kiriting:</b>\n"
        "Masalan: <code>-1001234567890</code>",
        parse_mode="HTML"
    )

    await state.set_state(ChannelManagementStates.waiting_for_channel_id)


@channel_management_router.message(ChannelManagementStates.waiting_for_channel_id)
async def process_channel_id(message: Message, state: FSMContext) -> None:
    """📥 Kanal ID sini qabul qiladi."""

    channel_id = message.text.strip()

    if not channel_id.startswith("-100"):
        return await message.answer(
            "⚠️ <b>Noto'g'ri kanal ID!</b>\n"
            "🔄 Qaytadan kiriting:",
            parse_mode="HTML"
        )

    if get_one_channel_by_telegram_id(channel_id):
        await state.clear()
        return await message.answer(
            "⚠️ Bu kanal allaqachon bazaga qo'shilgan."
        )

    await state.update_data(channel_id=channel_id)

    await message.answer(
        "🔗 <b>Kanal havolasini kiriting:</b>\n"
        "Masalan: <code>https://t.me/BuzzyMedia</code>",
        parse_mode="HTML"
    )

    await state.set_state(ChannelManagementStates.waiting_for_channel_url)


@channel_management_router.message(ChannelManagementStates.waiting_for_channel_url)
async def process_channel_url(message: Message, state: FSMContext) -> None:
    """📥 Kanal havolasini qabul qiladi va bazaga saqlaydi."""

    channel_url = message.text.strip()

    if not channel_url.startswith("https://t.me/"):
        return await message.answer(
            "⚠️ <b>Noto'g'ri kanal havolasi!</b>\n"
            "🔄 Qaytadan kiriting:",
            parse_mode="HTML"
        )

    data = await state.get_data()

    add_channel(
        data["channel_name"],
        data["channel_id"],
        channel_url
    )

    await message.answer(
        "✅ <b>Kanal muvaffaqiyatli qo'shildi!</b>\n\n"
        f"📢 Kanal: <b>{data['channel_name']}</b>\n"
        f"🆔 ID: <code>{data['channel_id']}</code>\n"
        f"🔗 Havola: {channel_url}",
        parse_mode="HTML"
    )

    await state.clear()