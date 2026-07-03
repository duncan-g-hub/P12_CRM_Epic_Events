from commands.contracts import contracts_group


# create

def test_create_success(runner, mocker, gestion_ctx, payload_gestion, fake_customers_list, fake_contract):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_customers", return_value=fake_customers_list)
    mock_create = mocker.patch("commands.contracts.create_contract", return_value=fake_contract)

    user_input = "\n".join(["1", "1000", "500", "true"])
    result = runner.invoke(contracts_group, ["create"], input=user_input, obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Contrat pour le client client créé." in result.output
    mock_create.assert_called_once()


def test_create_no_customers_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_customers", side_effect=ValueError("Clients introuvables."))

    result = runner.invoke(contracts_group, ["create"], input="", obj=gestion_ctx)
    assert result.exit_code == 0
    assert "Clients introuvables." in result.output


def test_create_denied_for_wrong_role(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mock_create = mocker.patch("commands.contracts.create_contract")

    result = runner.invoke(contracts_group, ["create"], input="", obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Accès refusé" in result.output
    mock_create.assert_not_called()


def test_create_displays_permission_error(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.create_contract", side_effect=PermissionError("Action non autorisée."))

    user_input = "\n".join(["1", "1000", "500", "true"])
    result = runner.invoke(contracts_group, ["create"], input=user_input, obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


# update

def test_update_success(runner, mocker, gestion_ctx, payload_gestion, fake_contracts_list, fake_customers_list,
                        fake_contract):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_contracts", return_value=fake_contracts_list)
    mocker.patch("commands.contracts.get_customers", return_value=fake_customers_list)
    mocker.patch("commands.contracts.get_contract", return_value=fake_contract)
    mock_update = mocker.patch("commands.contracts.update_contract", return_value=fake_contract)

    user_input = "\n".join(["1", "", "", "", "", ""])
    result = runner.invoke(contracts_group, ["update"], input=user_input, obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Contrat pour le client client mis à jour." in result.output
    mock_update.assert_called_once()


def test_update_no_contract_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_contracts", side_effect=ValueError("Contrats introuvables."))
    result = runner.invoke(contracts_group, ["update"], input="", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Contrats introuvables." in result.output


def test_update_no_customers_available(runner, mocker, gestion_ctx, payload_gestion, fake_contracts_list,
                                       fake_contract):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_contracts", return_value=fake_contracts_list)
    mocker.patch("commands.contracts.get_contract", return_value=fake_contract)
    mocker.patch("commands.contracts.get_customers", side_effect=ValueError("Clients introuvables."))

    result = runner.invoke(contracts_group, ["update"], input="1\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Clients introuvables." in result.output


def test_update_denied_for_support(runner, mocker, support_ctx, payload_support,
                                   fake_contracts_list, fake_customers_list, fake_contract):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mock_update = mocker.patch("commands.contracts.update_contract")

    user_input = "\n".join(["1", "", "", "", ""])
    result = runner.invoke(contracts_group, ["update"], input=user_input, obj=support_ctx)

    assert result.exit_code == 0
    assert "Accès refusé." in result.output
    mock_update.assert_not_called()


def test_update_permission_error(runner, mocker, gestion_ctx, payload_gestion, fake_contracts_list,
                                 fake_customers_list, fake_contract):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_contracts", return_value=fake_contracts_list)
    mocker.patch("commands.contracts.get_contract", return_value=fake_contract)
    mocker.patch("commands.contracts.get_customers", return_value=fake_customers_list)
    mocker.patch("commands.contracts.update_contract", side_effect=PermissionError("Action non autorisée."))

    user_input = "\n".join(["1", "", "", "", "", ""])

    result = runner.invoke(contracts_group, ["update"], input=user_input, obj=gestion_ctx)
    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


# display

def test_display_as_gestion(runner, mocker, gestion_ctx, payload_gestion, fake_contracts_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_contracts", return_value=fake_contracts_list)
    mock_display = mocker.patch("commands.contracts.display_contract")

    result = runner.invoke(contracts_group, ["display"], input="1\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Affichage des détails d'un contrat" in result.output
    mock_display.assert_called_once()


def test_display_as_commercial_with_all_filters(runner, mocker, commercial_ctx, payload_commercial,
                                                fake_contracts_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.contracts.decode_token", return_value=payload_commercial)
    mocker.patch("commands.contracts.get_contracts", return_value=fake_contracts_list)
    mock_display = mocker.patch("commands.contracts.display_contract")

    user_input = "\n".join(["y", "y", "y", "1"])
    result = runner.invoke(contracts_group, ["display"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Affichage des détails d'un contrat" in result.output
    mock_display.assert_called_once()


def test_display_no_contracts_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.decode_token", return_value=payload_gestion)
    mocker.patch("commands.contracts.get_contracts", side_effect=ValueError("Contrats introuvables."))

    result = runner.invoke(contracts_group, ["display"], input="", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Contrats introuvables." in result.output
