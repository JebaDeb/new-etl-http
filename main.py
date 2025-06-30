from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from datetime import datetime
from google.cloud import bigquery
import os

app = FastAPI()

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    currency: str
    region: str

    @validator("currency")
    def validate_currency(cls, v):
        if v not in ["USD", "EUR", "GBP"]:
            raise ValueError("Unsupported currency")
        return v

@app.post("/ingest")
async def ingest(transaction: Transaction):
    tax_rate = 0.3
    tax = round(transaction.amount * tax_rate, 2)
    enriched = {
        "transaction_id": transaction.transaction_id,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "region": transaction.region,
        "tax": tax,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Load into BigQuery
    client = bigquery.Client()
    table_id = os.environ["BQ_TABLE_ID"]
    errors = client.insert_rows_json(table_id, [enriched])
    if errors:
        raise HTTPException(status_code=500, detail=str(errors))

    return {"status": "success", "data": enriched}
