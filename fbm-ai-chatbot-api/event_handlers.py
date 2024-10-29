from utils import invoke_lambda_function, logger
from config import CLASSIFIER_LAMBDA_ARN, CHATBOT_CONTROLLER_LAMBDA_ARN
import json

def handle_default_event(event_data, event_type) -> dict:
    message: str = event_data.get('message', '')
    logger.info(f"Invoking Lambda function with message: {message}")
    if not message:
        return {
            'statusCode': 200,
            'body': json.dumps({'responses': [{'message': '', 'buttons': {}}]}, ensure_ascii=False, indent=4)
        }
    classification_response = invoke_lambda_function(CLASSIFIER_LAMBDA_ARN, {'user_input': message})
    print(classification_response)
    classified_labels = [int(key) for key, value in classification_response.items() if value > 0.5]
    if not classified_labels:
        return {
            'statusCode': 200,
            'body': json.dumps({'responses': [{'message': 'Կա՞րող եք հստակեցնել ձեր հարցը։', 'buttons': {}}]},  ensure_ascii=False, indent=4)
        }
    chatbot_controller_response: dict = invoke_lambda_function(CHATBOT_CONTROLLER_LAMBDA_ARN, {'event_data': event_data, 'labels': classified_labels})
    decoded_response = json.loads(json.dumps(chatbot_controller_response), strict=False)
    return {
        'statusCode': 200,
        'body': json.dumps(decoded_response, ensure_ascii=False, indent=4)
    }
def handle_action_events(event_data, event_type) -> dict:
    chatbot_controller_response: dict = invoke_lambda_function(CHATBOT_CONTROLLER_LAMBDA_ARN, {'event_data': event_data, 'event_type': event_type})
    decoded_response = json.loads(json.dumps(chatbot_controller_response), strict=False)
    return {
        'statusCode': 200,
        'body': json.dumps(decoded_response, ensure_ascii=False, indent=4)
    }
    