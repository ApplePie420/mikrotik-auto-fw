import paramiko as p
from dotenv import dotenv_values

# load env variables
env_vars = dotenv_values(".env")

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
def connect_to_router():
    client = p.SSHClient()
    client.set_missing_host_key_policy(p.AutoAddPolicy())
    client.connect(env_vars["IP"], 22, env_vars["user"], env_vars["password"], look_for_keys=False)
    return client