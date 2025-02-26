from pydactyl.api.servers import Servers
from pydactyl.api.user import User
from src.schema import UpdateOrder
from functools import lru_cache
from src.config import PANEL_URL, PANEL_API


class PanelWorker(User, Servers):
    def __init__(self,  session=None):
        super().__init__(PANEL_URL, PANEL_API, session)
        
    def start_order_creation(self, order: UpdateOrder):
        if not self.check_user_exists(order.billing.email):
            self.create_user()
    
    def create_user(self, username, email, first_name, last_name, external_id=None, password=None, root_admin=False, language='en'):
        return super().create_user(username, email, first_name, last_name, external_id, password, root_admin, language)
    
    def check_user_exists(self, email_input:str):
        print(f"Checking for email : {email_input}")
        user_response = self.list_users(email=email_input)
        users = [i['attributes'] for i in user_response.data]
        for i in users:
            if i["email"] == email_input:
                print("Exists")
                return True
        return False