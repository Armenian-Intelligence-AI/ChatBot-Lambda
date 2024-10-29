from config import *
import uuid
from datetime import datetime
import pyodbc
import json

def execute_query_on_db(query: str):
    try:
        # Connection details
        server = DATABASE_HOST
        database = DATABASE_NAME
        username = DATABASE_USERNAME
        password = DATABASE_PASSWORD
        port = 5118
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server},{port};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            'TrustServerCertificate=yes;'
        )   
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    columns = [column[0] for column in cursor.description]
                    rows = cursor.fetchall()
                    
                    results = []
                    for row in rows:
                        row_dict = dict(zip(columns, row))
                        results.append(row_dict)
                    
                    return results
        except pyodbc.InterfaceError as ie:
            print("Interface Error:", ie)
        except pyodbc.DatabaseError as de:
            print("Database Error:", de)
        except Exception as ex:
            print("General Error:", ex)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

def send_request_to_call_center(customer_phone: str, label):
    ...

def call_bank_internal_api(request_data: dict, request_method: str):
    ...

def json_serializable(obj):
    """Helper function to convert non-serializable objects to JSON serializable formats."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
    
def format_return_label_data(message: str, buttons: dict = {}) -> dict:
    serialized_data = json.dumps({
        'message': message,
        'buttons': buttons
    }, default=json_serializable)
    return json.loads(serialized_data)
    
    
def log_to_dynamodb(user_input, chatbot_answer, labels):
    pk = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    log_item = {
        'pk': pk,
        'user_input': user_input,
        'chatbot_answer': chatbot_answer,
        'created_at': created_at,
        'labels': labels,
        'is_personal_info': 0 in labels
    }
    
    try:
        dynamodb_client.put_item(
            TableName='fbm-chatbot-message-logs',
            Item={
                'request_id': {'S': log_item['pk']},
                'user_input': {'S': log_item['user_input']},
                'chatbot_answer': {'S': log_item['chatbot_answer']},
                'is_personal_info': {'BOOL': log_item['is_personal_info']},
                'detected_labels': {'L': [{'N': str(label)} for label in log_item['labels']]},
                'created_at': {'S': log_item['created_at']},
            }
        )
        logger.info(f"Log entry created with pk: {pk}")
    except Exception as e:
        logger.error(f"Failed to log to DynamoDB: {e}")
        