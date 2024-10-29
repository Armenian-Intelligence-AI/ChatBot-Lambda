import os

def lambda_handler(event, context):
    # Retrieve the API key from environment variables
    expected_api_key = os.getenv('API_KEY')
    
    # Get the API key from the incoming request headers
    api_key = event['headers'].get('x-api-key')
    
    if not api_key:
        return generate_policy('Deny', event['routeArn'])
    
    # Compare the API keys
    if api_key == expected_api_key:
        return generate_policy('Allow', event['routeArn'])
    else:
        return generate_policy('Deny', event['routeArn'])

def generate_policy(effect, resource):
    # Generate a policy allowing or denying access
    policy_document = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }
        ]
    }
    return {
        'principalId': 'user',
        'policyDocument': policy_document
    }
