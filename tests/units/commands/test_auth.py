from commands.auth import login_command, logout_command


# login_command
def test_login_success(runner, mocker, fake_commercial):
    mocker.patch(
        "commands.auth.login",
        return_value=("fake-token", fake_commercial),
    )
    mock_save = mocker.patch("commands.auth.save_token")
    mock_sentry = mocker.patch("commands.auth.sentry_sdk.set_user")

    result = runner.invoke(
        login_command,
        input="commercial@crm.com\nMdp12345\n",
    )

    assert result.exit_code == 0
    assert "Connecté en tant que" in result.output
    assert fake_commercial.name in result.output
    mock_save.assert_called_once_with("fake-token")
    mock_sentry.assert_called_once_with({"id": fake_commercial.id})


def test_login_invalid_credentials(runner, mocker):
    mocker.patch(
        "commands.auth.login",
        side_effect=ValueError("Email ou mot de passe incorrect."),
    )
    mock_save = mocker.patch("commands.auth.save_token")

    result = runner.invoke(
        login_command,
        input="wrong@mail.com\nwrongpass\n",
    )

    assert result.exit_code != 0
    assert "Email ou mot de passe incorrect." in result.output
    mock_save.assert_not_called()


def test_login_prompts_hide_password(runner, mocker, fake_commercial):
    """Vérifie que le mot de passe n'apparaît jamais en clair dans l'output."""
    mocker.patch(
        "commands.auth.login",
        return_value=("fake-token", fake_commercial),
    )
    mocker.patch("commands.auth.save_token")
    mocker.patch("commands.auth.sentry_sdk.set_user")

    result = runner.invoke(
        login_command,
        input="commercial@crm.com\nMdp12345\n",
    )
    assert result.exit_code == 0
    assert "Mdp12345" not in result.output



# logout_command
def test_logout_deletes_token(runner, mocker):
    mock_delete = mocker.patch("commands.auth.delete_token")

    result = runner.invoke(logout_command)

    assert result.exit_code == 0
    assert "Déconnecté." in result.output
    mock_delete.assert_called_once()