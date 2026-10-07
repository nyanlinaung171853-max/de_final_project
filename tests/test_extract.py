import pytest
from unittest.mock import patch, Mock
from src.extract import extract_products


@patch("src.extract.requests.get")
def test_extract_returns_products(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "products": [{"id": 1, "title": "Test"}],
        "total": 1
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    products = extract_products()
    assert len(products) == 1
    assert products[0]["id"] == 1


@patch("src.extract.requests.get")
def test_extract_handles_timeout(mock_get):
    from requests.exceptions import Timeout
    mock_get.side_effect = Timeout("timeout")

    with pytest.raises(Timeout):
        extract_products()