import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# from dotenv import load_dotenv
from shopping_bot.db.repository.product_repository import ProductRepository
from shopping_bot.db.repository.request_repository import RequestRepository
from shopping_bot.db.repository.user_repository import UserRepository
from shopping_bot.handlers.add_products import product_router
from shopping_bot.handlers.base import router
from shopping_bot.services.product_service import ProductController
from shopping_bot.services.request_service import RequestService
from shopping_bot.services.user_service import UserService

# load_dotenv()

TOKEN = str(os.getenv("SHOPPING_BOT_TOKEN"))
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)
dp.include_router(product_router)

# Register User repository and User service to User handlers
user_repository = UserRepository()
user_service = UserService(user_repository)

# TODO: Register Product repository and Product service to Product handers
product_repository = ProductRepository()
product_service = ProductController(product_repository)

request_repository = RequestRepository()
request_service = RequestService(request_repository, user_service)


async def main():
    await dp.start_polling(
        bot,
        user_controller=user_service,
        product_controller=product_service,
        request_controller=request_service,
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
