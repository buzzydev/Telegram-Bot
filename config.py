from aiogram import Bot
from database import get_all_channels

GROUP_ID = -4943806883
ADMIN_ID = 8968685902

channels = get_all_channels()

CHANNEL_ID = []

for i in channels:
    CHANNEL_ID.append(i[2])

LEFT_STATUS = [
    'left',
    'kicked'
]