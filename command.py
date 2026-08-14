from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import bot, GROUP_ID, CHANNEL_ID, LEFT_STATUS

from add_channel import ChannelManagementStates

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# -------------------------------------------------------------------
# 🗺️ GEOLOKATSIYA SOZLAMALARI
# -------------------------------------------------------------------
geo = Nominatim(user_agent="myGeocoder")
distance = geodesic

from add_admin import AdminManagementStates
from add_category import CategoryManagementStates
from register_user import RegisterState
from database import (
    check_admin,
    delete_channel,
    get_all_cart_items_by_id,   
    check_cart, 
    get_one_channel,
    check_user,
    clear_user_cart, 
    delete_products, 
    get_all_admins, 
    get_all_users_id,
    get_cart_item_price_by_product_id,
    get_cart_item_quantity_by_product_id,
    get_one_cart_item_by_id, 
    get_one_category, 
    deletes_category, 
    get_one_admin, 
    delete_admin, 
    get_one_product,
    add_cart_item,
    update_cart_price_by_product_id,
    update_cart_quantity_by_product_id,
    delete_cart_item_by,
    delete_cart_item_by_id,
    add_users
)

from buttons import (
    approve_button,
    delivery_type_inline_keyboard,
    user_start_keyboard,
    phone_request_keyboard,
    back_keyboard,
    get_admin_channel_action_keyboard,
    get_user_categories_keyboard,
    get_user_category_products_keyboard,
    get_user_product_action_keyboard,
    get_user_cart_items_keyboard,
    admin_start_keyboard,
    admin_menu_keyboard,
    admin_product_keyboard,
    admin_category_keyboard,
    admin_users_keyboard,
    get_admin_categories_keyboard,
    get_admin_category_products_keyboard,
    get_admin_all_products_keyboard,
    get_admin_list_keyboard,
    get_admin_category_action_keyboard,
    get_admin_product_action_keyboard,
    get_admin_user_action_keyboard,
    location_request_keyboard,
    channel_button,
    channel_menu_keyboard,
    get_admin_channels_keyboard
)

# -------------------------------------------------------------------
# 🔀 ROUTER WA FSM STATE SOZLAMALARI
# -------------------------------------------------------------------
s_router = Router()


class MessageState(StatesGroup):
    """Barcha foydalanuvchilarga xabar (reklama) yuborish holati."""
    message = State()
class User_Location_State(StatesGroup):
    location = State()

# ====================================================================
# 1. KANALGA OBUNA
# ====================================================================

# @s_router.message(Command('start'))
# async def start_command(message: Message):
#     user_id = message.from_user.id
#     check_subs = await bot.get_chat_member(CHANNEL_ID, user_id)
#     xabar = (
# "⚠️ <b>Majburiy obuna!</b>\n\n"
# "🔔 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘lishingiz kerak.\n\n"
# "📢 <b>Kanallarga obuna bo‘ling</b> va so‘ngra "
# "✅ <b>«Tekshirish»</b> tugmasini bosing.\n\n"
# "💡 Obuna bo‘lganingizdan keyin botdan to‘liq foydalanishingiz mumkin!"
#     )
#     if check_subs.status in LEFT_STATUS:
#         await message.answer(xabar, reply_markup=channel_button(), parse_mode="HTML")
#     else:
#         xabar_2 = (
# "👋 <b>Assalomu alaykum!</b>\n\n"
# "🤖 <b>BuzzyDev Bot</b> ga xush kelibsiz!\n\n"
# "✨ Sizning obunangiz muvaffaqiyatli tasdiqlandi.\n"
# "🚀 Endi botimizdan to‘liq foydalanishingiz mumkin.\n\n"
# "📌 Kerakli bo‘limni tanlash uchun quyidagi menyudan foydalaning.\n\n"
# "💙 <b>Yoqimli foydalanish tilaymiz!</b>"
#     )
#     await message.delete()

#     await message.answer(xabar_2, reply_markup=user_start_keyboard, parse_mode="HTML")
# @s_router.callback_query(F.data == "check_subs")
# async def check_subs_cmd(callback: CallbackQuery):
    
