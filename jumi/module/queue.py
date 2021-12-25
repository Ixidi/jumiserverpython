def apply_queue_module(jumi):
    handler = jumi.event_handler

    @handler.listener("/lol-matchmaking/v1/ready-check")
    def auto_accept(data):
        jumi.lcu.rest().ready_check_accept_post()