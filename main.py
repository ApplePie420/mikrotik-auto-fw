import json
from dotenv import dotenv_values
import paramiko as p

# ! Paramiko verbose SSH
# p.common.logging.basicConfig(level=p.common.DEBUG)

# load env variables
env_vars = dotenv_values(".env")

# load JSON config file
configf = open("./config.json")
config = json.load(configf)

# load JSON IP list
iplistf = open("./iplist.json")
iplist = json.load(iplistf)

# wrapper for client.exec_command fnc, handles stdout, error logging and paramiko exceptions
def exec_on_client(client, command, logError=False):
    try:
        stdin, stdout, stderr = client.exec_command(command)
        print("stdout on '{}':".format(command))
        print(stdout.read().decode("ascii"))

        if(logError == True):
            print(stderr.read().decode("ascii").strip("\n"))

    except p.SSHException as e:
        print(e)
        return 1

# @ MikroTik SSH functions
# return a connection object type thing, which is then used as parameter for other SSH oriented stuff
def connect_to_router(ip, username, password):
    client = p.SSHClient()
    client.set_missing_host_key_policy(p.AutoAddPolicy())
    client.connect(ip, 22, username, password, look_for_keys=False)
    return client

# mainly for testing, prints all active connections on the firewall 
def print_active_connections(client):
    exec_on_client(client, "ip firewall connection print")

# creates IP address lists from iplist.json
def import_iplist_to_router(client, iplist):
    for section in iplist:
        for ip in iplist[section]:
            exec_on_client(client, 'ip firewall address-list add list="{}" address="{}" comment="auto-fw: {}"'.format(ip["list_name"], ip["ip"], ip["comment"]))

# creates firewall rules on the router based on the iplist
def add_iplist_to_firewall(client, iplist):
    for section in iplist:
            for ip in iplist[section]:
                exec_on_client(client, 'ip firewall filter add action="{}" chain=input src-address-list="{}" comment="auto-fw: {}"'.format(section, ip["list_name"], ip["comment"]))

client = connect_to_router(env_vars["IP"], env_vars["user"], env_vars["password"])
import_iplist_to_router(client, iplist)
add_iplist_to_firewall(client, iplist)