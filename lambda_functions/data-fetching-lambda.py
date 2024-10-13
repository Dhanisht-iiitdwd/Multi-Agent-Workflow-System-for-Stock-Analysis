import boto3
import yfinance as yf
import pandas as pd
from io import StringIO
import json

def lambda_handler(event, context):
    stock_symbols = event['stock_symbols']
    
    s3 = boto3.client('s3')
    bucket_name = 'expedite-comm-stock-data-bucket'  
    
    for symbol in stock_symbols:
        # Fetch stock dataa
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")
        
        # Saving to S3 buket 
        csv_buffer = StringIO()
        hist.to_csv(csv_buffer)
        s3.put_object(Bucket=bucket_name, Key=f"{symbol}.csv", Body=csv_buffer.getvalue())
    
    # And then Trigger Data Analysis Lambda function
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(
        FunctionName='data-analysis-lambda',
        InvocationType='Event',
        Payload=json.dumps({'bucket': bucket_name, 'symbols': stock_symbols})
    )
    
    return {
        'statusCode': 200,
        'body': f'Fetched and saved data for {len(stock_symbols)} stocks'
    }
