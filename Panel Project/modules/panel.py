from dotenv import load_dotenv
import string,random,os,requests,sys
from modules import emails as mail

load_dotenv()

main_url = 'https://panel.infinity-projects.de/api/application'
panel_api = os.getenv('panel_api_key')
post_headers = {
        "Authorization":f"Bearer {panel_api}"
}
get_headers = {
        "Authorization":f"Bearer {panel_api}",
        "Content-Type": "application/json",
        "Accept" : "application/json"
}
#Check if user account exists in the panel
def check_panel_user(details):
    panel_user_url = main_url+'/users'
    response = requests.get((panel_user_url+f"?filter[email]={details['email']}"),headers=get_headers)
    json_data = response.json()
    if(json_data['meta']['pagination']['total']) != 0:
        print('Account Exists')
        return json_data['data'][0]
    else:
        print('User not found, creating a new user account!')
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        payload = {"email": details['email'],"username": details['username'],"first_name": details['first_name'],"last_name": details['last_name'],"password": password}
        response = requests.post(url=panel_user_url,headers=post_headers,data=payload)
        try:
            message = f"""
Your User credentials have been created!
Please go to https://panel.infinity-projects.de to log into your new account

Username : {details['username']}
Password : {password}
"""
            mail.send_email(message, "New User Created",user_email= details['email'])
        except:
            sys.exit("Fail Sending Mail ")
        return response.json()
    

def check_server_nodes():
    node_url=main_url+'/nodes'
    response = requests.get(url=node_url,headers=get_headers)
    data = response.json()['data']
    node_list = []
    for i in data:
        node_list.append(i['attributes']['id'])
    return node_list

#function to read nodes allocation
def check_server_allocation(node, amount):
    url = main_url+f'/nodes/{node}/allocations'
    response = requests.get(url=url,headers=get_headers)
    data = response.json()['data']
    id = []
    for i in data:
        if i['attributes']['assigned'] == False:
            id.append(i['attributes']['id'])
            if len(id)==amount:
                break
    print(id)
    return id


def create_new_server(username,user_id,ram,threads,disk=10000,database=1,ports=1):
    # Get list of node ids
    nodes = check_server_nodes()
    additional_ports = []
    try:
        for i in nodes:
            ids = check_server_allocation(i, ports)
            additional_ports = ids
            if len(additional_ports) == ports:
                break
    except:
        sys.exit("Error Occured on getting allocation")
    print("additional Ports : ",additional_ports)
    create_server_url = main_url+'/servers'
    payload = {
        "name":f"{username}_{additional_ports[0]}",
        "user":f"{user_id}",
        "egg":1,
        "startup":"java -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs/ -Daikars.new.flags=true --add-modules=jdk.incubator.vector -jar {{SERVER_JARFILE}}",
        "docker_image":"ghcr.io/pterodactyl/yolks:java_18",
        "environment":{
            "BUILD_NUMBER":"latest",
            "SERVER_JARFILE":"fabric-server-launch.jar",
            "FABRIC_VERSION":"latest",
            "LOADER_VERSION":"latest"
        },
        "limits":{
            "memory": ram*1024,
            "swap": 0,
            "disk": disk*1024,
            "io": 500,
            "cpu": threads*50
        },
        "feature_limits":{
            "databases":database,
            "backups":1
        },
        "allocation":{
            "default":additional_ports[0]
        }
    }
    if ports >1:
        payload["allocation"]["additional"]= additional_ports
    try:
        response = requests.post(url=create_server_url,headers=post_headers,json=payload)
        return response.json()
    except:
        return (f'Server Build Failed. Reason : {response.reason}')
