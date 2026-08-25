import pytest

from shopping_bot.core.domain import ResponseUserDomain, UserRegistrationResult
from shopping_bot.handlers.messages import user_domain_to_string


@pytest.mark.parametrize(
    "status, response_string",
    [
        (
            UserRegistrationResult.REGISTER_USER_SUCCESS,
            "Welcome Marko, \nnow you are registered user",
        ),
        (UserRegistrationResult.REGISTERED_USER, "Welcome back Marko"),
    ],
)
def test_user_domain_to_string(status, response_string):
    user_domain = ResponseUserDomain(status, 1, 123, "Marko")
    res = user_domain_to_string(user_domain)
    assert res == response_string
