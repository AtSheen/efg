import numpy as np
import pandas as pd
import joblib
import logging
import requests
import os
from io import BytesIO
from typing import Tuple, Optional, Union, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging = logging.getLogger(__name__)

eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'SE', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'DK']
FUNCTION_APP_BASE_URL = os.getenv('AZURE_FUNCTION_APP_URL','http://127.0.0.1:8000')
FUNCTION_APP_KEY = os.getenv('AZURE_FUNCTION_APP_KEY','')


endpoint_config = {
    'categorical_config': 'GetCategoricalConfigFile',
    'legal_entities': 'GetLegalEntitiesFile',
    'tax_code_info': 'GetTaxCodeInfoFile',
    'tax_code_description': 'GetTaxCodeDescriptionFile',
    'company_code_info': 'GetCompanyCodeDetailsFile',
    'vendor_info': 'GetVendorDetailsFile',
    'attention_list': 'GetAttentionListFile',
    'ip_vat_issues': 'GetIPVatFile',
    'historical_meta': 'GetHistoricalMetaFile'
}

function_app_field_mapper = {
    'Company Code': 'company_code',
    'Vendor Number': 'vendor_number',
    'VAT Rate': 'vat_rate',
    'AP/AR/FI': 'ap_ar',
    'Reverse Charge': 'is_reverse_charge',
    'Legal Entity': 'legal_entity',
    'Goods/Services': 'goods_services',
    'EU/NON EU': 'eu_noneu',
    'Domestic/ Foreign': 'domestic_foreign'
}


def load_categorical_config_file_from_blob():
    logging.info(f"Loading categorical config from azure blob")
    endpoint = endpoint_config['categorical_config']
    request_url = f'{FUNCTION_APP_BASE_URL}/api/{endpoint}?code={FUNCTION_APP_KEY}'
    response = requests.get(request_url)
    # Load the joblib file from the response content
    joblib_file = BytesIO(response.content)
    config = joblib.load(joblib_file)
    return config

def load_df_from_blob(endpoint):
    logging.info(f"Loading {endpoint} from azure blob")
    request_url = f'{FUNCTION_APP_BASE_URL}/api/{endpoint}?code={FUNCTION_APP_KEY}'
    response = requests.get(request_url)
    file_content = BytesIO(response.content)
    df = pd.read_csv(file_content)
    logging.info(f"Loaded {endpoint} from azure blob")
    return df


# Load Files to memory
# category_config = load_categorical_config_file_from_blob()
# tax_code_static_df = load_df_from_blob(endpoint=endpoint_config['tax_code_info'])
# same_legal_entity = load_df_from_blob(endpoint=endpoint_config['legal_entities'])
# concatenated_tax_description = load_df_from_blob(endpoint=endpoint_config['tax_code_description'])
# company_code_df = load_df_from_blob(endpoint=endpoint_config['company_code_info'])
# vendor_country_df = load_df_from_blob(endpoint=endpoint_config['vendor_info'])
# attention_list_df = load_df_from_blob(endpoint=endpoint_config['attention_list'])
# ip_vat_df = load_df_from_blob(endpoint=endpoint_config['ip_vat_issues'])
# historical_meta = load_df_from_blob(endpoint=endpoint_config['historical_meta'])


