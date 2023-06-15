from flask import Flask, json, request
from flask_restful import Resource, Api, reqparse, abort

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

app_key = os.getenv("APP_KEY")
client_key = os.getenv("CLIENT_KEY")
    
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

null = None
server_details_file = open('resources/server_details.json', 'r')
server_details = json.load(server_details_file)

change_type_args = reqparse.RequestParser()
change_type_args.add_argument("server_id", type=int, help="External server id invalid...", required=True)
change_type_args.add_argument("owner_id", type=int, help="External owner id invalid...", required=True)
change_type_args.add_argument("request_type", type=int, help="Server type request invalid...", required=True)


def download_file(server_full_uuid:str,download_url:str):
    url_download = f'https://panel.infinity-projects.de/api/client/servers/{server_full_uuid}/files/pull'
    body={
        "root": "/",
        "url": f"{download_url}"
    }
    result = requests.post(url=url_download,headers=header_client,json=body)
    return True


#Check if user that requested the type change has the servers
def verify_user(user_id:int,server_id:int):
    url_verify_ownership=f'https://panel.infinity-projects.de/api/application/servers/{server_id}'
    result = requests.get(url=url_verify_ownership,headers=header_app).json()
    if result['attributes']["user"]!=user_id:
        return False
    else:
        return True,{"server_id": server_id,
                     "server_uuid": f"{result['attributes']['uuid']}",
                      "server_identifier": f"{result['attributes']['uuid']}"
                    }
def rename_file(server_identifier:int,old_name:str,new_name:str):
    url_rename = f'https://panel.infinity-projects.de/api/client/{server_identifier}/files/rename'
    body = {
        "root": "/",
        "files": [
            {
                "from": f"{old_name}",
                "to": f"{new_name}"
            }
        ]
    }
    response = requests.put(url=url_rename,headers=header_client,json=body)
    return response.json()
    
def fabric_process(server_details:dict,details):
    fabric_version = details['environment']['FABRIC_VERSION']
    server_id= server_details['server_id']
    server_uuid = server_details['server_uuid']
    server_identifier= server_details['server_identifier']
    url_change_startup=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/startup'
    download_file(server_full_uuid=server_uuid,download_url=f'https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fabric_version}/fabric-installer-{fabric_version}.jar')
    rename_file(server_identifier=server_identifier,old_name=f'{fabric_version}.jar',new_name=f'fabric-installer-{fabric_version}.jar')
    details['startup'] = 'java -jar fabric-installer.jar server -mcversion $MC_VERSION -loader $LOADER_VERSION -downloadMinecraft'
    result_install = requests.patch(url=url_change_startup,headers=header_app,json=details)
    
    return True

def change_type(server_id:int,details):
    url_change_type=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/startup'
    result = requests.patch(url=url_change_type,headers=header_app,json=details)
    response = result.json()
    return response


class MinecraftChangeType(Resource):
    def get(self):
        return "Hello damdam"
    def post(self):
        args = change_type_args.parse_args()
        check_user = verify_user(user_id=args['owner_id'],server_id=args['server_id']) 
        if check_user == False:
            abort(404, message="User is not the owner of server...")
        details=next(a['body'] for a in server_details if a['id']==args['request_type'])
        print(details)
        if details['environment']['PROJECT'] == "fabric":
            print('Fabric detected. Reinstalling')
            fabric_process(server_uuid=check_user[1], details=details)
        process_type = change_type(server_id=args['server_id'],details=next(a['body'] for a in server_details if a['id']==args['request_type']))
        return f"{process_type}"
            
            
    
        
class server:
    app = Flask("PanelAPI")
    api = Api(app)
    def __init__(self):
        pass
    def start(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title',required=True)
        server.api.add_resource(MinecraftChangeType, '/mc-type-change/')
        server.app.run(host='0.0.0.0',port=46752,debug=True)