#     user_id = callback.from_user.id
#     check_subs = await bot.get_chat_member(CHANNEL_ID, user_id)
#     if check_subs.status in LEFT_STATUS:
#         xabar = (
#         "⚠️ <b>Siz hali ham kanalga obuna bo‘lmagansiz!</b>\n\n"
#         "📢 Iltimos, kanalga obuna bo‘ling va\n"    
#         "🔄 <b>«Tekshirish»</b> tugmasini bosing.\n\n"
#         "✅ Obuna bo‘lganingizdan so‘ng botdan foydalanishingiz mumkin!"
#         )
#         await callback.message.answer(xabar, reply_markup=channel_button(), parse_mode="HTML")
#     xabar_2 = (
# "👋 <b>Assalomu alaykum!</b>\n\n"
# "🤖 <b>BuzzyDev Bot</b> ga xush kelibsiz!\n\n"
# "✨ Sizning obunangiz muvaffaqiyatli tasdiqlandi.\n"
# "🚀 Endi botimizdan to‘liq foydalanishingiz mumkin.\n\n"
# "📌 Kerakli bo‘limni tanlash uchun quyidagi menyudan foydalaning.\n\n"
# "💙 <b>Yoqimli foydalanish tilaymiz!</b>"
#     )
#     await callback.message.answer(xabar_2, reply_markup=user_start_keyboard, parse_mode="HTML")

async def get_unsubscribed_channels(user_id: int):
    """
    📢 Foydalanuvchining majburiy kanallarga obuna bo'lmaganlarini aniqlaydi.
    """
    obuna_bolmagan_kanallar = []

    for channel_id in CHANNEL_ID:
        check_subs = await bot.get_chat_member(channel_id, user_id)

        if check_subs.status in LEFT_STATUS:
            obuna_bolmagan_kanallar.append(channel_id)

    return obuna_bolmagan_kanallar

@s_router.message(Command('start'))
async def start_command(message: Message):
    obuna_bolmagan_kanallar = []
    user_id = message.from_user.id
    user = check_user(user_id)

    # Foydalanuvchi allaqachon mavjud bo'lsa
    if user is None:
        name = message.from_user.full_name
        username = message.from_user.username
        id = message.from_user.id
        add_users(name, username, id)   

    for i in CHANNEL_ID:
        check_subs = await bot.get_chat_member(i, user_id)
        if check_subs.status in LEFT_STATUS:
            obuna_bolmagan_kanallar.append(i)
        else:
            continue
    if not obuna_bolmagan_kanallar:
        xabar_2 = (
    "👋 <b>Assalomu alaykum!</b>\n\n"
    "🤖 <b>BuzzyDev Bot</b> ga xush kelibsiz!\n\n"
    "✨ Sizning obunangiz muvaffaqiyatli tasdiqlandi.\n"
    "🚀 Endi botimizdan to‘liq foydalanishingiz mumkin.\n\n"
    "📌 Kerakli bo‘limni tanlash uchun quyidagi menyudan foydalaning.\n\n"
    "💙 <b>Yoqimli foydalanish tilaymiz!</b>"
        )
        return await message.answer(xabar_2, reply_markup=user_start_keyboard, parse_mode="HTML")
    else:
        xabar = (
        "⚠️ <b>Siz hali ham kanalga obuna bo‘lmagansiz!</b>\n\n"
        "📢 Iltimos, kanalga obuna bo‘ling.\n"
        "🔄 Obuna bo‘lganingizdan so‘ng <b>«Tekshirish»</b> tugmasini bosing.\n\n"
        "❗️ Botdan foydalanish uchun kanalga obuna bo‘lish majburiy."
        )
        
        await message.answer(xabar, reply_markup=channel_button(obuna_bolmagan_kanallar), parse_mode="HTML")
