import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_favicon_png():
    response = client.get("/favicon.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_main_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_get_tax_code_prediction():
    request_data = {
        "pID": "123456",
        "companyCode": "1027",
        "vendorNumber": "373458",
        "vatRate": "0",
        "isReverseCharge": False,
        "goods": True,
        "services": False,
        "apAr": "AP"
    }

    response = client.post("/get_tax_code_prediction", json=request_data)
    assert response.status_code == 200
    
    response_data = response.json()
    assert "reportingName" in response_data
    assert "vendorName" in response_data
    assert "taxCodeTableColumns" in response_data
    assert "filtered_tax_codes" in response_data
    assert "predictedTaxCode" in response_data
    assert "confidenceScore" in response_data
    assert "probsTableColumns" in response_data
    assert "taxCodePredictionProbabilities" in response_data

def test_get_attention_list_table():

    response = client.get("/get_attention_list_table")
    assert response.status_code == 200
    
    response_data = response.json()
    assert "tableColumns" in response_data
    assert "attentionList" in response_data

def test_get_vat_ip_table():

    response = client.get("/get_vat_ip_table")
    assert response.status_code == 200
    
    response_data = response.json()
    assert "tableColumns" in response_data
    assert "ipVatList" in response_data

def test_get_historical_meta_table():

    response = client.get("/get_historical_meta_table")
    assert response.status_code == 200
    
    response_data = response.json()
    assert "tableColumns" in response_data
    assert "historicalMeta" in response_data