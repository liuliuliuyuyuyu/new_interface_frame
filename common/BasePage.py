import datetime

import requests
import readConfig


class BasePage:
    @staticmethod
    def login():
        localReadConfig = readConfig.ReadConfig()
        url = 'http://59.56.182.79:9192/api/login'
        token = localReadConfig.get_headers("User-Agent")
        headers = {
            "User-Agent": str(token)
        }
        data = {
            "username": "hrp3",
            "password": "e10adc3949ba59abbe56e057f20f883e",
            "context": "ygt",
            "businessOfficeId": "3501240101",
            "businessTime": str(datetime.datetime.now())[:10]
        }
        rep = requests.post(url=url, data=data, headers=headers)

        # print(rep.json()['data']['token'])
        return rep.json()['data']['token']

if __name__ == '__main__':
    BasePage().login()


