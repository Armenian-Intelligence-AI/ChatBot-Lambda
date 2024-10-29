import utils

def handle_order_item(event_data: dict) -> str:
    if 'order_item_id' in event_data and 'order_branch_id' in event_data:
        return "Պատվերը հաստատված է։", True
    return "Տվյալները բացակայում են", False

def handle_order_get_info(event_data: dict) -> str:
    return "Պատվերը հասնում է 5-7 օրում", True

def handle_cancel_order_item(event_data: dict) -> str:
    if 'cancel_order_item_id':
        return "Պատվերը հաջողությամբ չեղարկվե է։", True
    return "Տվյալները բացակայում են", False

def handle_contac_me(event_data: dict) -> str:
    utils.send_request_to_call_center(1, None)
    return "Մեր մասնագետը շուտով կապ կհաստատի ձեր հետ", True