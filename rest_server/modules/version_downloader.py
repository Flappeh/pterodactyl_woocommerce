import json 
import requests
from dotenv import load_dotenv
import os
load_dotenv()

null = None

environment= {
            "PROJECT":"",
            "SERVER_JARFILE": "",
            "MINECRAFT_VERSION": "latest",
            "BUILD_NUMBER":"latest",
            "DL_PATH": null,
            "FABRIC_VERSION":"latest",
            "LOADER_VERSION":"latest",
            "BUILD_TYPE":"recommended",
            "FORGE_VERSION":null,
            "BUNGEE_VERSION":"latest"
        }
app_key = os.getenv("APP_KEY")
client_key = os.getenv("CLIENT_KEY")
header_app= {
    "Authorization": f'Bearer {app_key}',
    "Content-type": 'application/json',
    "Accept": 'application/json',
}
header_client= {
    "Authorization": f'Bearer {client_key}',
    "Content-type": 'application/json',
    "Accept": 'application/json',
}

def download_file(server_full_uuid:str,download_url:str):
    print(f'downloading from {download_url}')
    url_download = f'https://panel.infinity-projects.de/api/client/servers/{server_full_uuid}/files/pull'
    body={
        "root": "/",
        "url": f"{download_url}"
    }
    response = requests.post(url=url_download,headers=header_client,json=body)
    print(response)
    return True

def check_file(server_uuid:str,file_name:str):
    url_check = f'https://panel.infinity-projects.de/api/client/servers/{server_uuid}/files/list?directory=%2F'
    response = requests.get(url=url_check,headers=header_client).json()
    file_check = next((i['attributes']['name'] for i in response['data'] if i['attributes']['name']==file_name),"false")
    print(f'fileChecked = {file_check}')
    return file_check==file_name

def rename_file(server_identifier:str,old_name:str,new_name:str):
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

def purpur_process(server_details:dict,env_details:dict):
    env = env_details['environment']
    download_url=''
    jar_name=''
    if env['DL_PATH'] != null:
        download_url = env['DL_PATH']
    else:
        mc_version = env['MINECRAFT_VERSION']
        avail_versions = requests.get('https://api.purpurmc.org/v2/purpur').json()['versions']
        if mc_version not in avail_versions: mc_version = avail_versions[-1]
        build_number = env['BUILD_NUMBER']
        avail_builds = requests.get(f'https://api.purpurmc.org/v2/purpur/{mc_version}').json()['builds']
        if build_number not in (avail_builds['latest'] or avail_builds['all']): build_number=avail_builds['latest']
        jar_name = f"{env['PROJECT']}-{mc_version}-{build_number}.jar"
        download_url=f"https://api.purpurmc.org/v2/{env['PROJECT']}/{mc_version}/{build_number}/download"
    
    download_file(server_full_uuid=server_details['server_uuid'],download_url=download_url)
        
    pass

def fabric_process():
    pass