@s_router.callback_query(F.data == "check_subs")
async def check_subs_cmd(callback: CallbackQuery):
    
    user_id = callback.from_user.id
    obuna_bolmgan_kanallar = []
    for i in CHANNEL_ID:
        check_subs = await bot.get_chat_member(i, user_id)
        if check_subs.status in LEFT_STATUS:
            obuna_bolmgan_kanallar.append(i)
        else:
            continue
    if not obuna_bolmgan_kanallar:
        xabar_2 = (
    "👋 <b>Assalomu alaykum!</b>\n\n"
    "🤖 <b>BuzzyDev Bot</b> ga xush kelibsiz!\n\n"
    "✨ Sizning obunangiz muvaffaqiyatli tasdiqlandi.\n"
    "🚀 Endi botimizdan to‘liq foydalanishingiz mumkin.\n\n"
    "📌 Kerakli bo‘limni tanlash uchun quyidagi menyudan foydalaning.\n\n"
    "💙 <b>Yoqimli foydalanish tilaymiz!</b>"
        )
        return await callback.message.answer(xabar_2, reply_markup=user_start_keyboard, parse_mode="HTML")
    xabar = (
        "⚠️ <b>Siz hali ham kanalga obuna bo‘lmagansiz!</b>\n\n"
        "📢 Iltimos, kanalga obuna bo‘ling.\n"
        "🔄 Obuna bo‘lganingizdan so‘ng <b>«Tekshirish»</b> tugmasini bosing.\n\n"
        "❗️ Botdan foydalanish uchun kanalga obuna bo‘lish majburiy."
    )
    await callback.message.delete()
    await callback.message.answer(xabar, reply_markup=channel_button(obuna_bolmgan_kanallar), parse_mode="HTML")


# ====================================================================
# 1. 👤 USER HANDLERS (FOYDALANUVCHI AMALLARI)
# ====================================================================

@s_router.message(User_Location_State.location)
async def location_handler(message: Message, state: FSMContext):
    """
    📍 Foydalanuvchi yuborgan geolokatsiyani qabul qiladi va 
    manzil haqida batafsil ma'lumot qaytaradi.
    """
    
    if not message.location:
        return await message.answer(
            "Iltimos Lakatsiya yuboring."
        )

    user_location = (message.location.latitude, message.location.longitude)
    location = geo.reverse(user_location, language="uz")
    
    if location:
        data = location.raw.get("address", {})

        country = data.get("country")
        address_state = data.get("state")
        city = data.get("city") or data.get("town") or data.get("village")
        district = data.get("county") or data.get("district")
        road = data.get("road")

        text = f"""
🌍 Davlat: {country}
🏙 Viloyat: {address_state}
🏘 Tuman: {district}
🏠 Shahar/Qishloq: {city}
🛣 Ko'cha: {road}
        """
        
        await message.answer(
            text
        )
    user_orders = get_all_cart_items_by_id(message.from_user.id)
    orders_text = "Foydalanuvchining buyurtmalari\n\n"
    for i in user_orders:
        product = get_one_product(i[2])
        order_id = i[0]
        orders_text += product[1]
        orders_text += f"\n{i[4]} x {product[4]} = {i[3]}"
        orders_text += "\n___________________________\n"
    await bot.send_message(
        GROUP_ID, orders_text
    )
    await bot.send_location(
        chat_id=GROUP_ID,
        latitude=message.location.latitude,
        longitude=message.location.longitude, reply_markup=approve_button(order_id)
    )
    await bot.send_message(
        GROUP_ID, text
    )
    await message.answer(
        "Buyurtmangiz qabul qildindi\nTez orada bog'lanamiz!"
    )
    await state.clear()

@s_router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    """
    🚀 /start buyrug'i berilganda foydalanuvchini bazadan tekshiradi.
    Mavjud bo'lsa menyuni chiqaradi, bo'lmasa ro'yxatdan o'tkazishni boshlaydi.
    """
    user = check_user(message.from_user.id)

    if user:
        await state.clear()
        await message.answer(
            "👋 Assalomu alaykum! Xush kelibsiz!",
            reply_markup=user_start_keyboard
        )
    else:
        await state.clear()
        await state.set_state(RegisterState.ism)
        await message.answer("✍️ Ismingizni kiriting:")


# ============================================================
# ✅ BUYURTMANI TASDIQLASH
# ============================================================

