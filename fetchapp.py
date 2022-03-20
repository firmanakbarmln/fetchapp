import requests
import json
from flask import make_response
from flask import request

class Fetch:
    
    def fetchData():    
        claim = Fetch.claim()
        if claim['status'] == 'success':
            response_API = requests.get('https://60c18de74f7e880017dbfd51.mockapi.io/api/v1/jabar-digital-services/product')
            data = json.loads(response_API.text)
            response_API = requests.get("https://v6.exchangerate-api.com/v6/1130eaad8154c5561ed7a3d4/pair/USD/IDR/")
            fetched = json.loads(response_API.text)
            currency = float(fetched['conversion_rate'])
            for i in range(len(data)):
                price_idr = currency * float(data[i]['price'])
                data[i]['price_in_idr'] = price_idr
            data = json.dumps(data, indent=4)
            return data
        else:
            return claim

    def aggregation():
        claim = Fetch.claim()
        if claim['status'] == 'success':
            data = json.loads(Fetch.fetchData())
            data.sort(key=lambda x: x["price_in_idr"])
            for i in range(len(data)):
                del data[i]['id']
                del data[i]['price']
                del data[i]['createdAt']
            data = json.dumps(data, indent=4)
            return data
        else:
            return claim
        
    def claim():
        s = request.cookies.get('X-SESSION')
        if s is None:
            return {
                "status": "failed",
                "message": "user not login!"
            }
        response_API = requests.post('https://firmanakbarm-api.000webhostapp.com/claim.php', headers={"Cookie": "X-SESSION="+s})
        data = json.loads(response_API.text)
        return data
    
    def login(nik, password):
        body = {'nik':nik, 'password':password}
        response_API = requests.post('https://firmanakbarm-api.000webhostapp.com/login.php', data=body)
        data = json.loads(response_API.text)
        c = make_response(data, 200)
        c.set_cookie(
            "X-SESSION",
            value=data['data']['jwt'],
        )
        return c

