import boto3
import logging
import json

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the Boto3 client outside the handler for better performance
lambda_client = boto3.client('lambda')

sagemaker_runtime = boto3.client('sagemaker-runtime')

def extract_event_details(event):
    event_type: str = event.get('event_type', 'default')
    event_data: dict = event.get('event_data', {})
    return event_type, event_data

def invoke_lambda_function(function_arn, payload):
    try:
        response = lambda_client.invoke(
            FunctionName=function_arn,
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read())
        return response_payload
    except Exception as e:
        logger.error(f"Error invoking Lambda function: {str(e)}")
        raise

def invoke_stt_endpoint(wav_bs64):
    endpoint_name = 'ASR'
    
    # Define the payload
    payload = {
        "audio": wav_bs64
    }
    
    # Convert the payload to JSON format
    payload_json = json.dumps(payload)
    
    # Invoke the endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=payload_json
    )
    
    # Parse the response
    result = json.loads(response['Body'].read().decode())

    return result
    