@s_router.callback_query(F.data.startswith("approve:order:"))
async def approve_order(callback: CallbackQuery):
    """
    ✅ Admin buyurtmani tasdiqlaydi.
    Agar cart mavjud bo'lsa foydalanuvchiga xabar yuboradi.
    Agar mavjud bo'lmasa "Buyurtma mavjud emas" deydi.
    """

    order_id = int(callback.data.split(":")[2])

    # 🔍 Cart mavjudligini tekshirish
    order = get_one_cart_item_by_id(order_id)

    if not order:
        await callback.answer(
            "❌ Buyurtma mavjud emas!",
            show_alert=True
        )
        return

    # Cart ma'lumotlari
    user_id = order[1]
    product_id = order[2]
    quantity = order[4]

    # 📦 Mahsulotni olish
    product_info = get_one_product(product_id)

    if not product_info:
        await callback.answer(
            "❌ Mahsulot topilmadi!",
            show_alert=True
        )
        return

    # 👤 Foydalanuvchiga xabar
    await bot.send_message(
        user_id,
        f"✅ Buyurtmangiz tasdiqlandi!\n\n"
        f"📦 Mahsulot: {product_info[1]}\n"
        f"💰 Narxi: {product_info[4]} so'm\n"
        f"📦 Miqdori: {quantity} dona\n"
        f"📝 Tavsif: {product_info[2]}"
    )

    # 👨‍💼 Adminga xabar
    await callback.message.answer(
        "✅ Buyurtma tasdiqlandi va foydalanuvchiga xabar yuborildi."
    )

    # 🗑️ Cartdan o'chirish
    delete_cart_item_by(order_id)

    await callback.answer(
        "Buyurtma tasdiqlandi!"
    )


# ============================================================
# ❌ BUYURTMANI BEKOR QILISH
# ============================================================

@s_router.callback_query(F.data.startswith("cancel:order:"))
async def cancel_order(callback: CallbackQuery):
    """
    ❌ Admin buyurtmani bekor qiladi.
    Agar cart mavjud bo'lsa foydalanuvchiga xabar yuboradi.
    Agar mavjud bo'lmasa "Buyurtma mavjud emas" deydi.
    """

    order_id = int(callback.data.split(":")[2])

    # 🔍 Cart mavjudligini tekshirish
    order = get_one_cart_item_by_id(order_id)

    if not order:
        await callback.answer(
            "❌ Buyurtma mavjud emas!",
            show_alert=True
        )
        return

    # Cart ma'lumotlari
    user_id = order[1]
    product_id = order[2]
    quantity = order[4]

    # 📦 Mahsulotni olish
    product_info = get_one_product(product_id)

    if not product_info:
        await callback.answer(
            "❌ Mahsulot topilmadi!",
            show_alert=True
        )
        return

    # 👤 Foydalanuvchiga xabar
    await bot.send_message(
        user_id,
        f"❌ Buyurtmangiz bekor qilindi!\n\n"
        f"📦 Mahsulot: {product_info[1]}\n"
        f"💰 Narxi: {product_info[4]} so'm\n"
        f"📦 Miqdori: {quantity} dona\n"
        f"📝 Tavsif: {product_info[2]}"
    )

    # 👨‍💼 Adminga xabar
    await callback.message.answer(
        "❌ Buyurtma bekor qilindi va foydalanuvchiga xabar yuborildi."
    )

    # 🗑️ Cartdan o'chirish
    delete_cart_item_by(order_id)

    await callback.answer(
        "Buyurtma bekor qilindi!"
    )

@s_router.callback_query(F.data == "user:start_menu")
async def back_to_user_start_cmd(callback: CallbackQuery):
    """
    🏠 Foydalanuvchini asosiy menyuga qaytaradi.
    """
    await callback.message.delete()
    await callback.message.answer(
        "📂 Foydalanuvchilar menyusisiz:", 
        reply_markup=user_start_keyboard
    )
    await callback.answer()


