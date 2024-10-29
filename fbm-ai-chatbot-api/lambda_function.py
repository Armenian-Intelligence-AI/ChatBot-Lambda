import json
from utils import extract_event_details, logger, invoke_stt_endpoint
from event_handlers import handle_default_event, handle_action_events

def lambda_handler(event, context):
    try:
        event = json.loads(event['body'])
        # event = event['body']
        event_type, event_data = extract_event_details(event)
    
        if event_type == 'default':
            if event_data.get('message_type', 'text') == 'audio':
                stt_pred = invoke_stt_endpoint(event_data.get('message'))
                event_data['message'] = stt_pred.get('prediction')
            return handle_default_event(event_data, event_type)
        else:
            return handle_action_events(event_data, event_type)
        
    except Exception as e:
        logger.error(f"Error handling Lambda event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
