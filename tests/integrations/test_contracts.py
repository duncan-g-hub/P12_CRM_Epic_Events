import pytest
from controllers.contracts import (
    create_contract,
    update_contract,
    display_contract,
    get_contracts,
)

# create
def test_create_contract(db_session, gestion_token, customer):
    contract = create_contract(
        token=gestion_token,
        customer_id=customer.id,
        total_amount=1000,
        amount_to_pay=200,
        signed=False
    )

    assert contract.id is not None
    assert contract.total_amount == 1000


def test_create_contract_invalid_amount(db_session, gestion_token, customer):
    with pytest.raises(ValueError):
        create_contract(
            token=gestion_token,
            customer_id=customer.id,
            total_amount=1000,
            amount_to_pay=2000,
            signed=False
        )

# update
def test_update_contract(db_session, gestion_token, signed_contract):
    updated = update_contract(
        token=gestion_token,
        contract_id=signed_contract.id,
        customer_id=None,
        total_amount=1500,
        amount_to_pay=300,
        signed=True
    )

    assert updated.total_amount == 1500


def test_unsign_signed_contract(db_session, gestion_token, signed_contract):
    with pytest.raises(ValueError):
        update_contract(
            token=gestion_token,
            contract_id=signed_contract.id,
            customer_id=None,
            total_amount=None,
            amount_to_pay=None,
            signed=False
        )

# display
def test_display_contract(db_session, gestion_token, signed_contract, capsys):
    display_contract(gestion_token, signed_contract.id)

    out = capsys.readouterr().out
    assert str(signed_contract.id) in out or "client" in out

# get
def test_get_contracts(db_session, signed_contract):
    result, ids = get_contracts()

    assert str(signed_contract.id) in ids
