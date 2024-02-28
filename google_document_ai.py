from google.cloud import documentai_v1 as documentai
from constants import PROJECT_ID, PROCESSOR_ID
import base64
from datetime import datetime
import re

project_id = PROJECT_ID
location = 'us'
processor_id = PROCESSOR_ID

def get_lineitem_price(s):
    m = re.search(r'\d+\.\d+$', s)
    return float(m.group()) if m else None

def get_lineitem_name(s):
    m = re.search(r'^[%#]?(.*?)(?:\s+\d+\.\d+)?%?$', s)
    return m.group(1).strip() if m else None

def get_datetime(yyyy, mm, dd, hh, min) -> datetime:
    date = [yyyy, mm, dd]
    time = [hh, min]

    if all(v is not None for v in date) and all(v is not None for v in time):
        return datetime(yyyy, mm, dd, hh, min)
    elif all(v is not None for v in date):
        return datetime(yyyy, mm, dd)
    else:
        return

def get_ocr_document(
        project_id: str,
        location: str,
        file_path: str,
        mime_type: str,) -> documentai.types.document.Document:
    '''
    Uses Google's Document AI API for optical character recognition.
    Created and trained custom processor to read receipt data.
    Schema fields: abn, line_items, store_branch, store_name, total_price, transaction_datetime

    :param project_id:
    :param location:
    :param file_path:
    :param mime_type:
    :return: A canonical Document object (ie Document AI's output)
    '''

    opts = {
        "api_endpoint": f"{location}-documentai.googleapis.com"
    }

    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory, then load binary data
    with open(file_path, "rb") as image:
        image_content = image.read()
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
    # Optional: Additional configurations for processing.
    # process_options = documentai.ProcessOptions(
    #     # Process only specific pages
    #     individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
    #         pages=[1]
    #     )
    # )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        # process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document

def get_features_dict(document: documentai.types.document.Document) -> dict:
    '''
    Reads the text recognition output from the processor

    :param document: Output from Document AI API
    :return: Populated dictionary, containint: store name, store branch, abn, total price, transaction datetime and line items.
    '''

    receipt_dict = {
        'store_name': None,
        'store_branch': None,
        'abn': None,
        'total_price': None,
        'transaction_datetime': None,
        'line_items': [],
    }

    for entity in document.entities:
        if entity.type == 'store_name':
            receipt_dict['store_name'] = entity.mention_text
        elif entity.type == 'store_branch':
            receipt_dict['store_branch'] = entity.mention_text
        elif entity.type == 'abn':
            receipt_dict['abn'] = int(entity.normalized_value.text)  # first digit of ABN is always non-zero
        elif entity.type == 'total_price':
            receipt_dict['total_price'] = float(entity.normalized_value.money_value.units) + float(entity.normalized_value.money_value.nanos) / 10 ** 9
        elif entity.type == 'transaction_datetime':
            year = entity.normalized_value.datetime_value.year
            month = entity.normalized_value.datetime_value.month
            day = entity.normalized_value.datetime_value.day
            hour = entity.normalized_value.datetime_value.hours
            mins = entity.normalized_value.datetime_value.minutes
            receipt_dict['transaction_datetime'] = get_datetime(year,month,day,hour,mins)
        elif entity.type == 'line_items':
            price = get_lineitem_price(entity.mention_text)
            name = get_lineitem_name(entity.mention_text)
            receipt_dict['line_items'].append((name,price)) # append name & price pair tuple

        # print(entity)
        # print('===========\n\n')

    return receipt_dict

if __name__ == '__main__':
    file_path = 'Image/image7.jpg'
    mime_type = 'image/jpeg'
    doc = get_ocr_document(PROJECT_ID, location, file_path, mime_type)
    receipt_dict = get_features_dict(doc)
    print(receipt_dict)
