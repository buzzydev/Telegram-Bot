from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import add_products
from buttons import ctgs_for_add_prd, skip_kb

# -------------------------------------------------------------------
# 🔀 ROUTER SETUP (Mahsulotlar ruteri)
# -------------------------------------------------------------------
p_router = Router()


# -------------------------------------------------------------------
# 📌 FSM STATES (Mahsulot qo'shish bosqichlari)
# -------------------------------------------------------------------
class ProductState(StatesGroup):
    """Mahsulot qo'shish jarayonining holatlari."""
    category = State()     # Kategoriya tanlash
    name = State()         # Mahsulot nomi
    description = State()  # Mahsulot tavsifi
    price = State()        # Mahsulot narxi
    quantity = State()     # Mahsulot miqdori
    image = State()        # Mahsulot rasmi


# -------------------------------------------------------------------
# 🛠️ HANDLERS (Mahsulot qo'shish ishlovchilari)
# -------------------------------------------------------------------

@p_router.callback_query(F.data == "add_product")
async def add_product_start(callback: CallbackQuery, state: FSMContext):
    """
    🛍️ 'Mahsulot qo'shish' tugmasi bosilganda jarayonni boshlaydi
    va kategoriyalar ro'yxatini chiqaradi.
    """
    await callback.answer()
    await state.clear()
    await callback.message.answer("📂 Qaysi kategoriyaga mahsulot qo'shmoqchisiz?", reply_markup=ctgs_for_add_prd())
    await state.set_state(ProductState.category)


@p_router.callback_query(ProductState.category)
async def select_category(callback: CallbackQuery, state: FSMContext):
    """
    📂 Tanlangan kategoriyaning ID sini ajratib oladi va mahsulot nomini so'raydi.
    """
    await callback.answer()
    data = callback.data
    
    # Callback ma'lumotidan kategoriya ID sini ajratib olish (masalan "ctg_5" -> 5)
    category_id = int(data.split('_')[-1]) if '_' in data else int(data)
    
    await state.update_data(category=category_id)
    await callback.message.delete()

    await callback.message.answer("📦 Mahsulot nomini kiriting:")
    await state.set_state(ProductState.name)


@p_router.message(ProductState.name)
async def get_name(message: Message, state: FSMContext):
    """
    📝 Mahsulot nomini qabul qiladi va tavsif kiritishni so'raydi.
    """
    text = message.text.strip()

    if len(text) < 3:
        return await message.answer("❌ Mahsulot nomini to'liqroq kiriting (kamida 3 belgi):")

    await state.update_data(name=text)
    xabar = """📝 Mahsulot tavsifini kiriting (Agarda hohlasangiz "skip" yoki "⏭ skip" yozing):"""
    await message.answer(xabar, reply_markup=skip_kb)
    await state.set_state(ProductState.description)


@p_router.message(ProductState.description)
async def get_description(message: Message, state: FSMContext):
    """
    📄 Mahsulot tavsifini qabul qiladi (yoki o'tkazib yuboradi) va narxini so'raydi.
    """
    text = message.text.strip()

    if len(text) < 3:
        return await message.answer("❌ Tavsifni to'liqroq kiriting (kamida 5 belgi):")
    if text.lower() in ["skip", "⏭ skip"]:
        await state.update_data(description=None)
    else:
        await state.update_data(description=text)

    await message.answer("💰 Mahsulot narxini kiriting (faqat raqamda):")
    await state.set_state(ProductState.price)


@p_router.message(ProductState.price)
async def get_price(message: Message, state: FSMContext):
    """
    💰 Mahsulot narxini tekshirib qabul qiladi va miqdorini so'raydi.
    """
    text = message.text.strip()

    if not text.isdigit():
        return await message.answer("❌ Narx faqat musbat son bo'lishi kerak. Qayta kiriting:")

    await state.update_data(price=int(text))

    await message.answer("🔢 Mahsulot miqdorini (sonini) kiriting:")
    await state.set_state(ProductState.quantity)


@p_router.message(ProductState.quantity)
async def get_quantity(message: Message, state: FSMContext):
    """
    🔢 Mahsulot miqdorini tekshirib qabul qiladi va rasmini so'raydi.
    """
    text = message.text.strip()

    if not text.isdigit():
        return await message.answer("❌ Miqdor faqat raqam bo'lishi kerak. Qayta kiriting:")

    await state.update_data(quantity=int(text))

    await message.answer("🖼️ Mahsulot rasmini yuboring:")
    await state.set_state(ProductState.image)


@p_router.message(ProductState.image)
async def get_image(message: Message, state: FSMContext):
    text = message.text
    """
    🖼️ Mahsulot rasmini qabul qiladi (yoki o'tkazib yuboradi), 
    ma'lumotlarni bazaga saqlaydi va FSM holatini yakunlaydi.
    """
    if not message.photo:
        return await message.answer("❌ Iltimos, faqat rasm shaklida yuboring:")

    else:
        file_id = message.photo[-1].file_id
        await state.update_data(image=file_id)


    data = await state.get_data()
    
    add_products(
        name=data.get("name"),
        description=data.get("description"),
        category_id=data.get("category"),
        price=data.get("price"),
        quantity=data.get("quantity"),
        image=data.get("image")
    )

    await message.answer(f"✅ <b>{data.get('name')}</b> muvaffaqiyatli saqlandi!", parse_mode="HTML")
    await state.clear()