@s_router.callback_query(F.data == "user:categories")
async def view_user_categories(callback: CallbackQuery):
    """
    📂 Foydalanuvchi uchun kategoriyalar ro'yxatini ko'rsatadi.
    """
    await callback.message.delete()
    await callback.message.answer(
        "📂 Kategoriyani tanlang:",
        reply_markup=get_user_categories_keyboard()
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("user:category:"))
async def view_category_products_for_user(callback: CallbackQuery):
    """
    📦 Tanlangan kategoriya ichidagi mahsulotlarni ko'rsatadi.
    """
    category_id = int(callback.data.split(":")[2])
    await callback.message.edit_text(
        "📦 Mahsulotni tanlang:",
        reply_markup=get_user_category_products_keyboard(category_id)
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("user:product:"))
async def view_one_product_user(callback: CallbackQuery):
    """
    🥤 Mahsulot haqida to'liq ma'lumot va rasmini chiqaradi.
    """
    product_id = int(callback.data.split(":")[2])
    product_info = get_one_product(product_id)

    rasm = product_info[6]

    xabar = (
        f"🥤 {product_info[1]}\n\n"
        f"💰 Narxi: {product_info[4]} so'm\n"
        f"📦 Mavjud: {product_info[5]} dona\n\n"
        f"📝 Tavsif:\n{product_info[2]}"
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=rasm,
        caption=xabar,
        reply_markup=get_user_product_action_keyboard(product_id)
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("user:add_to_cart:"))
async def add_to_cart_handler(callback: CallbackQuery):
    """
    🛒 Mahsulotni savatga qo'shadi yoki savatdagi miqdor va narxini oshiradi.
    """
    product_id = int(callback.data.split(":")[2])
    product_info = get_one_product(product_id)
    product = check_cart(product_id)
    if not product:
        add_cart_item(
            callback.from_user.id,
            product_id,
            product_info[4],
            1
        )
        await callback.answer(
            f"✅ {product_info[1]} savatga qo'shildi!", show_alert=True
        )
    else:
        old_count = get_cart_item_quantity_by_product_id(product_id)[0]
        new_count = old_count + 1

        old_price = get_cart_item_price_by_product_id(product_id)[0]
        product_price = get_one_product(product_id)[4]
        new_price = old_price + product_price

        update_cart_quantity_by_product_id(product_id, new_count)
        update_cart_price_by_product_id(product_id, new_price)
        await callback.answer(
            f"✅ {product_info[1]} savatga qo'shildi!", show_alert=True
        )


@s_router.callback_query(F.data.startswith("user:order"))
async def place_order(callback: CallbackQuery):
    """
    📦 Buyurtma berish usulini tanlash menyusini chiqaradi.
    """
    await callback.message.delete()
    await callback.message.answer(
        "📦 Buyurtma berish:",
        reply_markup=delivery_type_inline_keyboard()
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("order:delivery"))
async def place_delivery_order(callback: CallbackQuery, state: FSMContext):
    """
    🛵 Eltib berish tanlanganda geolokatsiya so'raydi.
    """
    await callback.message.delete()
    await callback.message.answer(
        "🛵 Locatsiya yuboring",
        reply_markup=location_request_keyboard
    )
    await callback.answer()
    await state.set_state(User_Location_State.location)


@s_router.callback_query(F.data == "user:cart")
async def view_cart_handler(callback: CallbackQuery):
    """
    🛒 Savatdagi barcha mahsulotlarni ko'rsatadi.
    """
    await callback.message.delete()
    await callback.message.answer(
        "🛒 Savatingizdagi mahsulotlar:",
        reply_markup=get_user_cart_items_keyboard(callback.from_user.id)
    )
    await callback.answer()

@s_router.callback_query(F.data.startswith("add:count:"))
async def increase_cart_item_quantity(callback: CallbackQuery):
    """
    ➕ Savatdagi mahsulot sonini 1 taga oshiradi.
    """
    cart_id = int(callback.data.split(":")[2])

    cart_item = get_one_cart_item_by_id(cart_id)

    product_id = cart_item[2]
    old_quantity = cart_item[4]
    old_price = cart_item[3]

    product_price = get_one_product(product_id)[4]

    new_quantity = old_quantity + 1
    new_price = old_price + product_price

    update_cart_price_by_product_id(product_id, new_price)
    update_cart_quantity_by_product_id(product_id, new_quantity)

    await callback.message.edit_reply_markup(
        reply_markup=get_user_cart_items_keyboard(
            callback.from_user.id
        )
    )

    await callback.answer("Mahsulot soni oshirildi ✅")

# @s_router.callback_query(F.data.startswith("user:add_to_cart:"))
# async def sub_count_product_quantity(callback: CallbackQuery):
#     product_id = int(callback.data.split(":")[2])
#     product_info = get_one_product(product_id)

#     old_quantity = product_info[5]


#     new_quantity = old_quantity - 1
#     update_product_quantity_by_id(new_quantity, product_id)


    # rasm = product_info[6]
    # xabar = (
    #     f"🥤 {product_info[1]}\n\n"
    #     f"💰 Narxi: {product_info[4]} so'm\n"
    #     f"📦 Mavjud: {product_info[5]} dona\n\n"
    #     f"📝 Tavsif:\n{product_info[2]}"
    # )

    # await callback.message.delete()
    # await callback.message.answer_photo(
    #     photo=rasm,
    #     caption=xabar,
    #     reply_markup=get_user_product_action_keyboard(product_id)
    # )
    # await callback.answer()
    

