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
server_details=[
        {
            "id":1,
            "body":{
                "startup": "java -Xmx$(({{SERVER_MEMORY}}-1024))M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "PROJECT":"paper",
                    "SERVER_JARFILE": "paper.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":2,
            "body":{
                "startup": "java  -Xmx$(({{SERVER_MEMORY}}-1024))M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "PROJECT":"fabric",
                    "SERVER_JARFILE": "fabric.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":3,
            "body":{
                "startup": "java -Xmx$(({{SERVER_MEMORY}}-1024))M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -Dterminal.jline=false -Dterminal.ansi=true $( [[  ! -f unix_args.txt ]] && printf %s \"-jar {{SERVER_JARFILE}}\" || printf %s \"@unix_args.txt\" )",
                "environment": {
                    "PROJECT":"forge",
                    "SERVER_JARFILE": "forge.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_TYPE":"recommended",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":4,
            "body":{
                "startup": "java  -Dterminal.jline=false -Dterminal.ansi=true  -Xmx$(({{SERVER_MEMORY}}-1024))M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "PROJECT":"purpur",
                    "SERVER_JARFILE": "purpur.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":5,
            "body":{
                "startup": "java -Xmx$(({{SERVER_MEMORY}}-512))M -XX:MaxRAMPercentage=95.0 -jar {{SERVER_JARFILE}}",
                "environment": {
                    "PROJECT":"bungeecord",
                    "SERVER_JARFILE": "bungeecord.jar",
                    "BUNGEE_VERSION": "latest",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":6,
            "body":{
                "startup": "java -Xmx$(({{SERVER_MEMORY}}-512))M -Dterminal.jline=false -Dterminal.ansi=true -jar {{SERVER_JARFILE}}",
                "environment": {
                    "PROJECT":"waterfall",
                    "SERVER_JARFILE": "waterfall.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":7,
            "body":{
                "startup": "java -Xmx$(({{SERVER_MEMORY}}-1024))M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "PROJECT":"folia",
                    "SERVER_JARFILE": "folia.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest",
                    "DL_PATH": null,
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest",
                    "BUILD_TYPE":"recommended",
                    "FORGE_VERSION":null,
                    "BUNGEE_VERSION":"latest"
                },
                "egg": 46,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        }
        
    ]

change_type_args = reqparse.RequestParser()
change_type_args.add_argument("server_id", type=int, help="External ID of server", required=True)
change_type_args.add_argument("owner_id", type=int, help="External ID of server owner", required=True)
change_type_args.add_argument("request_type", type=int, help="Type of minecraft server requested", required=True)


def download_file(server_full_uuid:str,download_url:str):
    url_download = f'https://panel.infinity-projects.de/api/client/servers/{server_full_uuid}/files/pull'
    body={
        "root": "/",
        "url": f"{download_url}"
    }
    result = requests.post(url=url_download,headers=header_client,json=body)



def verify_user(user_id:int,server_id:int,requested_type:int):
    url_verify_ownership=f'https://panel.infinity-projects.de/api/application/servers/{server_id}'
    result = requests.get(url=url_verify_ownership,headers=header_app).json()
    if result["user"]!=user_id:
        return False
    else:
        details=next((item for item in server_details if item['id']==requested_type))
        change_type(server_id,json.dumps(details))
        

def change_type(server_id:int,details:json,app_header:str):
    url_change_type=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/startup'
    result = requests.post(url=url_change_type,headers=app_header,data=details)


class MinecraftChangeType(Resource):
    def get(self):
        return "Hello damdam"
    def post(self,server_id,owner_id,requested_type):
        args = change_type_args.parse_args()
        
        if verify_user==False:
            abort(404, message="User is not the owner of server...")
        else:
            pass
        return f"Server ID : {server_id}, Server Owner: {owner_id}, requested Type: {requested_type}"
    
        
class server:
    app = Flask("PanelAPI")
    api = Api(app)
    def __init__(self):
        pass
    def start(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title',required=True)
        server.api.add_resource(MinecraftChangeType, '/mc-type-change')
        server.app.run(host='0.0.0.0',port=46752,debug=True)