import requests, json
from datetime import datetime
from pygeocoder import Geocoder

def save_json(r):
    data = r.json()
    out_file = open("e.json","w")
    json.dump(data,out_file, indent=4)                                    
    out_file.close()

def get_request(origin1, origin2, date):
    #ENDPOINT = "https://api.wanderu.com/v2/search.json?depart_datetime=2017-04-19&dest_lat=48.856614&dest_lng=2.3522219&jit=true&origin_lat=52.3702157&origin_lng=4.8951679"
    ENDPOINT = "https://api.wanderu.com/v2/trips.json?"
    #ENDPOINT = "https://api.wanderu.com/v2/search.json?"
    params = get_params(origin1, origin2, date)
    headers = {
        'Host': 'api.wanderu.com',
        'X-TOKEN': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiJfSTRqbGJadHlKMG45cE1DaWY5NVR4SS1aU0p6Yk8waiIsImNyZWRlbnRpYWxzIjp7InR5cGUiOiJ1c2VyIiwiYnVpbGRJZCI6IjIuMC4xMCIsImNsaWVudE5hbWUiOiJpcGhvbmU6Y29tLndhbmRlcnUuV2FuZGVydSIsInVzZXJuYW1lIjoiYW5vbnltb3VzIiwiY2xpZW50SWQiOiJqeXdfTEVwQzJjR0VpS0dlbW5jQUtNMUpkTEI2YTlqR2NWeXg4eXNnSkJZIn0sImlhdCI6MTQ5MzA0NzI5NSwiZXhwIjoxNDkzMTMzNjk1fQ.UIKrNhmGgwFrE8fLh5yFTqyKQ8K1po5vtZm_JTQrgN0',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': 'sp=774fa7a7-db96-4637-941d-992e5e721f18; __cfduid=d98c5f200f2cf139280bc50986fa2f5331492613797',
        'Accept-Language': 'en-us',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'Wanderu/140 CFNetwork/758.4.3 Darwin/15.5.0'           
            }
    r = requests.get('%s' % (ENDPOINT, ), params=params, headers = headers)#= {'content-type': 'application/json'})
    print(r.status_code)
    save_json(r)
    return r.json()

def get_params(origin1, origin2, date):
    date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')
    one = Geocoder.geocode(origin1)
    two = Geocoder.geocode(origin2)
    params = {
        'jit': 'true',
        'depart_datetime': date,
        'origin_lat': one[0].latitude,
        'origin_lng': one[0].longitude,
        'dest_lat': two[0].latitude,
        'dest_lng': two[0].longitude                        
            }
    return params

def get_matches(origin1, origin2, date):
    req = get_request(origin1, origin2, date)
    matches = []
    for i in req['result']:
        if 'price' in i:
            d_datetime = datetime.strptime(str(i['depart_datetime']), '%Y-%m-%dT%H:%M:%S.%fZ')
            d_time = d_datetime.replace(hour = d_datetime.hour + i['depart_timezone_offset']).strftime('%H:%M')
            print(d_time)
            a_datetime = datetime.strptime(str(i['arrive_datetime']), '%Y-%m-%dT%H:%M:%S.%fZ')
            a_time = a_datetime.replace(hour = (a_datetime.hour + i['arrive_timezone_offset']) %24).strftime('%H:%M')
            print(a_time)
            print(i['price'])
            print(i['carrier_fields']['links'][0]['href'])
            matches.append({'total': i['price'], 'one': i['depart_name'] + ', ' + i['depart_cityname'], 'two': i['arrive_name'] + ', ' + i['arrive_cityname'], 'to': round(i['duration'], 1), 'arrive_time': a_time, 'depart_time': d_time, 'link': i['carrier_fields']['links'][0]['href']})
    return matches

#tests
# s = get_request()
# save_json(s)
#print(get_matches('Florence','Rome','06/12/2017'))
#save_json(search())

#attempt at extracting x-token...
#ENDPOINT = "https://api.wanderu.com/v2/auth.json"
#r = requests.head('%s' % (ENDPOINT, ), headers = {'content-type': 'application/json'})
#print(r.status_code)
#print(r.headers)

