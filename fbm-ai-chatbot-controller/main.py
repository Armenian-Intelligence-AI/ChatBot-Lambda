from mappings import LABEL_HANDLERS, ACTION_HANDLERS
from config import logger, PRIORITY_LABELS, dynamodb_client, NOT_PRIORITY_LABELS
from utils import log_to_dynamodb

def process_label(label: int, labels: list, event_data: dict, is_first: bool, is_last: bool) -> dict:
    try:
        label_handler_func = LABEL_HANDLERS[label]
        response = label_handler_func(event_data, labels, label)
        if response.get('message'):
            if is_first:
                response['message'] = response['message'][0].upper() + response['message'][1:]
            if not is_last:
                response['message'] += ', '
            else:
                response['message'] += ':'
        return response
    except Exception as e:
        logger.error(f"Failed to process label {label}: {str(e)}")
        return None

def handle_labels(labels: list, event_data: dict) -> dict:
    responses = []
    processed_labels = set()
    
    user_input = event_data.get('message')
    chatbot_answer = ''
    
    # Filter out only the priority labels that are present in the labels list
    existing_priority_labels = [label for label in PRIORITY_LABELS if label in labels]
    
    remaining_labels = [label for label in labels if label not in PRIORITY_LABELS and label not in NOT_PRIORITY_LABELS]
    
    # Filter out only the not priority labels that are present in the labels list
    not_priority_labels = [label for label in NOT_PRIORITY_LABELS if label in labels]
    
    # Combine all labels at the end
    all_labels = existing_priority_labels + remaining_labels + not_priority_labels
    
    for index, label in enumerate(all_labels):
        if label in LABEL_HANDLERS:
            is_last = index == len(all_labels) - 1
            response = process_label(label, all_labels, event_data, index == 0, is_last)
            if response and response.get('message'):
                chatbot_answer += response.get('message')
                if is_last and not chatbot_answer:
                    response['message'] = "Կա՞րող եք հստակեցնել ձեր հարցը։"
                responses.append(response)
    try:
        log_to_dynamodb(user_input, chatbot_answer, labels)
    except Exception as e:
        logger.error(f"Failed to log to DynamoDB: {e}")
    return {
        'success': True,
        'responses': responses
    }

def handle_action(event_type: str, event_data: dict) -> dict:
    try:
        action_handler_func = ACTION_HANDLERS[event_type]
        response_message, success = action_handler_func(event_data)
        return {
            'success': success,
            'responses': [
                {
                    "message": response_message,
                    "buttons": {}
                }
            ]
        }
    except Exception as e:
        logger.error(f"Failed to process action {event_type}: {str(e)}")
        return {
            'success': False,
            'response_message': 'Failed to process action'
        }

def handler(event: dict, context) -> dict:
    event_data: dict = event['event_data']
    labels: list = event.get('labels', [])
    event_type: str = event.get('event_type', 'default')
    logger.info(event)
    if event_type == 'default':
        return handle_labels(labels, event_data)
    else:
        return handle_action(event_type, event_data)
        