from shopping_bot.core.domain import ResponseUserDomain, UserRegistrationResult
from shopping_bot.handlers.messages import user_domain_to_string


def test_user_domain_to_string():
    user_domain = ResponseUserDomain(
        UserRegistrationResult.REGISTER_USER_SUCCESS, 1, 123, "Marko"
    )
    res = user_domain_to_string(user_domain)
    assert res == "Welcome Marko, \nnow you are registered user"
