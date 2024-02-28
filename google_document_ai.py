from google.cloud import documentai_v1 as documentai
import base64
from datetime import datetime
import re

def get_lineitem_price(s):
    m = re.search(r'\d+\.\d+$', s)
    return float(m.group()) if m else None

def get_lineitem_name(s):
    m = re.search(r'^[%#]?(.*?)(?:\s+\d+\.\d+)?%?$', s)
    return m.group(1).strip() if m else None


project_id = 'secret'
location = 'us'
processor_id = 'secret'

file_path = 'Image/image7.jpg'
mime_type = 'image/jpeg'

opts = {
    "api_endpoint": f"{location}-documentai.googleapis.com"
}

client = documentai.DocumentProcessorServiceClient(client_options=opts)

name = client.processor_path(project_id, location, processor_id)

with open(file_path, "rb") as image:
    image_content = image.read()

# Load binary data
raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

# For more information: https://cloud.google.com/document-ai/docs/reference/rest/v1/ProcessOptions
# Optional: Additional configurations for processing.
process_options = documentai.ProcessOptions(
    # Process only specific pages
    individual_page_selector=documentai.ProcessOptions.IndividualPageSelector(
        pages=[1]
    )
)

# Configure the process request
request = documentai.ProcessRequest(
    name=name,
    raw_document=raw_document,
    process_options=process_options,
)

result = client.process_document(request=request)

# For a full list of `Document` object attributes, reference this page:
# https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
document = result.document

# Read the text recognition output from the processor
# print("The document contains the following text:")
# print(document.entities)

receipt_dict = {
    'store_name': None,
    'store_branch': None,
    'abn': None,
    'total_price': None,
    'transaction_datetime': None,
    'line_items': [],
}


for entity in document.entities:
    # print(entity)
    type_name = entity.type
    mention_text = entity.mention_text
    normalized_value = entity.normalized_value if entity.normalized_value else None

    print(entity)

    if entity.type == 'store_name':
        receipt_dict['store_name'] = entity.mention_text
    elif entity.type == 'store_branch':
        receipt_dict['store_branch'] = entity.mention_text
    elif entity.type == 'abn':
        receipt_dict['abn'] = int(entity.normalized_value.text)  # first digit of ABN is always non-zero
    elif entity.type == 'total_price':
        receipt_dict['total_price'] = float(entity.normalized_value.money_value.units) + float(entity.normalized_value.money_value.nanos) / 10 ** 9
    elif entity.type == 'transaction_datetime':
        yyyy = entity.normalized_value.datetime_value.year
        mm = entity.normalized_value.datetime_value.month
        dd = entity.normalized_value.datetime_value.day
        hh = entity.normalized_value.datetime_value.hours
        min = entity.normalized_value.datetime_value.minutes
        date = [yyyy,mm,dd]
        time = [hh,min]

        if all(v is not None for v in date) and all(v is not None for v in time):
            dt = datetime(yyyy, mm, dd, hh, min)
        elif all(v is not None for v in date):
            dt = datetime(yyyy, mm, dd)
        else:
            dt = None

        receipt_dict['transaction_datetime'] = dt

    elif entity.type == 'line_items':
        price = get_lineitem_price(entity.mention_text)
        name = get_lineitem_name(entity.mention_text)
        receipt_dict['line_items'].append((name,price))

    print('===========\n\n')



print(receipt_dict)

'''
abn: int
line_items: str
store_branch: str
store_name: str
total_price: float
transaction_datetime: ?
'''
