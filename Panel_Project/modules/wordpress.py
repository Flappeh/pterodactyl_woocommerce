from dotenv import load_dotenv
import os, requests


# Get order_details
def get_order_id(id):
    con_key=os.getenv('consumer_key')
    con_sec=os.getenv('consumer_secret')
    url_store = f'https://infinity-projects.de/wp-json/wc/v3/orders/{id}?consumer_key={con_key}&consumer_secret={con_sec}'
    response = requests.get(url_store)
    return response.json()


def get_user_details(user_id):
    con_key=os.getenv('consumer_key')
    con_sec=os.getenv('consumer_secret')
    user_url = f'https://infinity-projects.de/wp-json/wc/v3/customers/{user_id}?consumer_key={con_key}&consumer_secret={con_sec}'
    response = requests.get(user_url)
    return response.json()