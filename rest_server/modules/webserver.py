from flask import Flask, json, request
import httpx
import requests
import asyncio
import json
import sys
companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

# app = Flask(__name__)

server_details=[
        {
            "id":15,
            "body":{
                "startup": "java -Xmx{{SERVER_MEMORY}}M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "SERVER_JARFILE": "paper.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest"
                },
                "egg": 15,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":16,
            "body":{
                "startup": "java  -Xmx{{SERVER_MEMORY}}M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "SERVER_JARFILE": "fabric.jar",
                    "MC_VERSION": "latest",
                    "FABRIC_VERSION":"latest",
                    "LOADER_VERSION":"latest"
                },
                "egg": 16,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":17,
            "body":{
                "startup": "java -Xmx{{SERVER_MEMORY}}M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -Dterminal.jline=false -Dterminal.ansi=true $( [[  ! -f unix_args.txt ]] && printf %s \"-jar {{SERVER_JARFILE}}\" || printf %s \"@unix_args.txt\" )",
                "environment": {
                    "SERVER_JARFILE": "forge.jar",
                    "MC_VERSION": "latest",
                    "BUILD_TYPE":"recommended"
                },
                "egg": 17,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":25,
            "body":{
                "startup": "java  -Dterminal.jline=false -Dterminal.ansi=true  -Xmx{{SERVER_MEMORY}}M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "SERVER_JARFILE": "purpur.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest"
                },
                "egg": 25,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":22,
            "body":{
                "startup": "java -Xmx{{SERVER_MEMORY}}M -XX:MaxRAMPercentage=95.0 -jar {{SERVER_JARFILE}}",
                "environment": {
                    "SERVER_JARFILE": "bungeecord.jar",
                    "BUNGEE_VERSION": "latest"
                },
                "egg": 22,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":21,
            "body":{
                "startup": "java -Xmx{{SERVER_MEMORY}}M -Dterminal.jline=false -Dterminal.ansi=true -jar {{SERVER_JARFILE}}",
                "environment": {
                    "SERVER_JARFILE": "waterfall.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest"
                },
                "egg": 21,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        },
        {
            "id":24,
            "body":{
                "startup": "java -Xmx{{SERVER_MEMORY}}M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
                "environment": {
                    "SERVER_JARFILE": "folia.jar",
                    "MINECRAFT_VERSION": "latest",
                    "BUILD_NUMBER":"latest"
                },
                "egg": 24,
                "image": "ghcr.io/pterodactyl/yolks:java_18",
                "skip_scripts": False
            }
        }
        
    ]

headers= {
            "Authorization": 'Bearer ptla_ebaFM0p5C6kJJruwF2XPbeuTuc9FOUIh2tWSyohA0Qv',
            "Content-type": 'application/json',
            "Accept": 'application/json',
        }

def verify_user(user_id:int,server_id:int,requested_type:int):
    url_verify_ownership=f'https://panel.infinity-projects.de/api/application/servers/{server_id}'
    result = requests.get(url=url_verify_ownership,headers=headers).json()
    print(f'result from verifying {result["attributes"]["user"]}')
    if int(result["attributes"]["user"])!=int(user_id):
        print(f'user {user_id} is not the owner, reporting this incident')
        return 0
    else:
        details=next((item for item in server_details if int(item['id'])==int(requested_type)))['body']
        change_type(server_id,json.dumps(details))

def change_type(server_id:int,details):
    print('details used for changing server: ',details)
    url_change_type=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/startup'
    result = requests.patch(url=url_change_type,headers=headers,data=details).json()
    print(result)
    server_uuid = result["attributes"]["identifier"]
    print(f'server_uuid is : {server_uuid}')
    reinstall_server(server_id=server_id)

def reinstall_server(server_id):
    print('reinstalling server now\n')
    url_reinstall_server=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/reinstall'
    result = requests.post(url=url_reinstall_server,headers=headers)
    print(result)
    start_server(server_id)

def start_server(server_id):
    url_restart_server=f'https://panel.infinity-projects.de/api/application/servers/{server_id}/power'
    header_start=headers
    header_start["Authorization"] = "Bearer ptlc_CyPQOKVtwK8VObE2GLRvDs1u95ju9lg3n4VrMp1PNKc"
    print('processing server startup')
    result = requests.post(url=url_restart_server,headers=header_start)
    print(result.json())
    

async def start_type_change(user_id:int,server_id:int):
    async with httpx.AsyncClient() as session:
        tasks=[]
        tasks.append(asyncio.create_task(verify_user(user_id=user_id,server_id=server_id)))
        result = await asyncio.gather(*tasks)
    return result

# @app.route('/server_details', methods=['GET'])
# async def change_type():
#   test = await verify_user(12,114)
#   if not test:
#     return "no!"
#   return json.dumps(server_details)





if __name__ == '__main__':
    verify_user(sys.argv[1],sys.argv[2],sys.argv[3])
    # app.run(host='0.0.0.0',port=46752,debug=True)