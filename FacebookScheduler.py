import requests
import facebook

fb_id = ""
fb_secret = ""

def get_fb_token(app_id, app_secret):
    url = 'https://graph.facebook.com/oauth/access_token'       
    payload = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret
    }
    response = requests.post(url, params=payload)
    return response.json()['access_token']

f = get_fb_token(fb_id, fb_secret)


graph = facebook.GraphAPI(str(f))
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")
graph.put_object("me", "feed", message="!")

