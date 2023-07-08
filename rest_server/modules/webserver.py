from flask import Flask, json, request
from flask_restful import Resource, Api, reqparse, abort
from modules import version_downloader as vd
import requests,json,yaml
from pydactyl import PterodactylClient 


with open('env.yml','r') as f:
    api_keys = yaml.safe_load(f)

app_key=[]
for i in api_keys['app_key']:
    app_key.append(i)   
client_key = api_keys['client_key']

header_app= {
    "Authorization": f'Bearer {app_key[0]}',
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

#start Pydactyl instance
client_api = PterodactylClient('https://panel.infinity-projects.de', client_key)
server_api = PterodactylClient('https://panel.infinity-projects.de',app_key)


#Check if user that requested the type change has the servers
def verify_user(user_id:int,server_id:int):
    result=server_api.servers.get_server_info(server_id=146)
    if result['attributes']["user"]!=user_id:
        return False
    else:
        return True,{"server_id": server_id,
                     "server_uuid": f"{result['attributes']['uuid']}",
                      "server_identifier": f"{result['attributes']['identifier']}"
                    }
def rename_file(server_identifier:str,old_name:str,new_name:str):
    response = client_api.client.servers.files.rename_file(server_id=server_identifier,old_name=old_name,new_name=new_name,root='/')
    return response.json()
    
def start_server(server_identifier:str):
    try:
        client_api.client.servers.send_power_action(server_id=server_identifier,signal='start')
        return True
    except Exception as e:
        return e

def fabric_process(server_details:dict,env_details):
    fabric_version = env_details['environment']['FABRIC_VERSION']
    server_id= server_details['server_id']
    server_uuid = server_details['  ']
    server_identifier= server_details['server_identifier']
    url_change_startup=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/startup'
    download_file(server_full_uuid=server_uuid,download_url=f'https://maven.fabricmc.net/net/fabricmc/fabric-installer/{fabric_version}/fabric-installer-{fabric_version}.jar')
    rename_file(server_identifier=server_identifier,old_name=f'{fabric_version}.jar',new_name=f'fabric-installer-{fabric_version}.jar')
    env_details['startup'] = 'java -jar fabric-installer.jar server -mcversion $MC_VERSION -loader $LOADER_VERSION -downloadMinecraft'
    response = requests.patch(url=url_change_startup,headers=header_app,json=details)
    print(response.json())
    start_server(server_identifier=server_identifier)
    
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
            fabric_process(server_details=check_user[1], details=details)
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