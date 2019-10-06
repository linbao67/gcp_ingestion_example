import requests
import json
import authentication


def link():
    url = "https://rest.apisandbox.zuora.com"
    endpoint = "/v1/transactions/payments/accounts/ff1e23e2211fb802b818d7c630fbc4f6"

    #token = json.loads(authentication.getOAuth())
    #access_token = token["access_token"]
    access_token = "8045e668be2e445286f9ee03ca0498c3"

    headers = {
        'Authorization': "Bearer {}".format(access_token)
    }

    headers2 = {'apiAccessKeyId': 'lin.l.bao@pwc.com',
      'apiSecretAccessKey': 'admin123'
    }

    print(headers['Authorization'], headers)
    payload = {}

    res = requests.get(url+endpoint, headers=headers2)
    print(res.content)
    return res.content


if __name__ == '__main__':
    link()
