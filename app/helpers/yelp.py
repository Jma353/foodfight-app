from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io, requests
# from xml.etree import ElementTree4
# import untangle
# from HTMLParser import HTMLParser
from lxml import html

auth = Oauth1Authenticator(
    consumer_key='vZacw-VFx-lpohJ4NP18dg',
    consumer_secret='Msw2c1ucS75FXpVlmpM37pgYYKw',
    token='QA002Ksj-663GPrYuthbERc5hdPKmgf5',
    token_secret='EMKb2zc3RCCJeCwcBc0evBl-Vik'
)

client = Client(auth)

# with io.open('config_secret.json') as cred:
#     creds = json.load(cred)
#     auth = Oauth1Authenticator(**creds)
#     client = Client(auth)

def yelpApiCoordinates(lat, long, params):
    return client.search_by_coordinates(lat, long, **params)

def yelpApiBoundingBox(lat, long, params):
    return client.search_by_bounding_box(lat1,long1,lat2,long2,**params)

def yelpApiSearch(location, params):
    return client.search(location, **params)

def yelpBusinsess(id):
    return client.get_business(id);

def getYelpInfo(lat, long, term):
    params = {
        "limit": 20,
        "term": term

    }
    response = yelpApiCoordinates(lat, long, params)
    # print(len(response.businesses))
    # print(response.businesses[0])

    responses = []
    for i in range(0, len(response.businesses)):
        review = yelpBusinsess(response.businesses[i].id)

        responses.append({
            "id": response.businesses[i].id,
            "name": response.businesses[i].name,
            "rating": response.businesses[i].rating,
            "cats": response.businesses[i].categories,
            "lat": response.businesses[i].location.coordinate.latitude,
            "long": response.businesses[i].location.coordinate.longitude,
            "review": review.business.reviews[0].excerpt
        });
    return responses

# parser = HTMLParser()
# def yelpScraper():
#     result = requests.get("https://www.yelp.com/search?find_loc=New+York,+NY&start=10")

#     tree = html.fromstring(result.content)

#     print(tree)
#     # print(result.content)
#     # obj = untangle.parse("https://www.yelp.com/search?find_loc=New+York,+NY&start=10")
#     # print(obj)

# yelpScraper()

print(getYelpInfo(40.712784, -74.005941, "sushi"))