import requests
from bs4 import BeautifulSoup
import json


# API request to extract HTML (overkill, just trying to use Postman)
def get_html():
    name = 'credor'
    page = '1'
    url = 'https://buyee.jp/item/search/query/' + name + '/category/23140?sort=score&ranking=popular&translationType=98&page=' + page
    #  https://buyee.jp/item/search/query/credor/category/23140?sort=score&ranking=popular&translationType=98&page=1

    payload = {}
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': 'mrc_v2=mrc1%3Dmail%26mrc2%3Dauction_watchlist%26mrc3%3Dmail-reminder; mrc_v1=mrc1%3Dmail%26mrc2%3Dauction_watchlist%26mrc3%3Dmail-reminder; otherbuyee=0ijm113u46c3iorj0gao6nmn82; FREECOINS_6670_retry2=1; version=841be4ac561b9e1bfd3739d917d0a63fc5e021f2; live-agent=false; convoId=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJZV1J0YVc1amVXSmxjZz09IiwiY3JlYXRlZEF0IjoxNzE2NzEyMzk2MjAzLCJib3RJZCI6ImJ1eWVlX2VuX2RldiIsInVzZXJJZCI6IllXUnRhVzVqZVdKbGNnPT0iLCJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNzE2NzEyMzk2fQ.BgWHmSQpjb6gVQwMchm6Z-HLrd4koyO5IykjsTlhHOI; googtrans=/ja/en; googtrans=/ja/en; version=841be4ac561b9e1bfd3739d917d0a63fc5e021f2',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print('Getting html from:' + url)
    return response


# Scrape Auction IDs from HTML
def get_auction_ids(html):
    # Example HTML string
    html_string = html.text

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(html_string, 'html.parser')

    # Find all div elements with the specified class
    divs = soup.find_all('div', class_='watchItem__items')

    # Extract and print the value of the data-auctionid attribute for each div
    auction_ids = []
    for div in divs:
        auction_id = div.get('data-auctionid')
        if auction_id:
            auction_ids.append(auction_id)
            # print(f"Auction ID: {auction_id}")
    print(auction_ids)
    
    return auction_ids


# TODO: URL incorrect
def get_price(auction_id):
    url = "https://buyee.jp/api/v1/auction/total_amount?price=11&quantity=1&planId=1&buyeeFeeCouponId=&internationalDeliveryFeeCouponId=&itemPriceCouponId=&auctionId=" + auction_id + "&memberDeliveryAddressLogId=&paymentMethodType=2"

    payload = {}
    headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en;q=0.7',
    'cookie': 'mrc_v2=mrc1%3Dmail%26mrc2%3Dauction_watchlist%26mrc3%3Dmail-reminder; mrc_v1=mrc1%3Dmail%26mrc2%3Dauction_watchlist%26mrc3%3Dmail-reminder; otherbuyee=0ijm113u46c3iorj0gao6nmn82; version=841be4ac561b9e1bfd3739d917d0a63fc5e021f2; convoId=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJZV1J0YVc1amVXSmxjZz09IiwiY3JlYXRlZEF0IjoxNzE2NjU3NTYyMDY0LCJib3RJZCI6ImJ1eWVlX2VuX2RldiIsInVzZXJJZCI6IllXUnRhVzVqZVdKbGNnPT0iLCJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNzE2NjU3NTYyfQ.2mJIQMur258h8xH0vyl8k1bv1JZoGKi4YmF2Dh3KqaI; live-agent=false',
    'priority': 'u=1, i',
    'referer': 'https://buyee.jp/bid/s1134252387?conversionType=buyee_top_browsing_history',
    'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)   # parse JSON string
    data = response_dict['data']

    item_price = data['item_price'] # lowest possible bid in Yen
    total_price = data['total_amount'] # in Yen
    fx_total_price = data['fx_total_amount'] # in foreign currency (i.e. SGD)
    price = [item_price, total_price, fx_total_price]

    print('Getting price from: ' + url + '. Price: ' + str(price))


for auction_id in get_auction_ids(get_html()):
    get_price(auction_id)