@s_router.callback_query(F.data.startswith("sub:count:"))
async def decrease_cart_item_quantity(callback: CallbackQuery):
    """
    ➖ Savatdagi mahsulot sonini 1 taga kamaytiradi (0 bo'lsa o'chiradi).
    """
    cart_id = int(callback.data.split(":")[2])

    cart_item = get_one_cart_item_by_id(cart_id)

    product_id = cart_item[2]
    old_quantity = cart_item[4]
    old_price = cart_item[3]

    product_price = get_one_product(product_id)[4]

    new_quantity = old_quantity - 1
    new_price = old_price - product_price

    if new_quantity < 1:
        delete_cart_item_by(cart_id)

        await callback.message.edit_reply_markup(
            reply_markup=get_user_cart_items_keyboard(
                callback.from_user.id
            )
        )

        await callback.answer(
            "❌ Mahsulot savatdan o'chirildi!"
        )
        return

    update_cart_price_by_product_id(
        product_id,
        new_price
    )

    update_cart_quantity_by_product_id(
        product_id,
        new_quantity
    )

    await callback.message.edit_reply_markup(
        reply_markup=get_user_cart_items_keyboard(
            callback.from_user.id
        )
    )

    await callback.answer("Mahsulot soni kamaytirildi ✅")


@s_router.callback_query(F.data == "user:clear_cart")
async def clear_cart(callback: CallbackQuery):
    """
    🗑️ Foydalanuvchining butun savatini tozalaydi.
    """
    user_id = callback.from_user.id

    clear_user_cart(user_id)

    await callback.message.edit_text(
        text="🗑️ Savatingiz tozalandi!",
        reply_markup=get_user_cart_items_keyboard(user_id)
    )

    await callback.answer(
        "Savat tozalandi ✅"
    )


# ====================================================================
# 2. 👨‍💼 ADMIN HANDLERS (ADMINISTRATOR AMALLARI)
# ====================================================================

@s_router.message(Command("admin"))
async def admin_cmd(message: Message):
    """
    ⚙️ Admin paneliga kirish uchun /admin buyrug'ini tekshirish.
    """
    user_id = message.from_user.id
    user = check_admin(user_id)
    if not user:
        await message.answer("⚠️ Siz admin emassiz!")
        return
    else:
        await message.answer(
            "⚙️ Siz admin menyusiga muvaffaqiyatli kirdingiz!", 
            reply_markup=admin_start_keyboard
        )


@s_router.callback_query(F.data == "admin:start_menu")
async def back_to_admin_start_cmd(callback: CallbackQuery):
    """
    ⚙️ Admin bosh menyusiga qaytaradi.
    """
    await callback.message.delete()
    await callback.message.answer(
        "⚙️ Admin bosh menyusi:", 
        reply_markup=admin_start_keyboard
    )
    await callback.answer()


# -------------------------------------------------------------------
# 📊 ADMIN MENYU TUGMALARI
# -------------------------------------------------------------------

@s_router.callback_query(F.data == "admin:menu:products")
async def product_menu_cmd(callback: CallbackQuery):
    """📦 Admin mahsulotlar menyusi."""
    await callback.message.edit_text(
        "📦 Mahsulotlar menyusi:", 
        reply_markup=admin_product_keyboard
    )
    await callback.answer()

@s_router.callback_query(F.data == "admin:add_channel")
async def product_menu_cmd(callback: CallbackQuery):
    """📦 Admin mahsulotlar menyusi."""
    await callback.message.edit_text(
        "🏞️ Kanallar menyusi:", 
        reply_markup=channel_menu_keyboard
    )
    await callback.answer()


@s_router.callback_query(F.data == "admin:menu:admins")
async def admin_menu_cmd(callback: CallbackQuery):
    """👥 Adminlar menyusi."""
    await callback.message.edit_text(
        "👥 Adminlar menyusi:", 
        reply_markup=admin_menu_keyboard
    )
    await callback.answer()


@s_router.callback_query(F.data == "admin:menu:categories")
async def category_menu_cmd(callback: CallbackQuery):
    """📂 Admin kategoriyalar menyusi."""
    await callback.message.edit_text(
        "📂 Kategoriyalar menyusi:", 
        reply_markup=admin_category_keyboard
    )
    await callback.answer()


