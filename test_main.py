from main import Transaction

def test_valid_transaction():
    tx = Transaction(
        transaction_id="123",
        amount=100.0,
        currency="USD",
        region="NA"
    )
    assert tx.amount == 100.0

def test_invalid_currency():
    try:
        Transaction(transaction_id="123", amount=100.0, currency="YEN", region="NA")
    except Exception as e:
        assert "Unsupported currency" in str(e)
