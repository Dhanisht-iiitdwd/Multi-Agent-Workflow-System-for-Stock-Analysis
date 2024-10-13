#Firts import important libs
import boto3
import json
import re
from googleapiclient.discovery import build
import yfinance as yf

def lambda_handler(event, context):
    # Utilizzing gogle Search API 
    api_key = "GOOGLE_API_KEY"
    cse_id = "CUSTOM_SEARCH_ENGINE_ID"
    
    service = build("customsearch", "v1", developerKey=api_key)
    
    # Now search for top performing stocks
    query = "top performing stocks last 3 months"
    result = service.cse().list(q=query, cx=cse_id, num=10).execute()
    
    # Extract stock symbols from search results
    stock_symbols = extract_stock_symbols(result['items'])
    
    # And then Trigger Data Fetching Lambda
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(
        FunctionName='data-fetching-lambda',
        InvocationType='Event',
        Payload=json.dumps({'stock_symbols': stock_symbols})
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Initiated data fetching for {len(stock_symbols)} stocks')
    }

def extract_stock_symbols(search_items):
    potential_symbols = set()
    
    # For now i am using RegX- (or even we can build some other logic as well - Regular expression for common stock symbol formats
    symbol_pattern = re.compile(r'\b[A-Z]{1,5}\b')
    
    for item in search_items:
         
        text = item['title'] + ' ' + item['snippet']
        symbols = symbol_pattern.findall(text)
        potential_symbols.update(symbols)
    
    
    valid_symbols = validate_symbols(potential_symbols)
    
    # Limit to top 10 symbols
    return list(valid_symbols)[:10]

def validate_symbols(symbols):
    valid_symbols = set()
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            if 'symbol' in info and info['symbol'] == symbol:
                valid_symbols.add(symbol)
        except:
            # If there's any error, I assume it's not a valid symbol and just paas the loop
            pass
    return valid_symbols
