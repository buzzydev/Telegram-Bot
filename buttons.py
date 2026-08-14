from email import message

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import (
    get_all_cart_items_by_id,
    get_all_categories,
    get_all_products,
    get_one_product,
    get_product_by_category,
    get_all_admins,
    get_all_channels
)

# ====================================================================
# 1. 👤 FOYDALANUVCHI (USER) TUGMALARI
# ====================================================================

# 🏠 Asosiy boshlang'ich menyu (User Start)
user_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📂 Kategoriyalar", callback_data="user:categories"),
            InlineKeyboardButton(text="🛒 Savat", callback_data="user:cart")
        ]
    ]
)

# ⏭ Qadamni o'tkazib yuborish tugmasi
skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏭ Skip")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 📱 Telefon raqam so'rash tugmasi
phone_request_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 📍 Geolokatsiya so'rash tugmasi
location_request_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# 🔙 Oddiy orqaga qaytish tugmasi
back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="user:start_menu")]
    ]
)


# 📂 Kategoriyalar ro'yxati (Foydalanuvchilar uchun)
def get_user_categories_keyboard():
    """Foydalanuvchilar uchun barcha kategoriyalar tugmalarini shakllantiradi."""
    builder = InlineKeyboardBuilder()
    categories = get_all_categories()

    for category in categories:
        builder.button(
            text=f"📁 {category[1]}",
            callback_data=f"user:category:{category[0]}"
        )

    builder.button(text="🔙 Orqaga", callback_data="user:start_menu")
    builder.adjust(1)
    return builder.as_markup()


# 🛵 Yetkazib berish turini tanlash tugmalari
def delivery_type_inline_keyboard():
    """Buyurtma usulini (Eltib berish / Borib olish) tanlash tugmalari."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🛵 Eltib berish",
        callback_data="order:delivery"
    )
    builder.button(
        text="🚶 Borib olish",
        callback_data="order:pickup"
    )
    builder.button(
        text="⬅️ Ortga",
        callback_data="user:cart"
    )

    builder.adjust(2, 1)
    return builder.as_markup()


# 📦 Kategoriya ichidagi mahsulotlar ro'yxati (Foydalanuvchilar uchun)
def get_user_category_products_keyboard(category_id):
    """Tanlangan kategoriya bo'yicha mahsulotlar ro'yxatini qaytaradi."""
    builder = InlineKeyboardBuilder()
    products = get_product_by_category(category_id)

    for product in products:
        builder.button(
            text=f"📦 {product[1]}",
            callback_data=f"user:product:{product[0]}"
        )

    builder.button(text="🔙 Orqaga", callback_data="user:categories")
    builder.adjust(1)
    return builder.as_markup()


# 🛒 Mahsulot kartochkasi ostidagi tugma (Savatga qo'shish)
def get_user_product_action_keyboard(product_id):
    """Mahsulotni savatga qo'shish yoki ortga qaytish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🛒 Savatga qo'shish",
        callback_data=f"user:add_to_cart:{product_id}"
    )
    builder.button(text="🔙 Orqaga", callback_data="user:categories")
    builder.adjust(1)
    return builder.as_markup()

def approve_button(order_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Tasdiqlash",
        callback_data=f"approve:order:{order_id}"
    )

    builder.button(
        text="❌ Rad etish",
        callback_data=f"cancel:order:{order_id}"
    )

    builder.adjust(2)

    return builder.as_markup()


# def channel_button():
#     builder = InlineKeyboardBuilder()

#     builder.button(
#         text="KANAL 1",
#         url="https://t.me/TestWorldServer"
#     )
#     builder.button(
#         text="✅ Tasdiqlash",
#         callback_data="check_subs"
#     )
#     builder.adjust(2)

#     return builder.as_markup()

CHANNEL = get_all_channels()


CHANNEL = get_all_channels()


def channel_button(obuna_bolmagan_kanallar):
    builder = InlineKeyboardBuilder()

    for channel_id in obuna_bolmagan_kanallar:
        for channel in CHANNEL:

            # Database'dagi kanal ID bilan tekshirish
            if str(channel[0]) == str(channel_id):
                builder.button(
                    text=f"📢 {channel[1]}",
                    url=channel[2]
                )
                break

    builder.button(
        text="✅ Tekshirish",
        callback_data="check_subs"
    )

    builder.adjust(1)

    return builder.as_markup()

