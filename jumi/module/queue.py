def apply_queue_module(jumi):
    handler = jumi.event_handler

    @handler.listener("/lol-matchmaking/v1/ready-check")
    async def auto_accept(data):
        jumi.lcu.rest().queue_ready_check_accept_post()