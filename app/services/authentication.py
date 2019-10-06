import requests
from flask import Flask , jsonify

app = Flask(__name__)


@app.route('/service/authentication')
def test():
    """Return a friendly HTTP greeting."""
    return 'Authentication'


@app.route('/service/oauth', methods=['GET','POST'])
def get_oath():
    url = "https://rest.apisandbox.zuora.com/oauth/token"
    payload = "client_id=3de56ab4-7032-4363-a1d6-ed2873ea03cd&client_secret=kLToS%3DaJVz42gm3cxCyZm7t5XkPHt5JEn1wy%2FFM&grant_type=client_credentials"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return jsonify(response.content)



if __name__ == '__main__':
    app.run(debug=True)