import os
import requests


def get_detail_by_google_map(location: str) -> dict:
    GOOGLEMAP_KEY = os.environ.get('GOOGLEMAP_KEY')
    result = {
        'latLng': None,
        'placeUri': None,
    }
    textsearch_url = 'https://places.googleapis.com/v1/places:searchText'
    payload = {'textQuery': location}
    headers = {
        'X-Goog-Api-Key': GOOGLEMAP_KEY,
        'X-Goog-FieldMask': 'places.id',
    }
    resp = requests.post(textsearch_url, json=payload, headers=headers)
    if not resp.ok:
        return result
    data = resp.json()
    if len(data['places']) < 1:
        return result
    place = data['places'][0]
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
        return result
    data = resp.json()
    result['latLng'] = data['location']
    result['placeUri'] = data['googleMapsLinks']['placeUri']
    return result


def get_candidate_places_by_google_map(location: str, activity_type: str) -> dict:
    # ratings, userRatingCount, reviews
    GOOGLEMAP_KEY = os.environ.get('GOOGLEMAP_KEY')
    result = {
        'locations': [],
    }
    textsearch_url = 'https://places.googleapis.com/v1/places:searchText'
    payload = {
        'textQuery': f'{location} {activity_type}',
    }
    headers = {
        'X-Goog-Api-Key': GOOGLEMAP_KEY,
        'X-Goog-FieldMask': (
            'places.rating,'
            'places.userRatingCount,'
            'places.displayName.text'
        ),
    }
    resp = requests.post(textsearch_url, json=payload, headers=headers)
    if not resp.ok:
        return result
    for loc in resp.json()['places']:
        data = {
            'name': loc['displayName']['text'],
            'rating': loc['rating'],
            'userRatingCount': loc['userRatingCount'],
        }
        result['locations'].append(data)
    return result


if __name__ == '__main__':
    #print(get_detail_by_google_map('日月潭水社碼頭商店街'))
    print(get_candidate_places_by_google_map('日月潭', 'accommodation'))
