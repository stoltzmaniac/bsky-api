import pytest
from unittest.mock import Mock
from bskyapi.clients import BskyApiClient


@pytest.fixture
def mock_atproto_client(mocker):
    """Mock the atproto.Client instance."""
    mock_client = mocker.Mock()
    # Ensure the mocked login method behaves as expected
    mock_client.login.return_value = None
    return mock_client


@pytest.fixture
def mock_bsky_client(mocker):
    """Mock the BskyApiClient."""
    mock_client = mocker.Mock(spec=BskyApiClient)

    # Mock ensure_authenticated to raise AuthenticationError when needed
    mock_client.ensure_authenticated.return_value = None

    # Mock the client property to invoke ensure_authenticated
    mock_client.client = mocker.PropertyMock(
        side_effect=lambda: mock_client.ensure_authenticated() or Mock()
    )

    # Mock the app.bsky.feed.search_posts method
    mock_client.client.app.bsky.feed.search_posts = Mock(return_value={"results": []})

    return mock_client
