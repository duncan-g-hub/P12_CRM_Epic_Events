from commands.customers import customers_group


# create

def test_create_success(runner, mocker, commercial_ctx, payload_commercial, fake_customer):
    mocker.patch("commands.customers.decode_token", return_value=payload_commercial)
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mock_create = mocker.patch("commands.customers.create_customer", return_value=fake_customer)

    user_input = "\n".join(["Nouveau Client", "nouv.client@crm.com", "0123456789", "entreprise"])
    result = runner.invoke(customers_group, ["create"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Client 'client' créé." in result.output
    mock_create.assert_called_once()


def test_create_denied_for_wrong_role(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mock_create = mocker.patch("commands.customers.create_customer")

    result = runner.invoke(customers_group, ["create"], input="", obj=gestion_ctx)
    assert result.exit_code == 0
    assert "Accès refusé" in result.output
    mock_create.assert_not_called()


def test_create_displays_permission_error(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.customers.decode_token", return_value=payload_commercial)
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.create_customer", side_effect=PermissionError("Action non autorisée."))

    user_input = "\n".join(["Nouveau Client", "nouv.client@crm.com", "0123456789", "entreprise"])
    result = runner.invoke(customers_group, ["create"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


# update

def test_update_no_customers_available(runner, mocker, commercial_ctx, payload_commercial):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.get_customers", side_effect=ValueError("Aucun client disponible."))

    result = runner.invoke(customers_group, ["update"], input="", obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Aucun client disponible." in result.output


def test_update_as_commercial(runner, mocker, commercial_ctx, payload_commercial, fake_customers_list, fake_customer):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.get_customers", return_value=fake_customers_list)
    mock_update = mocker.patch("commands.customers.update_customer", return_value=fake_customer)

    user_input = "\n".join(["1", "", "", "", "", ""])
    result = runner.invoke(customers_group, ["update"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Client 'client' mis à jour." in result.output
    mock_update.assert_called_once()


def test_update_as_commercial_displays_permission_error(runner, mocker, commercial_ctx, payload_commercial,
                                                        fake_customers_list, ):
    mocker.patch("commands.utils.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.decode_token", return_value=payload_commercial)
    mocker.patch("commands.customers.get_customers", return_value=fake_customers_list)
    mocker.patch("commands.customers.update_customer", side_effect=PermissionError("Action non autorisée."))

    user_input = "\n".join(["1", "", "", "", "", "", ])
    result = runner.invoke(customers_group, ["update"], input=user_input, obj=commercial_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


def test_update_as_gestion_reassigns_commercial(runner, mocker, gestion_ctx, payload_gestion, fake_customers_list,
                                                fake_customer):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.get_customers", return_value=fake_customers_list)
    mocker.patch("commands.customers.get_commercials", return_value=(" nom : client (id : 1)", ["1"]))
    mock_reassign = mocker.patch("commands.customers.update_customer_commercial", return_value=fake_customer)

    user_input = "\n".join(["1", "1"])
    result = runner.invoke(customers_group, ["update"], input=user_input, obj=gestion_ctx)

    assert "Client 'client' mis à jour." in result.output
    assert result.exit_code == 0
    mock_reassign.assert_called_once()


def test_update_as_gestion_no_commercials_available(runner, mocker, gestion_ctx, payload_gestion, fake_customers_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.get_customers", return_value=fake_customers_list)
    mocker.patch("commands.customers.get_commercials", side_effect=ValueError("Il n'éxiste aucun commercial."))

    result = runner.invoke(customers_group, ["update"], input="1\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Il n'éxiste aucun commercial." in result.output


def test_update_as_gestion_displays_permission_error(runner, mocker, gestion_ctx, payload_gestion, fake_customers_list
                                                     ):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.get_customers", return_value=fake_customers_list)
    mocker.patch("commands.customers.get_commercials", return_value=(" id : 1 - Nom : commercial", ["1"]))
    mocker.patch("commands.customers.update_customer_commercial", side_effect=PermissionError("Action non autorisée."))

    result = runner.invoke(customers_group, ["update"], input="1\n1\n", obj=gestion_ctx)

    assert result.exit_code == 0
    assert "Action non autorisée." in result.output


def test_update_denied_for_support(runner, mocker, support_ctx, payload_support):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mock_update = mocker.patch("commands.customers.update_customer")

    result = runner.invoke(customers_group, ["update"], input="", obj=support_ctx)

    assert result.exit_code == 0
    assert "Accès refusé" in result.output
    mock_update.assert_not_called()


# display
def test_display_success(runner, mocker, support_ctx, payload_support, fake_customers_list):
    mocker.patch("commands.utils.decode_token", return_value=payload_support)
    mocker.patch("commands.customers.get_customers", return_value=fake_customers_list)
    mock_display = mocker.patch("commands.customers.display_customer")

    result = runner.invoke(customers_group, ["display"], input="1\n", obj=support_ctx)

    assert result.exit_code == 0
    assert "Affichage des détails d'un client" in result.output
    mock_display.assert_called_once_with(support_ctx["token"], "1")


def test_display_no_customers_available(runner, mocker, gestion_ctx, payload_gestion):
    mocker.patch("commands.utils.decode_token", return_value=payload_gestion)
    mocker.patch("commands.customers.get_customers", side_effect=ValueError("Clients introuvables."))

    result = runner.invoke(customers_group, ["display"], input="", obj=gestion_ctx, )

    assert result.exit_code == 0
    assert "Clients introuvables." in result.output