@s_router.callback_query(F.data == "admin:menu:users")
async def users_menu_cmd(callback: CallbackQuery):
    """📊 Admin foydalanuvchilar menyusi."""
    await callback.message.edit_text(
        "📊 Foydalanuvchilar menyusi:", 
        reply_markup=admin_users_keyboard
    )
    await callback.answer()


# -------------------------------------------------------------------
# 📂 ADMIN KATEGORIYA AMALLARI
# -------------------------------------------------------------------

@s_router.callback_query(F.data == "admin:view_categories")
async def view_categories_admin(callback: CallbackQuery):
    """📂 Barcha kategoriyalarni admin ko'rinishida chiqaradi."""
    await callback.message.edit_text(
        "📂 Kategoriyani tanlang:",
        reply_markup=get_admin_categories_keyboard()
    )
    await callback.answer()

@s_router.callback_query(F.data == "add_category")
async def start_add_category_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(
        "📝 Yangi kategoriya nomini kiriting:"
    )

    await state.set_state(
        CategoryManagementStates.waiting_for_category_title
    )

@s_router.callback_query(F.data == "channel:view")
async def view_channels(callback: CallbackQuery):
    await callback.message.edit_text(
        "📢 Kanallar:",
        reply_markup=get_admin_channels_keyboard()
    )

    await callback.answer()

@s_router.callback_query(F.data == "admin:menu:channels")
async def admin_channels_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛹 <b>Kanallar Menyusi</b>",
        reply_markup=channel_menu_keyboard,
        parse_mode="HTML"
    )

    await callback.answer()

@s_router.callback_query(F.data.startswith("admin:channel:"))
async def view_one_channel_admin(callback: CallbackQuery):
    """📢 Muayyan kanal ma'lumotlarini chiqaradi."""
    channel_id = int(callback.data.split(":")[2])

    channel_info = get_one_channel(channel_id)

    xabar = (
        f"📢 Kanal nomi: {channel_info[1]}\n"
        f"🆔 ID: {channel_info[0]}\n"
        f"🔗 Kanal ID: {channel_info[2]}\n"
        f"🌐 Kanal havolasi: {channel_info[3]}\n"
        f"📅 Yaratilgan vaqti: {channel_info[4]}"
    )

    await callback.message.edit_text(
        xabar,
        reply_markup=get_admin_channel_action_keyboard(channel_id)
    )

    await callback.answer()

@s_router.callback_query(F.data == "channel:add")
async def start_add_channel_process(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        "📢 <b>Kanal qo'shish</b>\n\n"
        "Kanal nomini kiriting:",
        parse_mode="HTML"
    )

    await state.set_state(
        ChannelManagementStates.waiting_for_channel_name
    )

    await callback.answer()

@s_router.callback_query(F.data.startswith("admin:delete:channel:"))
async def delete_channel_handler(callback: CallbackQuery):
    """🗑️ Kanalni bazadan o'chirib tashlaydi."""
    channel_id = int(callback.data.split(":")[3])

    delete_channel(channel_id)

    await callback.message.edit_text(
        f"✅ Kanal (ID: {channel_id}) muvaffaqiyatli o'chirildi.",
        reply_markup=channel_menu_keyboard
    )

    await callback.answer()


# -------------------------------------------------------------------
# 📦 ADMIN MAHSULOT AMALLARI
# -------------------------------------------------------------------

@s_router.callback_query(F.data == "admin:view_products")
async def view_products_admin(callback: CallbackQuery):
    """🗂️ Admin uchun barcha mahsulotlar ro'yxati."""
    await callback.message.edit_text(
        "🗂️ Barcha mahsulotlar ro'yxati:",
        reply_markup=get_admin_all_products_keyboard()
    )
    await callback.answer()

@s_router.callback_query(F.data == "add_admin")
async def start_add_admin_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(
        "📝 Yangi admin telegram ID sini kiriting:"
    )

    await state.set_state(
        AdminManagementStates.waiting_for_admin_id
    )


