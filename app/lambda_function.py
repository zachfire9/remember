import boto3
import json
import logging
import os

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    # Replace with your bucket name and file key
    bucket_name = os.getenv("BUCKET_NAME")
    file_key = os.getenv("FILE_KEY")
    
    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the content of the file
        file_content = response['Body'].read().decode('utf-8')
        
        # Log the content
        logger.info(f"Contents of the file: {file_key}:")
        logger.info(file_content)

        # Parse the JSON content
        json_data = json.loads(file_content)

        logger.info(f"Quote count: {json_data['count']}:")
        
        # Loop through the JSON data
        email_quote = ""
        index = 0
        while index < len(json_data['quotes']):
            if email_quote != "":
                break

            quote = json_data['quotes'][index]
            logger.info(f"Quote: {quote['count']}, Text: {quote['text']}")

            if quote['count'] == json_data['count'] - 1:
                quote['count'] += 1
                email_quote = quote['text']

            # Check if it's the last element
            if index == len(json_data['quotes']) - 1:
                json_data['count'] += 1

            index += 1

        response = client.send_email(
        Destination={
            'ToAddresses': [os.getenv("TO_ADDRESS")]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': email_quote,
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Quote of the Day',
            },
        },
        Source=os.getenv("SOURCE_ADDRESS")
        )
        
        logger.info(response)

        json_updated = json.dumps(json_data)

        s3_client.put_object(Body=json_updated, Bucket=bucket_name, Key=file_key)
        
        return {
            "statusCode": 200,
            "body": "File content logged successfully."
        }
    except Exception as e:
        logger.error(f"Error reading file from S3: {e}")
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
