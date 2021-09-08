import requests

def get_id_by_url(url):
    print(requests.get(url).text)

get_id_by_url(input())