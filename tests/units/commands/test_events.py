from commands.events import events_group


# create

def test_create_success(runner, mocker, commercial_ctx, payload_commercial, fake_contracts_list,
                        fake_event):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.get_contracts", return_value=fake_contracts_list)
    mock_create = mocker.patch("commands.events.create_event", return_value=fake_event)

    user_input = "\n".join([
        "événement",  # nom
        "1",  # id contrat
        "01/09/2056",  # date début
        "02/09/2056",  # date fin
        "Paris",  # adresse
        "100",  # participants
        "RAS",  # commentaires
    ])

    result = runner.invoke(events_group, ["create"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Événement événement créé." in result.output
    mock_create.assert_called_once()


def test_create_denied_for_wrong_role(runner, mocker, support_ctx, payload_support):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mock_create = mocker.patch("commands.events.create_event")

    result = runner.invoke(events_group, ["create"], input="", obj=support_ctx)

    assert "Accès refusé" in result.output
    mock_create.assert_not_called()


def test_create_no_contracts_available(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.get_contracts", side_effect=ValueError("Contrats introuvables."))

    result = runner.invoke(events_group, ["create"], input="événement\n", obj=commercial_ctx)
    assert "Contrats introuvables." in result.output


def test_create_displays_permission_error(runner, mocker, commercial_ctx, payload_commercial, fake_contracts_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.get_contracts", return_value=fake_contracts_list)
    mocker.patch("commands.events.create_event", side_effect=PermissionError("Action non autorisée."))

    user_input = "\n".join([
        "événement",  # nom
        "1",  # id contrat
        "01/09/2056",  # date début
        "02/09/2056",  # date fin
        "Paris",  # adresse
        "100",  # participants
        "RAS",  # commentaires
    ])

    result = runner.invoke(events_group, ["create"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


# update


def test_update_as_support(runner, mocker, support_ctx, payload_support, fake_events_list, fake_contracts_list,
                           fake_event):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mocker.patch("commands.events.decode_token", return_value=payload_support)
    mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mocker.patch("commands.events.get_event", return_value=fake_event)
    mocker.patch("commands.events.get_contracts", return_value=fake_contracts_list)
    mock_update = mocker.patch("commands.events.update_event", return_value=fake_event)

    user_input = "\n".join([
        "1",  # id événement
        "",  # nouveau nom (ignoré)
        "",  # nouveau contrat (ignoré)
        "",  # nouvelle date début (ignoré)
        "",  # nouvelle date fin (ignoré)
        "",  # nouvelle adresse (ignoré)
        "",  # nouveaux participants (ignoré)
        "",  # nouveaux commentaires (ignoré)
        ""
    ])

    result = runner.invoke(events_group, ["update"], input=user_input, obj=support_ctx)

    assert result.exit_code == 0
    assert "Événement 'événement' mis à jour." in result.output
    mock_update.assert_called_once()


def test_update_as_support_with_no_event_available(runner, mocker, support_ctx, payload_support):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mocker.patch("commands.events.decode_token", return_value=payload_support)
    mocker.patch("commands.events.get_events", side_effect=ValueError("Événement introuvables."))

    result = runner.invoke(events_group, ["update"], input="", obj=support_ctx)

    assert result.exit_code == 0
    assert "Événement introuvables." in result.output


def test_update_as_support_with_no_contract_available(runner, mocker, support_ctx, payload_support, fake_events_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mocker.patch("commands.events.decode_token", return_value=payload_support)
    mocker.patch("commands.events.get_events", return_value=fake_events_list)

    mocker.patch("commands.events.get_contracts", side_effect=ValueError("Contrats introuvables."))

    result = runner.invoke(events_group, ["update"], input="1\n\n", obj=support_ctx)

    assert result.exit_code == 0
    assert "Contrats introuvables." in result.output


def test_update_as_support_permission_error(runner, mocker, support_ctx, payload_support, fake_events_list,
                                            fake_contracts_list, fake_event):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mocker.patch("commands.events.decode_token", return_value=payload_support)
    mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mocker.patch("commands.events.get_contracts", return_value=fake_contracts_list)
    mocker.patch("commands.events.get_event", return_value=fake_event)
    mocker.patch("commands.events.update_event", side_effect=PermissionError("Action non autorisée."))

    user_input = "\n".join([
        "1",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    ])
    result = runner.invoke(events_group, ["update"], input=user_input, obj=support_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


def test_update_as_gestion(runner, mocker, gestion_ctx, payload_gestion, fake_events_list, fake_event):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mocker.patch("commands.events.get_supports", return_value=(" nom : support (id : 3)", ["3"]))
    mock_update = mocker.patch("commands.events.update_event_support", return_value=fake_event)

    user_input = "\n".join([
        "1",
        "3"
    ])
    result = runner.invoke(events_group, ["update"], input=user_input, obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Événement 'événement' mis à jour." in result.output
    mock_update.assert_called_once()


def test_update_as_gestion_with_no_event_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.get_events", side_effect=ValueError("Événements introuvables."))

    result = runner.invoke(events_group, ["update"], input="", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Événements introuvables." in result.output


def test_update_as_gestion_with_no_support_available(runner, mocker, gestion_ctx, payload_gestion, fake_events_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mocker.patch("commands.events.get_supports", side_effect=ValueError("Supports introuvables."))

    result = runner.invoke(events_group, ["update"], input="1\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Supports introuvables." in result.output


def test_update_as_gestion_permission_error(runner, mocker, gestion_ctx, payload_gestion, fake_events_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mocker.patch("commands.events.get_supports", return_value=(" nom : support (id : 3)", ["3"]))

    mocker.patch("commands.events.update_event_support", side_effect=PermissionError("Action non autorisée."))

    result = runner.invoke(events_group, ["update"], input="1\n3\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


def test_update_denied_for_commercial(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)

    mock_update = mocker.patch("commands.events.update_event")

    result = runner.invoke(events_group, ["update"], input="", obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Accès refusé" in result.output
    mock_update.assert_not_called()


# display

def test_display_as_support_with_filter(runner, mocker, support_ctx, payload_support, fake_events_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mocker.patch("commands.events.decode_token", return_value=payload_support)
    mock_get = mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mock_display = mocker.patch("commands.events.display_event")

    user_input = "\n".join([
        "y",  # afficher uniquement mes événements
        "1",  # id événement
    ])
    result = runner.invoke(events_group, ["display"], input=user_input, obj=support_ctx)

    assert result.exit_code == 0
    mock_get.assert_called_once_with(payload_support["id"], True, False)
    mock_display.assert_called_once_with(support_ctx["token"], "1")


def test_display_as_gestion_with_filter(runner, mocker, gestion_ctx, payload_gestion, fake_events_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.decode_token", return_value=payload_gestion)
    mock_get = mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mock_display = mocker.patch("commands.events.display_event")

    user_input = "\n".join([
        "y",  # événements sans support
        "1",
    ])
    result = runner.invoke(events_group, ["display"], input=user_input, obj=gestion_ctx)

    assert result.exit_code == 0
    mock_get.assert_called_once_with(None, False, True)
    mock_display.assert_called_once_with(gestion_ctx["token"], "1")


def test_display_as_commercial(runner, mocker, commercial_ctx, payload_commercial, fake_events_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.events.decode_token", return_value=payload_commercial)
    mock_get = mocker.patch("commands.events.get_events", return_value=fake_events_list)
    mock_display = mocker.patch("commands.events.display_event")

    user_input = "\n".join([
        "1",
    ])

    result = runner.invoke(events_group, ["display"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    mock_get.assert_called_once_with(None, False, False)
    mock_display.assert_called_once_with(commercial_ctx["token"], "1")


def test_display_no_event_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.decode_token", return_value=payload_gestion)
    mocker.patch("commands.events.get_events", side_effect=ValueError("Événements introuvables."))

    result = runner.invoke(events_group, ["display"], input="\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Événements introuvables." in result.output
