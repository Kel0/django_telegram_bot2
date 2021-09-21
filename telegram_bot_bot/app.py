import sys
from aiogram import executor
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # filters.setup(dp)
    # middlewares.setup(dp)
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    import django, os
    sys.path.append('../django_telegram_bot2')
    print(sys.path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_telegram_bot2.settings')
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': 'true'})
    django.setup()
    import middlewares, filters, handlers
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

