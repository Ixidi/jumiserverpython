def apply_lobby_module(jumi):
    handler = jumi.event_handler

    @handler.listener("/lol-lobby/v2/received-invitations")
    async def auto_join(data):
        # TODO
        print(data[0])

    @handler.listener("/lol-lobby/v2/lobby", "create")
    async def auto_position_choose(data):
        queue_id = data["gameConfig"]["queueId"]
        if queue_id not in [400, 420, 440]:
            return
        jumi.lcu.rest().lobby_choose_position_put("UTILITY", "MIDDLE")
