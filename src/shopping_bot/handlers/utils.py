from aiogram.types import User

from shopping_bot.core.domain import RequestUserDomain


def user_to_domain(user: User) -> RequestUserDomain:
    id = user.id
    name = user.first_name
    return RequestUserDomain(id, name)
