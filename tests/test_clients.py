import pytest
from bskyapi.clients import BskyApiClient, AuthenticationError
from atproto.exceptions import AtProtocolError


def test_authenticate_success(mock_atproto_client, mocker):
    """Test successful authentication."""
    # Correct patch path
    mocker.patch("bskyapi.clients.Client", return_value=mock_atproto_client)

    # Create the BskyApiClient and authenticate
    client = BskyApiClient()
    client.authenticate("username", "password")

    # Assert that the login method was called correctly
    mock_atproto_client.login.assert_called_once_with("username", "password")


def test_authenticate_failure(mock_atproto_client, mocker):
    """Test authentication failure."""
    # Correct patch path
    mocker.patch("bskyapi.clients.Client", return_value=mock_atproto_client)

    # Ensure the login method raises AtProtocolError
    mock_atproto_client.login.side_effect = AtProtocolError("Invalid credentials")

    # Create the BskyApiClient and attempt to authenticate
    client = BskyApiClient()
    with pytest.raises(AuthenticationError, match="Authentication failed"):
        client.authenticate("username", "password")

    # Assert that login was called with the correct arguments
    mock_atproto_client.login.assert_called_once_with("username", "password")
