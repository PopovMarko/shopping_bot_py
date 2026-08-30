from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_user_controller():
    user_controller = MagicMock()
    user_controller.start_cmd = AsyncMock()

    return user_controller


@pytest.fixture
def mock_product_controller():
    product_controller = MagicMock()
    product_controller.process_quantity = AsyncMock()
    product_controller.process_product = AsyncMock()
    product_controller.process_confirmation = AsyncMock()
    return product_controller


@pytest.fixture
def mock_state():
    state = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.get_vale = AsyncMock()
    return state


@pytest.fixture
def mock_response():
    response = AsyncMock()
    response.product_id = 1
    response.product_name = "milk"
    response.quantity = 10
    response.units = "kilo"
    return response
