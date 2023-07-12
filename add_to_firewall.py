import json
from global_funcs import connect_to_router, exec_on_client

# load JSON config file
configf = open("./src/config.json")
config = json.load(configf)

# @ MikroTik SSH functions

# main function that takes config file and client as parameters, in a loop that goes over "lists_enabled" gets cidr ranges,
# and creates firewall rules using add_enabled_vidr_to_firewall() function
def lists_to_firewall(config, client):
    for list_item in config["lists_enabled"]:
        iplist = parse_enabled_cidr_ranges(list_item)
        add_cidr_ip_tp_address_list(client, iplist, list_item)
        add_enabled_cidr_to_firewall(client, iplist, list_item)

# gets called from a for loop in a function, that parses the config file's "lists_enabled" section,
# returns contens of a file
def parse_enabled_cidr_ranges(list_name):
    iplistf = open('./lists/cidr/{}'.format(list_name))
    iplist = iplistf.readlines()
    return iplist, list_name

# takes an IP and a client, puts into address list
def add_cidr_ip_tp_address_list(client, address_list, list_name):
    for iplist in address_list[0]:
        exec_on_client(client, 'ip firewall address-list add list={} address="{}" comment="auto-fw: {}"'.format(list_name, iplist.strip("\n"), list_name))

# takes client and list from parse_enabled_cidr_ranges() and creates firewall rule
def add_enabled_cidr_to_firewall(client, address_list, list_name):
    for ip in address_list[0]:
        exec_on_client(client, 'ip firewall filter add action=drop chain=input src-address-list="{}" comment="auto-fw: {}"'.format(ip.strip("\n"), list_name))

# sample usage
client = connect_to_router()
# add pre-compiled lists to the firewall
lists_to_firewall(config, client)