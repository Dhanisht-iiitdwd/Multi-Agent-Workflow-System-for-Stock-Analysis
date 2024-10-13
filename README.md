# Stock Analysis Workflow

This project implements an automated workflow for analyzing stock performance using AWS services. It identifies the top 10 performing stocks over the last 3 months, fetches their data, normalizes prices, and determines the best performer.

## Project Structure

```
stock-analysis-project/
│
├── lambda_functions/
│   ├── stock_search_lambda.py
│   ├── data_fetching_lambda.py
│   └── data_analysis_lambda.py
│
├── step_functions/
│   └── workflow_definition.json
│
├── aws_config/
│   ├── eventbridge_rule.json
│   └── s3_lifecycle_rule.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

1. Clone this repository:
   ```
   git clone- Clone this git repository
   cd stock-analysis-project
   ```

2. Set up a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up AWS CLI and configure your AWS credentials.

4. Create an S3 bucket for storing stock data.

5. Create a DynamoDB table named `StockPerformanceReports` with a partition key `Date` of type String.

6. Create an SQS queue for email notifications.

7. Set up a Google Custom Search Engine and obtain the API key and Search Engine ID.

## AWS Configuration

1. Create Lambda functions:
   - Upload each Python file from the `lambda_functions/` directory as a separate Lambda function.
   - Set the handler to `<filename>.lambda_handler` for each function.
   - Set appropriate IAM roles with necessary permissions for each Lambda function.

2. Set up Step Functions:
   - Use the `step_functions/workflow_definition.json` to create a new state machine.
   - Update the ARNs in the definition to match your Lambda function ARNs.

3. Configure EventBridge:
   - Use `aws_config/eventbridge_rule.json` to create a new rule that triggers the Step Functions workflow every 5 days.

4. Set up S3 Lifecycle Rules:
   - Apply the configuration in `aws_config/s3_lifecycle_rule.json` to your S3 bucket.

## Environment Variables

Set the following environment variables in your Lambda functions:

- `GOOGLE_API_KEY`: Your Google Custom Search API key
- `GOOGLE_CSE_ID`: Your Custom Search Engine ID
- `S3_BUCKET_NAME`: Name of your S3 bucket for storing stock data
- `SQS_QUEUE_URL`: URL of your SQS queue for email notifications

## Running the Workflow

The workflow will run automatically every 5 days as per the EventBridge rule. To run it manually:

1. Go to the AWS Step Functions console.
2. Select your state machine.
3. Click "Start execution".

## Monitoring and Logging

- Use AWS CloudWatch to monitor the execution of your Lambda functions and Step Functions workflow.
- Check the CloudWatch Logs for each Lambda function for detailed execution logs.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