@s_router.callback_query(F.data.startswith("admin:product:"))
async def view_one_product_admin(callback: CallbackQuery):
    """📦 Muayyan mahsulot rasmi va ma'lumotlarini admin uchun ko'rsatadi."""
    product_id = int(callback.data.split(":")[2])
    product_info = get_one_product(product_id)
    rasm = product_info[6]

    xabar = (
        f"📦 Mahsulot ma'lumotlari\n\n"
        f"🥤 Nomi: {product_info[1]}\n"
        f"🆔 ID: {product_info[0]}\n"
        f"💰 Narxi: {product_info[4]} so'm\n"
        f"📦 Miqdori: {product_info[5]} dona\n"
        f"📝 Tavsif: {product_info[2]}\n"
        f"📅 Yaratilgan: {product_info[7]}"
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=rasm,
        caption=xabar,
        reply_markup=get_admin_product_action_keyboard(product_id)
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("admin:delete:product:"))
async def delete_product_handler(callback: CallbackQuery):
    """🗑️ Mahsulotni bazadan o'chiradi."""
    product_id = int(callback.data.split(":")[3])
    delete_products(product_id)
    await callback.message.delete()
    await callback.message.answer(
        f"✅ Mahsulot (ID: {product_id}) muvaffaqiyatli o'chirildi.", 
        reply_markup=admin_product_keyboard
    )
    await callback.answer()


# -------------------------------------------------------------------
# 👥 ADMINLARNI BOSHQARISH AMALLARI
# -------------------------------------------------------------------

@s_router.callback_query(F.data == "admin:view_admins")
async def view_admins_handler(callback: CallbackQuery):
    """📋 Barcha adminlar ro'yxatini ko'rsatadi."""
    await callback.message.edit_text(
        "📋 Adminni tanlang:",
        reply_markup=get_admin_list_keyboard()
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("admin:view_admin:"))
async def view_one_admin_handler(callback: CallbackQuery):
    """👤 Muayyan admin ma'lumotlarini ko'rsatadi."""
    admin_id = int(callback.data.split(":")[2])
    admin = get_one_admin(admin_id)

    xabar = (
        f"👤 Ismi: {admin[1]}\n"
        f"📛 Username: @{admin[2]}\n"
        f"🆔 Telegram ID: {admin[3]}\n"
        f"📅 Qo'shilgan vaqt: {admin[5]}"
    )

    await callback.message.edit_text(
        xabar,
        reply_markup=get_admin_user_action_keyboard(admin[3]) # delete tugmasiga telegram_id yuboriladi
    )
    await callback.answer()


@s_router.callback_query(F.data.startswith("admin:delete:admin:"))
async def delete_admin_handler(callback: CallbackQuery):
    """❌ Adminni vakolatlaridan mahrum qiladi va bazadan o'chiradi."""
    telegram_id = int(callback.data.split(":")[3])
    delete_admin(telegram_id)

    await callback.message.edit_text(
        "✅ Admin muvaffaqiyatli o'chirildi!",
        reply_markup=admin_menu_keyboard
    )
    await callback.answer()


# -------------------------------------------------------------------
# 📢 REKLAMA VA FOYDALANUVCHILAR STATISTIKASI
# -------------------------------------------------------------------

@s_router.callback_query(F.data == "admin:send_message")
async def send_message_cmd(callback: CallbackQuery, state: FSMContext):
    """📢 Reklama yuborish jarayonini boshlaydi (xabarni kutish holatiga o'tadi)."""
    await callback.message.answer("📢 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring:")
    await state.set_state(MessageState.message)
    await callback.answer()


@s_router.message(MessageState.message)
async def get_message(message: Message, state: FSMContext):
    """📢 Yuborilgan xabarni barcha foydalanuvchilarga nusxalab tarqatadi."""
    users_id = get_all_users_id()
    count = 0
    for user in users_id:
        try:
            await message.copy_to(user[0])
            count += 1
        except Exception:
            pass

    await state.clear()
    await message.answer(
        f"✅ Xabar {count} ta foydalanuvchiga muvaffaqiyatli yuborildi!",
        reply_markup=admin_users_keyboard
    )


@s_router.callback_query(F.data == "admin:view_users")
async def view_users_cmd(callback: CallbackQuery):
    """📊 Jami foydalanuvchilar sonini alert ko'rinishida ko'rsatadi."""
    users_id = get_all_users_id()
    xabar = f"📊 Botda jami {len(users_id)} ta foydalanuvchi mavjud."
    await callback.answer(xabar, show_alert=True)