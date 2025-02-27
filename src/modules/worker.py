from pydactyl.api.servers import Servers
from pydactyl.api.user import User
from src.schema import UpdateOrder, PanelUser, Server
from functools import lru_cache
from src.config import PANEL_URL, PANEL_API
import random
import string
from src.modules.email import send_email
import json

product_list = dict()

class PanelWorker(User, Servers):
    def __init__(self,  session=None):
        super().__init__(PANEL_URL, PANEL_API, session)
        
    def start_order_creation(self, order: UpdateOrder):
        user = self.check_user_exists(order.billing.email)
        if not user:
            user = self.start_create_user(order)
        # user = self.start_create_user(order)
        print(user.dict())
        self.start_server_creation(user, order)
        send_email(order.billing.email)
        # self.create_server(name=)
    
    def start_server_creation(self, user: PanelUser, order: UpdateOrder):
        name = user.first_name + ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        for i in order.line_items:
            server = get_server_detail(i.product_id)
            self.create_server(
                name=name,
                allocation_limit=server.allocation,
                backup_limit=server.backup,
                cpu_limit=server.cpu,
                database_limit=server.database,
                user_id=user.id,
                disk_limit=server.disk,
                egg_id=5,
                memory_limit=server.ram,
                oom_disabled=True,
                swap_limit=0,
                start_on_completion=True,
                nest_id=1,
                location_ids=[1]
                
            )
    
    def start_create_user(self, order: UpdateOrder):
        newUser = PanelUser(
            id=0,
            username=(order.billing.first_name + order.billing.last_name).strip().lower(),
            email= order.billing.email,
            first_name=order.billing.first_name,
            last_name=order.billing.last_name,
            password=self.generate_user_password()
        )
        # newUser = PanelUser(
        #     username=order.billing.email,
        #     email= order.billing.email,
        #     first_name=order.billing.first_name,
        #     last_name=order.billing.last_name,
        #     password=self.generate_user_password()
        # )
        
        try:
            result = self.create_user(
                email=newUser.email,
                first_name=newUser.first_name,
                last_name=newUser.last_name,
                password=newUser.password,
                username=newUser.username
            )
            newUser.id = result['attributes']['id']
            return newUser
        except:
            raise Exception("Error creating new user")

    def generate_user_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    def check_user_exists(self, email_input:str):
        print(f"Checking for email : {email_input}")
        user_response = self.list_users(email=email_input)
        users = [i['attributes'] for i in user_response.data]
        for i in users:
            if i["email"] == email_input:
                print(i)
                user = PanelUser(
                    id= i['id'],
                    username=i['username'],
                    email= i['email'],
                    first_name=i['first_name'],
                    last_name=i['last_name'],
                    password=''
                )
                return user
        return None
    
def get_server_detail(id: int) -> Server:
    with open('src/data/products.json','r') as f:
        products = json.load(f)['products']
        for i in products:
            if i['id'] == id:
                return Server(
                    name=i['name'],
                    allocation=i['allocation'],
                    backup=i['backup'],
                    cpu=i['cpu'],
                    database=i['database'],
                    disk=i['disk'],
                    id=i['id'],
                    ram=i['ram']
                )