# 🛍️ Savatdagi elementlar (user_id bo'yicha oladi)
def get_user_cart_items_keyboard(user_id: int):
    """Foydalanuvchi savatidagi mahsulotlar va miqdorini boshqarish tugmalari."""
    builder = InlineKeyboardBuilder()

    cart_items = get_all_cart_items_by_id(user_id)
    rows = []

    if cart_items:
        for item in cart_items:
            product = get_one_product(item[2])

            if not product:
                return "NO XATOLIK"

            # minus (-) tugmasi
            builder.button(
                text="➖",
                callback_data=f"sub:count:{item[0]}"
            )

            # mahsulot ma'lumoti tugmasi
            builder.button(
                text=f"🛍️ {product[1]} - {item[4]} ta - {item[3]} so'm",
                callback_data=f"user:cart_item:{item[0]}"
            )

            # plus (+) tugmasi
            builder.button(
                text="➕",
                callback_data=f"add:count:{item[0]}"
            )

            # Har bir mahsulot uchun 3 ta tugma ( - | Mahsulot | + )
            rows.append(3)

    else:
        builder.button(
            text="🛒 Savat bo'sh",
            callback_data="empty"
        )
        rows.append(1)

    # Buyurtma rasmiylashtirish va savatni tozalash
    if cart_items:
        builder.button(
            text="📦 Buyurtma berish",
            callback_data="user:order"
        )

        builder.button(
            text="🗑️ Savatni tozalash",
            callback_data="user:clear_cart"
        )

        rows.append(2)

    # Orqaga qaytish tugmasi
    builder.button(
        text="🔙 Orqaga",
        callback_data="user:start_menu"
    )

    rows.append(1)
    builder.adjust(*rows)

    return builder.as_markup()


# ====================================================================
# 2. 👨‍💼 ADMIN PANEL TUGMALARI
# ====================================================================

# 👑 Admin asosiy menyusi
admin_start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📦 Mahsulotlar Menyu", callback_data="admin:menu:products"),
            InlineKeyboardButton(text="👥 Adminlar Menyu", callback_data="admin:menu:admins")
        ],
        [
            InlineKeyboardButton(text="📂 Kategoriyalar Menyu", callback_data="admin:menu:categories"),
            InlineKeyboardButton(text="📊 Foydalanuvchilar", callback_data="admin:menu:users")
        ],
        [
            InlineKeyboardButton(text="🛹 Kanallar Menyu", callback_data="admin:add_channel")
        ]
    ]
)

channel_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Kanal qo'shish",
                callback_data="channel:add"
            ),
            InlineKeyboardButton(
                text="📋 Kanallarni ko'rish",
                callback_data="channel:view"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="admin:start_menu"
            )
        ]
    ]
)

# 👥 Adminlar Menyusi
admin_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"),
            InlineKeyboardButton(text="📋 Adminlarni ko'rish", callback_data="admin:view_admins")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:start_menu")]
    ]
)

# 📦 Mahsulotlar Menyusi
admin_product_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Mahsulot qo'shish", callback_data="add_product"),
            InlineKeyboardButton(text="👁️ Mahsulotlarni ko'rish", callback_data="admin:view_products")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:start_menu")]
    ]
)

# 📂 Kategoriyalar Menyusi
admin_category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kategoriya qo'shish", callback_data="add_category"),
            InlineKeyboardButton(text="👁️ Kategoriyalarni ko'rish", callback_data="admin:view_categories")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:start_menu")]
    ]
)

# 👥 Foydalanuvchilar Menyusi
admin_users_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Foydalanuvchilarni ko'rish", callback_data="admin:view_users"),
            InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="admin:send_message")
        ],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin:start_menu")]
    ]
)


# 📌 Mahsulot qo'shishda kategoriyalarni tanlash uchun
def ctgs_for_add_prd():
    """Mahsulot qo'shish bosqichida kategoriyalarni ro'yxat shaklida chiqaradi."""
    builder = InlineKeyboardBuilder()
    categories = get_all_categories()

    for category in categories:
        builder.button(
            text=f"📌 {category[1]}",
            callback_data=f"ctg_{category[0]}"
        )
    builder.adjust(1)
    return builder.as_markup()


