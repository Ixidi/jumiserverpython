import asyncio
import json


def apply_champion_select_module(jumi):
    handler = jumi.event_handler

    actions = []

    @handler.listener("/lol-champ-select/v1/session", "create")
    async def refresh_actions(data):
        nonlocal actions
        actions = []

    i = 1

    @handler.listener("/lol-champ-select/v1/summoners/", "update")
    async def do_action(data):
        if not data["isSelf"] or not data["isActingNow"]:
            return

        session = json.loads(jumi.lcu.rest().champion_select_session_get().content)
        actions_flatten = [item for sublist in session["actions"] for item in sublist]
        matching_actions = [x for x in actions_flatten
                            if x["actorCellId"] == data["cellId"]
                            and not x["completed"]
                            and x["isAllyAction"]
                            and x["isInProgress"]
                            and x["type"] == data["activeActionType"]]
        if len(matching_actions) == 0:
            return

        action = matching_actions[0]
        nonlocal actions

        if action in actions:
            return
        actions.append(action)

        if action["type"] == "ban":
            nonlocal i
            await asyncio.sleep(3)
            jumi.lcu.rest().champion_select_action_patch(action["id"], i)
            i += 1
            jumi.lcu.rest().champion_select_action_complete(action["id"])

        if action["type"] == "pick":
            await asyncio.sleep(1)
            jumi.lcu.rest().champion_select_action_patch(action["id"], 350)
            jumi.lcu.rest().champion_select_action_complete(action["id"])
