import boto3
import pandas as pd
import json
from io import StringIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    
    bucket = event['bucket']
    symbols = event['symbols']
    
    best_performer = None
    max_return = float('-inf')
    
    for symbol in symbols:
        # Reead CSV from S3
        csv_obj = s3.get_object(Bucket=bucket, Key=f"{symbol}.csv")
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string), index_col=0)
        
        # Normalizationn- Normalize prices
        df['Normalized_Close'] = df['Close'] / df['Close'].iloc[0]
        
        # Calculating return using normalized prices
        start_price = df['Normalized_Close'].iloc[0]
        end_price = df['Normalized_Close'].iloc[-1]
        stock_return = (end_price - start_price) / start_price
        
        if stock_return > max_return:
            max_return = stock_return
            best_performer = symbol
        
        # Now, Saveing normalized data back to S3 buckect
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3.put_object(Bucket=bucket, Key=f"{symbol}_normalized.csv", Body=csv_buffer.getvalue())
    
    # and Saving results to DDB
    table = dynamodb.Table('StockPerformanceReports')
    table.put_item(
        Item={
            'Date': pd.Timestamp.now().strftime('%Y-%m-%d'),
            'BestPerformer': best_performer,
            'Return': str(max_return)
        }
    )
    
    # extra implemented- Send message to SQS for email notification
    sqs = boto3.client('sqs')
    sqs.send_message(
        QueueUrl='YOUR_SQS_QUEUE_URL',
        MessageBody=json.dumps({
            'subject': 'Stock Performance Report',
            'body': f'The best performing stock over the last 3 months was {best_performer} with a return of {max_return:.2%}'
        })
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Analysis complete. Best performer: {best_performer}')
    }
