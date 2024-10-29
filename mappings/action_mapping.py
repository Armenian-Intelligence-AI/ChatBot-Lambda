import action_handlers

ACTION_HANDLERS = {
    'order_item': action_handlers.handle_order_item,
    'cancel_order_item': action_handlers.handle_cancel_order_item,
    'order_get_info': action_handlers.handle_order_get_info,
    'contact_me': action_handlers.handle_contac_me,
}
