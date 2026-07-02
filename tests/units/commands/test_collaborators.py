from commands.collaborators import collaborators_group


# create
def test_create_success_as_gestion(runner, mocker, gestion_ctx, payload_gestion, fake_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mock_create = mocker.patch(
        "commands.collaborators.create_collaborator",
        return_value=fake_gestion,
    )

    user_input = "\n".join([
        "Nouveau Collab",  # nom
        "nouv.collab@crm.com",  # email
        "Mdp12345!",  # mot de passe
        "Mdp12345!",  # confirmation
        "0123456789",  # téléphone
        "3",  # rôle : gestion
    ])

    result = runner.invoke(
        collaborators_group, ["create"],
        input=user_input, obj=gestion_ctx,
    )

    assert result.exit_code == 0
    assert "Collaborateur 'gestion' créé." in result.output
    mock_create.assert_called_once()


def test_create_denied_for_wrong_role(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mock_create = mocker.patch("commands.collaborators.create_collaborator")

    result = runner.invoke(
        collaborators_group, ["create"],
        input="", obj=commercial_ctx,
    )
    assert result.exit_code == 0
    assert "Accès refusé" in result.output
    mock_create.assert_not_called()


def test_create_password_mismatch_then_retry(runner, mocker, gestion_ctx, payload_gestion, fake_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch(
        "commands.collaborators.create_collaborator",
        return_value=fake_gestion,
    )

    user_input = "\n".join([
        "test",
        "test@email.com",
        "Mdp12345",  # mot de passe
        "Mdp54321",  # confirmation ne correspond pas -> re-demande
        "Mdp12345!",  # nouveau mot de passe
        "Mdp12345!",  # confirmation correcte
        "0123456789",
        "3",
        "",
    ])

    result = runner.invoke(
        collaborators_group, ["create"],
        input=user_input, obj=gestion_ctx,
    )

    assert "Les mots de passe ne correspondent pas." in result.output
    assert result.exit_code == 0


# update
def test_update_success(runner, mocker, gestion_ctx, payload_gestion, fake_gestion, fake_collaborators_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch(
        "commands.collaborators.get_collaborators",
        return_value=fake_collaborators_list,
    )
    mock_update = mocker.patch(
        "commands.collaborators.update_collaborator",
        return_value=fake_gestion,
    )

    user_input = "\n".join([
        "1",  # id du collaborateur
        "",  # nouveau nom (ignoré)
        "",  # nouvel email (ignoré)
        "",  # nouveau mot de passe (ignoré)
        "",  # nouveau téléphone (ignoré)
        "",  # nouveau rôle (ignoré)
        "",
    ])

    result = runner.invoke(
        collaborators_group, ["update"],
        input=user_input, obj=gestion_ctx,
    )

    assert result.exit_code == 0
    assert "mis à jour" in result.output
    mock_update.assert_called_once()


def test_update_denied_for_wrong_role(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mock_update = mocker.patch("commands.collaborators.update_collaborator")

    result = runner.invoke(
        collaborators_group, ["update"],
        input="", obj=commercial_ctx,
    )
    assert result.exit_code == 0
    assert "Accès refusé" in result.output
    mock_update.assert_not_called()


def test_update_no_collaborators_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch(
        "commands.collaborators.get_collaborators",
        side_effect=ValueError("Aucun collaborateur disponible."),
    )
    result = runner.invoke(
        collaborators_group, ["update"],
        input="", obj=gestion_ctx,
    )
    assert result.exit_code == 0
    assert "Aucun collaborateur disponible." in result.output


def test_update_displays_permission_error(runner, mocker, gestion_ctx, payload_gestion,
                                          fake_collaborators_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch(
        "commands.collaborators.get_collaborators",
        return_value=fake_collaborators_list,
    )
    mocker.patch(
        "commands.collaborators.update_collaborator",
        side_effect=PermissionError("Action non autorisée."),
    )

    user_input = "\n".join(["1", "", "", "", "", "", ""])

    result = runner.invoke(
        collaborators_group, ["update"],
        input=user_input, obj=gestion_ctx,
    )
    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


# display
def test_display_success(runner, mocker, commercial_ctx, payload_commercial, fake_collaborators_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch(
        "commands.collaborators.get_collaborators",
        return_value=fake_collaborators_list,
    )
    mock_display = mocker.patch("commands.collaborators.display_collaborator")

    user_input = "\n".join([
        "",  # pas de filtre par rôle
        "1",  # id du collaborateur à afficher
    ])

    result = runner.invoke(
        collaborators_group, ["display"],
        input=user_input, obj=commercial_ctx,
    )

    assert result.exit_code == 0
    mock_display.assert_called_once_with(commercial_ctx["token"], "1")


def test_display_with_role_filter(runner, mocker, gestion_ctx, payload_gestion, fake_collaborators_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mock_get = mocker.patch(
        "commands.collaborators.get_collaborators",
        return_value=fake_collaborators_list,
    )
    mocker.patch("commands.collaborators.display_collaborator")

    user_input = "\n".join([
        "1",  # filtre : commercial
        "1",  # id du collaborateur
    ])

    result = runner.invoke(
        collaborators_group, ["display"],
        input=user_input, obj=gestion_ctx,
    )

    assert result.exit_code == 0
    mock_get.assert_called_once_with("1")
