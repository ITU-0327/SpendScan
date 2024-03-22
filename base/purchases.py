import requests
import sys
import constants

header_payload = {'Authorization': f'Bearer {constants.YX_UP_PAT}',}

up_api_endpoint = 'https://api.up.com.au/api/v1'

def get_transactions():
    query_params = {'filter[since]':'2024-03-01T00:00:00+11:00',
                    'filter[until]':'2024-03-13T23:59:59+11:00'}
    response = requests.get(f'{up_api_endpoint}/transactions',headers=header_payload, params=query_params)
    with open('purchases_response.json', 'w') as f:
        f.write(str(response.json()))
    return response.json()

def get_transaction(transaction_id: str):
    response = requests.get(f'{up_api_endpoint}/transactions/{transaction_id}', headers=header_payload)
    print(str(response.json()))

if __name__ == '__main__':
    w_transaction = get_transaction('5e058479-4721-4c85-bf79-f0c74b82716e')

    transactions_payload = get_transactions()
    transactions = transactions_payload['data']
    print(len(transactions))
    for transaction in transactions:
        id = transaction['id']

        merchant_rawtext = transaction['attributes']['rawText']
        merchant_description = transaction['attributes']['description']
        message = transaction['attributes']['message']
        currency_code = transaction['attributes']['amount']['currencyCode']
        value = transaction['attributes']['amount']['valueInBaseUnits']/100
        date = transaction['attributes']['createdAt']
        if transaction['relationships']['category']['data'] is None:
            category = None
        else:
            category = transaction['relationships']['category']['data']['id']

        print(id)
        print(f'{merchant_description} | {merchant_rawtext}')
        print(message)
        print(currency_code, value)
        print(date)
        print(category)
        print('===============\n')



    # print(sys.path)
