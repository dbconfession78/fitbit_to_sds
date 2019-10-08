import requests


class FitBit:
    def __init__(self, config):
        self.config = config
        self.token = None
        self.get_token()

    def __get_token(self):
        return self.token

    def __headers(self):
        return {"Authorization": "Bearer %s" % self.__get_token(),
                "Content-type": "application/json",
                # "Content-type": "multipart/form-data; boundary=--------------------------102266415698341472523543",
                "Accept": "*/*"}

    def get_sleep_data(self, date_time):
        req_uri = "https://api.fitbit.com/1/user/223VS85/sleep/date/%s.json" % date_time
        response = requests.get(
            req_uri,
            headers=self.__headers())

        content = response.content
        json = response.json()
        return json

    def get_token(self):
        # TODO: make this programmatic
        self.token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkI2MjIiLCJzdWIiOiIyM1ZTODUiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTcxMDk2NzMwLCJpYXQiOjE1NzA0OTE5ODl9.di8nP0Ib1RkBxANVwLivzM1CPD9uu2FRomim7B4c49g"
