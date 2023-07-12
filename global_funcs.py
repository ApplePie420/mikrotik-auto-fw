import paramiko as p

# ! Paramiko verbose SSH
# p.common.logging.basicConfig(level=p.common.DEBUG)

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
    
# return a connection object type thing, which is then used as parameter for other SSH oriented stuff
def connect_to_router(ip, username, password):
    client = p.SSHClient()
    client.set_missing_host_key_policy(p.AutoAddPolicy())
    client.connect(ip, 22, username, password, look_for_keys=False)
    return client