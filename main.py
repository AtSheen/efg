from pydantic import BaseModel
import requests
import uvicorn
import sys
from typing import Optional, Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import tax_code_helpers as tch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/assets", StaticFiles(directory="public/assets"), name="static")

# @app.get("/favicon.png", response_class=FileResponse)
# async def favicon_png():
#     return FileResponse("public/favicon.png")


# @app.get("/", response_class=FileResponse)
# async def main():
#     return "public/index.html"


class TaxCodePredictionRequest(BaseModel):
    """
    Data model for a tax code prediction request.

    Attributes:
    -----------
    pID : str
        A unique identifier for the prediction request.
    companyCode : str
        The company code related to the prediction.
    vendorNumber : str
        The vendor number related to the prediction.
    vatRate : str
        The VAT rate to be used in the prediction.
    isReverseCharge : Optional[bool]
        Indicates if reverse charge applies (default is None).
    goods : Optional[bool]
        Indicates if the prediction involves goods (default is None).
    services : Optional[bool]
        Indicates if the prediction involves services (default is None).
    apAr : str
        Indicates whether the prediction is related to AP (Accounts Payable), AR (Accounts Receivable), or FI (Financial Accounting). Defaults to "AP".
    """
    pID: str
    companyCode: str
    vendorNumber: str
    vatRate: str
    isReverseCharge: Optional[bool] = None
    goods: Optional[bool] = None
    services: Optional[bool] = None
    apAr: str = "AP"



def create_payload_for_tax_code_prediction(
    parsed_query: Dict[str, str],
    filtered_tax_codes: List[str]
) -> Dict[str, any]:
    """
    Create a payload for tax code prediction based on the parsed query and filtered tax codes.

    Parameters:
    -----------
    parsed_query : Dict[str, str]
        A dictionary containing the query parameters for the prediction.
    filtered_tax_codes : List[str]
        A list of strings representing the filtered tax codes.

    Returns:
    --------
    Dict[str, any]:
        A dictionary containing the payload with the query data and filtered tax codes.
    """

    # Log the start of payload creation
    logging.info("Creating payload for tax code prediction.")

    # Generate the DataFrame for prediction
    data = tch.get_data_frame_for_prediction(parsed_query)
    
    # Convert the DataFrame to a dictionary record
    data_record = data.to_dict(orient='records')[0]
    
    # Map the DataFrame fields to the function app fields
    data_payload = {
        tch.function_app_field_mapper.get(col, col): data_record[col]
        for col in data_record
    }
    
    # Create the final payload
    payload = {
        "query": data_payload,
        "filtered_tax_codes": filtered_tax_codes
    }
    
    # Log the created payload (be cautious about sensitive information)
    logging.debug(f"Created payload: {payload}")

    return payload

@app.post("/get_tax_code_prediction")
async def get_tax_code_prediction(request: TaxCodePredictionRequest):
    """
    Endpoint to get tax code prediction based on the request data.

    Parameters:
    -----------
    request : TaxCodePredictionRequest
        The request object containing parameters for tax code prediction.

    Returns:
    --------
    JSONResponse:
        A JSON response containing the tax code prediction and related data.
    """
    try:
        parsed_query = tch.query_parser(
            company_code=request.companyCode,
            vendor_number=request.vendorNumber,
            is_reverse_charge=request.isReverseCharge,
            goods=request.goods,
            services=request.services,
            vat_rate=request.vatRate,
            ap_ar=request.apAr,
        )

        logging.info("Parsed query: %s", parsed_query)

        # Get filtered tax codes DataFrame
        filtered_tax_codes_df = tch.get_tax_code_static_filtered_df(parsed_query)

        # Create payload for tax code prediction
        payload = create_payload_for_tax_code_prediction(parsed_query=parsed_query, filtered_tax_codes=filtered_tax_codes_df['Tax code'].tolist())
        logging.info("Payload created for prediction: %s", payload)
        
        # Make POST request to external function app
        request_url = f'{tch.FUNCTION_APP_BASE_URL}/api/GetTaxCode?code={tch.FUNCTION_APP_KEY}'
        response = requests.post(request_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the response from the external function app
        response = response.json()
        response['ml_prediction_proba_df'] = [{'Tax Code': i['Tax Code'], 'prob': round(i['prob'], 2)} for i in response['ml_prediction_proba_df'][:5]]

        # Prepare the final response
        response = {
            "reportingName": parsed_query["reporting_name"],
            "vendorName": parsed_query["vendor_name"],
            "taxCodeTableColumns": filtered_tax_codes_df.columns.to_list(),
            "filtered_tax_codes": json.loads(
                filtered_tax_codes_df.to_json(orient="records")
            ),
            "predictedTaxCode": response['ml_prediction'],
            "confidenceScore": round(response['ml_prediction_proba'], 2),
            "probsTableColumns": ["Tax Code", "Probability"],
            "taxCodePredictionProbabilities": response['ml_prediction_proba_df'],
        }
        logging.info("Response prepared: %s", response)
        return JSONResponse(content=response)
    
    except requests.RequestException as e:
        logging.error("HTTP request error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Error in external service request")
    
    except Exception as e:
        logging.error("Unexpected error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/get_attention_list_table")
def get_attention_list_table():
    """
    Retrieve the attention list table from the DataFrame and return it as JSON.

    Returns:
    --------
    JSONResponse:
        A JSON response containing the table columns and the records of the attention list.
    """

    # Log the request handling
    logging.info("Handling request for attention list table.")
    attention_df = tch.attention_list_df.copy()
    attention_df = attention_df.rename(columns={'Company code': 'Company Code'})
    response = {
        "tableColumns": attention_df.columns.to_list(),
        "attentionList": json.loads(attention_df.to_json(orient="records")),
    }

    return JSONResponse(content=response)


@app.get("/get_vat_ip_table")
def get_vat_ip_table():
    """
    Retrieve the VAT-IP table from the DataFrame and return it as JSON.

    Returns:
    --------
    JSONResponse:
        A JSON response containing the table columns and the records of the VAT-IP table.
    """

    # Log the request handling
    logging.info("Handling request for VAT-IP table.")
    
    ip_vat_df = tch.ip_vat_df.copy()
    response = {
        "tableColumns": ip_vat_df.columns.to_list(),
        "ipVatList": json.loads(ip_vat_df.to_json(orient="records")),
    }
    return JSONResponse(content=response)

@app.get("/get_historical_meta_table")
def get_historical_meta_table():
    """
    Retrieve the historical meta table from the DataFrame and return it as JSON.

    Returns:
    --------
    JSONResponse:
        A JSON response containing the table columns and the records of the historical meta table.
    """

    # Log the request handling
    logging.info("Handling request for historical meta table.")

    historical_meta_df = tch.historical_meta.copy()
    response = {
        "tableColumns": historical_meta_df.columns.to_list(),
        "historicalMeta": json.loads(historical_meta_df.to_json(orient="records")),
    }
    return JSONResponse(content=response)



# app.mount("/", StaticFiles(directory="public", html=True))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "dev" | "--dev" | "-d" | "development":
                print("Development")
                uvicorn.run("main:app", port=8000, reload=True)
    else:
        print("Production")
        uvicorn.run(
            "main:app", host="0.0.0.0", port=8000, log_level="info", reload=False
        )
