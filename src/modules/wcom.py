from woocommerce import API
from config import WEB_URL, API_KEY, API_SECRET

class WooConn(API):
    def __init__(self, **kwargs):
        super().__init__(
            url=WEB_URL, 
            consumer_key=API_KEY, 
            consumer_secret=API_SECRET, 
            wp_api=True,
            version="wc/v3",
            **kwargs)
        
    def list_products(self):
        data = self.get("products").json()
        print(data)
        return data
    
    def list_orders(self):
        data = self.get("orders").json()
        for i in data:
            items = [x["name"] for x in i["line_items"]]
            print(f"""
ID : {i["id"]}
Status : {i["status"]}
Items : {
    items
    }
""")
        return data