#!/usr/bin/python3
from pydactyl import PterodactylClient 
from modules import version_downloader as vd
from time import sleep
import requests
import yaml

with open('env.yml','r') as f:
    api_keys = yaml.safe_load(f)

app_key=[]
for i in api_keys['app_key']:
    app_key.append(i)   
client_key = api_keys['client_key']
client_api = PterodactylClient('https://panel.infinity-projects.de', client_key)
server_api = PterodactylClient('https://panel.infinity-projects.de',app_key[0])
header_app= {
    "Authorization": f'Bearer {app_key}',
    "Content-type": 'application/json',
    "Accept": 'application/json',
}
header_client= {
    "Authorization": f'Bearer{client_key}',
    "Content-type": 'application/json',
    "Accept": 'application/json',
}
servers_app = server_api.servers.get_server_info(server_id=146)

print(servers_app)
version = 'latest'
