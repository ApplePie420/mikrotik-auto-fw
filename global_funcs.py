import paramiko as p
from dotenv import dotenv_values

# load env variables
env_vars = dotenv_values(".env")

# ! Paramiko verbose SSH
# p.common.logging.basicConfig(level=p.common.DEBUG)

# wrapper for client.exec_command fnc, handles stdout, error logging and paramiko exceptions
def exec_on_client(client, command, logError=False, verbose=True):
    try:
        # execute the command on the client and get stdin, stdout and stderr
        stdin, stdout, stderr = client.exec_command(command)
        # format the stdout so it's nice and displayable
        stdoutF = stdout.read().decode("ascii")

        # only display errors if explicitly set on (Off by default)
        if(logError == True):
            print(stderr.read().decode("ascii").strip("\n"))
        
        # only print stdout if set on (On by default)
        if(verbose):
            print(stdoutF)

        # return formatted stdout so we can use it
        return stdoutF

    # if something goes fucky, return the exception
    except p.SSHException as e:
        print(e)
        return e
    
# return a connection object type thing, which is then used as parameter for other SSH oriented stuff
def connect_to_router():
    client = p.SSHClient()
    client.set_missing_host_key_policy(p.AutoAddPolicy())
    client.connect(env_vars["IP"], 22, env_vars["user"], env_vars["password"], look_for_keys=False)
    return client