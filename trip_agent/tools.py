import os
import requests
import random


def get_detail_by_google_map(location: str) -> dict:
    GOOGLEMAP_KEY = os.environ.get('GOOGLEMAP_KEY')
    textsearch_url = 'https://places.googleapis.com/v1/places:searchText'
    payload = {'textQuery': location}
    headers = {
        'X-Goog-Api-Key': GOOGLEMAP_KEY,
        'X-Goog-FieldMask': 'places.id',
    }
    resp = requests.post(textsearch_url, json=payload, headers=headers)
    if not resp.ok:
        return {'latLng': None}
    data = resp.json()
    place = random.choice(data['places'])
    detail_url = f'https://places.googleapis.com/v1/places/{place["id"]}'
    headers = {
        'X-Goog-Api-Key': GOOGLEMAP_KEY,
        'X-Goog-FieldMask': (
            'location,'
            'regularOpeningHours,'
            'displayName,'
            'googleMapsLinks.placeUri'
        ),
    }
    resp = requests.get(detail_url, headers=headers)
    if not resp.ok:
        return {'latLng': None}
    data = resp.json()
    return {
        'latLng': data['location'],
        'placeUri': data['googleMapsLinks']['placeUri'],
    }


if __name__ == '__main__':
    print(get_detail_by_google_map('日月潭水社碼頭商店街'))
