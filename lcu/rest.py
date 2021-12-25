import requests
from requests.auth import HTTPBasicAuth


class LcuRest:

    def __init__(self, host, port, password):
        self._url = f'https://{host}:{port}'
        self._auth = HTTPBasicAuth('riot', password)

    def _make_url(self, endpoint):
        return f'{self._url}{endpoint}'

    def get(self, endpoint):
        return requests.get(self._make_url(endpoint), auth=self._auth, verify="riotgames.pem")

    def post(self, endpoint):
        return requests.post(self._make_url(endpoint), auth=self._auth, verify="riotgames.pem")

    def put(self, endpoint, json):
        return requests.put(self._make_url(endpoint), auth=self._auth, verify="riotgames.pem", json=json)

    def patch(self, endpoint, json):
        return requests.patch(self._make_url(endpoint), auth=self._auth, verify="riotgames.pem", json=json)

    def lobby_choose_position_put(self, first, second):
        return self.put("/lol-lobby/v2/lobby/members/localMember/position-preferences",
                        {"firstPreference": first, "secondPreference": second})

    def queue_ready_check_accept_post(self):
        return self.post("/lol-matchmaking/v1/ready-check/accept")

    def champion_select_session_get(self):
        return self.get("/lol-champ-select/v1/session")

    def champion_select_action_patch(self, action_id, champion_id):
        return self.patch(f"/lol-champ-select/v1/session/actions/{action_id}", {"championId": champion_id})

    def champion_select_action_complete(self, action_id):
        return self.post(f"/lol-champ-select/v1/session/actions/{action_id}/complete")