def get_reporting_country(company_code: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Retrieve the reporting country and company name for a given company code.

    Parameters:
    -----------
    company_code : str
        The code of the company to lookup.

    Returns:
    --------
    Tuple[Optional[str], Optional[str]]:
        A tuple containing the reporting country and company name if found, 
        otherwise (None, None).

    Logs:
    -----
    Logs the process of searching for the company code and whether it was found.
    """

    logging.info(f"Looking up reporting country for company code: {company_code}")

    # Filter the DataFrame for the given company code
    temp_company_code_df = company_code_df[company_code_df['Company Code'] == company_code].copy()

    if not temp_company_code_df.empty:
        reporting_country = temp_company_code_df['Reporting Country'].values[0]
        reporting_name = temp_company_code_df['Company Name'].values[0]
        logging.info(f"Found company: {reporting_name}, reporting country: {reporting_country}")
    else:
        reporting_country = None
        reporting_name = None
        logging.warning(f"No data found for company code: {company_code}")

    return reporting_country, reporting_name


def get_vendor_details(vendor: str):
    """
    Retrieve the country key and vendor name for a given vendor identifier.

    Parameters:
    -----------
    vendor : str
        The identifier of the vendor to look up.

    Returns:
    --------
    Tuple[Union[str, np.nan], str]:
        A tuple containing the country key and vendor name if found, 
        otherwise (np.nan, 'Vendor details not found').

    Logs:
    -----
    Logs the process of searching for the vendor identifier and whether it was found.
    """

    logging.info(f"Looking up vendor details for vendor: {vendor}")

    # Create a copy of the DataFrame and filter for the given vendor
    vendor_country_df_copy = vendor_country_df.copy()
    filtered_vendor_country_df_copy = vendor_country_df_copy[vendor_country_df_copy['Vendor'].astype(str) == str(vendor)]

    if not filtered_vendor_country_df_copy.empty:
        vendor_country = filtered_vendor_country_df_copy['Country Key'].values[0]
        vendor_name = filtered_vendor_country_df_copy['Vendor Name'].values[0]
        logging.info(f"Found vendor: {vendor_name}, country key: {vendor_country}")
    else:
        vendor_country = np.nan
        vendor_name = 'Vendor details not found'
        logging.warning(f"No details found for vendor: {vendor}")

    return vendor_country, vendor_name


def check_if_same_legal_entity(company_code: str, vendor: str) -> str:
    """
    Check if the provided company code and vendor number are both present 
    in the same legal entity data.

    Parameters:
    -----------
    company_code : str
        The company code to check.
    vendor : str
        The vendor number to check.

    Returns:
    --------
    str:
        'Same' if both the company code and vendor number are present 
        in the same legal entity data; otherwise, 'Different'.

    Logs:
    -----
    Logs the process of checking the company code and vendor number 
    against the same legal entity data.
    """

    logging.info(f"Checking if company code '{company_code}' and vendor '{vendor}' are in the same legal entity data.")

    # Convert the inputs to string and check if they are in the DataFrame
    company_code_str = str(company_code)
    vendor_str = str(vendor)
    
    cc_in_legal_entity = company_code_str in same_legal_entity['Company Code'].astype(str).values
    vendor_in_legal_entity = vendor_str in same_legal_entity['Vendor Number'].astype(str).values
    
    if cc_in_legal_entity and vendor_in_legal_entity:
        logging.info(f"Both company code '{company_code}' and vendor '{vendor}' are in the same legal entity data.")
        return 'Same'
    else:
        logging.info(f"Company code '{company_code}' and vendor '{vendor}' are not both in the same legal entity data.")
        return 'Different'


def get_goods_services(goods: Optional[bool], services: Optional[bool]) -> str:
    """
    Determine the type of offering based on the availability of goods and services.

    Parameters:
    -----------
    goods : Optional[bool]
        A boolean indicating the presence of goods. Can be None, True, or False.
    services : Optional[bool]
        A boolean indicating the presence of services. Can be None, True, or False.

    Returns:
    --------
    str:
        A string representing the type of offering based on the availability of goods and/or services.

    Examples:
    ---------
    >>> get_goods_services(True, False)
    'Goods'
    >>> get_goods_services(False, True)
    'Services'
    >>> get_goods_services(True, True)
    'Goods/Services'
    >>> get_goods_services(None, None)
    'Goods/Services'
    """

    # Log the input parameters (optional)
    logging.info(f"Determining offering type with goods={goods} and services={services}")

    if goods and services:
        return 'Goods/Services'
    elif goods:
        return 'Goods'
    elif services:
        return 'Services'
    return 'Goods/Services'

def get_data_frame_for_prediction(parsed_query):
    """
    Generate a DataFrame for prediction based on the provided parsed query.

    Parameters:
    -----------
    parsed_query : Dict[str, str]
        A dictionary containing parsed query parameters with keys corresponding 
        to feature names and values as strings representing the feature values.

    Returns:
    --------
    pd.DataFrame:
        A DataFrame with the features in the correct categorical format for model prediction.
    """
    # Create a DataFrame from the parsed query
    data = {
        'Company Code': parsed_query['company_code'],
        'Vendor Number': parsed_query['vendor_number'],
        'AP/AR/FI': parsed_query['ap_ar'],
        'VAT Rate': parsed_query['vat_rate'],
        'Reverse Charge': parsed_query['is_reverse_charge'],
        'EU/NON EU': parsed_query['eu_noneu'],
        'Goods/Services': parsed_query['goods_services'],
        'Domestic/ Foreign': parsed_query['domestic_foreign'],
        'Legal Entity': parsed_query['legal_entity']
    }

    df = pd.DataFrame([data])
    df = df[category_config['feature_names']]

    # Reorder and convert columns to categorical
    for col in df.columns:
        df[col] = pd.Categorical(df[col], categories=[str(i) for i in category_config[col]])

    # Log the shape of the DataFrame and its columns
    logging.info(f"Generated DataFrame for prediction with shape: {df.shape}")
    logging.info(f"DataFrame columns: {df.columns.tolist()}")
    return df


def get_tax_code_static_filtered_df(parsed_query: Dict[str, str]) -> pd.DataFrame:
    """
    Filter tax code descriptions based on the provided query parameters.

    Parameters:
    -----------
    parsed_query : Dict[str, str]
        A dictionary containing the query parameters for filtering the tax codes.
        Keys should include 'reporting_country', 'goods_services', 'is_reverse_charge', 
        'vat_rate', and 'eu_noneu'.

    Returns:
    --------
    pd.DataFrame:
        A DataFrame containing the tax code descriptions that match the filter criteria.

    Raises:
    -------
    KeyError:
        If any expected key is missing from the parsed_query dictionary.
    """

    # Log the start of the filtering process
    logging.info("Filtering tax codes based on the parsed query parameters.")

    filtered_tax_codes_df = tax_code_static_df[tax_code_static_df['Country'] == parsed_query['reporting_country']]
    filtered_tax_codes_df = filtered_tax_codes_df[filtered_tax_codes_df['Goods/Services'].isin([parsed_query['goods_services'], 'Goods/Services'])]
    filtered_tax_codes_df = filtered_tax_codes_df[filtered_tax_codes_df['Reverse Charge'].astype(str) == parsed_query['is_reverse_charge'].capitalize()]
    filtered_tax_codes_df = filtered_tax_codes_df[filtered_tax_codes_df['VAT Rate in Invoice copy'].astype(str) == str(parsed_query['vat_rate'])]

    # Filter tax descriptions
    tax_code_description = concatenated_tax_description[
        concatenated_tax_description['Tax code'].isin(filtered_tax_codes_df['Tax Code'].unique().tolist())
    ]
    tax_code_description.loc[:, 'Description']  = tax_code_description['Description'].str.replace('\\n', '. ')

    # Log the results of filtering
    logging.info(f"Filtered tax code descriptions with {len(tax_code_description)} entries.")
    
    return tax_code_description


def query_parser(company_code, vendor_number, is_reverse_charge, goods, services, vat_rate, ap_ar) -> dict:
    """
    Parse and generate a query dictionary based on the provided parameters.

    Parameters:
    -----------
    company_code : str
        The company code for the query.
    vendor_number : str
        The vendor number for the query.
    is_reverse_charge : bool
        Whether reverse charge applies (True/False).
    goods : Optional[bool]
        Whether goods are included in the query.
    services : Optional[bool]
        Whether services are included in the query.
    vat_rate : str
        The VAT rate to be used in the query.
    ap_ar : str
        Indicates whether the query is related to AP, AR, or FI.

    Returns:
    --------
    dict:
        A dictionary with parsed query parameters including additional 
        information such as reporting country, vendor details, legal entity, 
        and classification of goods/services.
    """
    # Log the start of the parsing process
    logging.info("Starting query parsing.")

    # Parse and generate the query dictionary
    parsed_query = dict()
    parsed_query['company_code'] = company_code
    parsed_query['vendor_number'] = vendor_number
    parsed_query['vat_rate'] = vat_rate
    parsed_query['ap_ar'] = ap_ar
    parsed_query['reporting_country'], parsed_query['reporting_name'] = get_reporting_country(company_code)
    parsed_query['vendor_country'], parsed_query['vendor_name'] = get_vendor_details(vendor=vendor_number)
    parsed_query['is_reverse_charge'] = str(is_reverse_charge)
    parsed_query['legal_entity'] = check_if_same_legal_entity(company_code=company_code, vendor=vendor_number)
    parsed_query['goods_services'] = get_goods_services(goods=goods, services=services)
    parsed_query['eu_noneu'] = 'EU' if parsed_query['vendor_country'] in eu_countries else 'Non EU'
    parsed_query['domestic_foreign'] = 'Domestic' if parsed_query['vendor_country'] == parsed_query['reporting_country'] else 'Foreign'
    
    # Log the completed parsed query
    logging.info(f"Parsed query generated: {parsed_query}")
    return parsed_query