# 📂 Kategoriyalar ro'yxati (Admin uchun)
def get_admin_categories_keyboard():
    """Admin uchun barcha kategoriyalar ro'yxati."""
    builder = InlineKeyboardBuilder()
    categories = get_all_categories()

    for category in categories:
        builder.button(
            text=f"📂 {category[1]}",
            callback_data=f"admin:category:{category[0]}"
        )

    builder.button(text="🔙 Orqaga", callback_data="admin:menu:categories")
    builder.adjust(1)
    return builder.as_markup()

def get_admin_channels_keyboard():
    """Admin uchun barcha kanallar ro'yxati."""
    builder = InlineKeyboardBuilder()
    channels = get_all_channels()

    for channel in channels:
        builder.button(
            text=f"📢 {channel[1]}",
            callback_data=f"admin:channel:{channel[0]}"
        )

    builder.button(
        text="🔙 Orqaga",
        callback_data="admin:menu:channels"
    )

    builder.adjust(1)
    return builder.as_markup()

def get_admin_channel_action_keyboard(channel_id):
    """📢 Kanal uchun admin action tugmalari."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🗑️ Kanalni o'chirish",
        callback_data=f"admin:delete:channel:{channel_id}"
    )

    builder.button(
        text="🔙 Orqaga",
        callback_data="admin:menu:channels"
    )

    builder.adjust(1)

    return builder.as_markup()


# 📦 Tanlangan kategoriya bo'yicha mahsulotlar (Admin uchun)
def get_admin_category_products_keyboard(category_id):
    """Admin uchun muayyan kategoriya ichidagi mahsulotlar."""
    builder = InlineKeyboardBuilder()
    products = get_product_by_category(category_id)

    for product in products:
        builder.button(
            text=f"📦 {product[1]}",
            callback_data=f"admin:product_item:{product[0]}"
        )
    builder.button(text="🔙 Orqaga", callback_data="admin:menu:categories")
    builder.adjust(1)
    return builder.as_markup()


# 🏷️ Barcha mahsulotlar ro'yxati (Admin uchun)
def get_admin_all_products_keyboard():
    """Admin uchun bazadagi barcha mahsulotlar ro'yxati."""
    builder = InlineKeyboardBuilder()
    products = get_all_products()

    for product in products:
        builder.button(
            text=f"🏷️ {product[1]}",
            callback_data=f"admin:product:{product[0]}"
        )

    builder.button(text="🔙 Orqaga", callback_data="admin:menu:products")
    builder.adjust(1)
    return builder.as_markup()


# 👤 Adminlar ro'yxati (Admin uchun)
def get_admin_list_keyboard():
    """Mavjud adminlar ro'yxatini chiqaruvchi tugmalar."""
    builder = InlineKeyboardBuilder()
    admins = get_all_admins()

    for admin in admins:
        builder.button(
            text=f"👤 {admin[1]}",
            callback_data=f"admin:view_admin:{admin[0]}"
        )

    builder.button(text="🔙 Orqaga", callback_data="admin:menu:admins")
    builder.adjust(1)
    return builder.as_markup()


# ====================================================================
# 3. ⚙️ ADMIN AMALLARI (O'CHIRISH TUGMALARI)
# ====================================================================

# 🗑️ Kategoriyani o'chirish
def get_admin_category_action_keyboard(category_id):
    """Kategoriyani o'chirish yoki ortga qaytish amali."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑️ O'chirish", callback_data=f"admin:delete:category:{category_id}")
    builder.button(text="🔙 Orqaga", callback_data="admin:menu:categories")
    builder.adjust(1)
    return builder.as_markup()


# 🗑️ Mahsulotni o'chirish
def get_admin_product_action_keyboard(product_id):
    """Mahsulotni o'chirish yoki ortga qaytish amali."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑️ O'chirish", callback_data=f"admin:delete:product:{product_id}")
    builder.button(text="🔙 Orqaga", callback_data="admin:menu:products")
    builder.adjust(1)
    return builder.as_markup()


# ❌ Adminlikdan olib tashlash
def get_admin_user_action_keyboard(admin_id):
    """Adminni lavozimidan olib tashlash yoki ortga qaytish amali."""
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Adminlikdan olish", callback_data=f"admin:delete:admin:{admin_id}")
    builder.button(text="🔙 Orqaga", callback_data="admin:menu:admins")
    builder.adjust(1)
    return builder.as_markup()