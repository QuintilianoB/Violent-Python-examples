# SSH connection with the pexpect library based on chapter 2
# Python 3.4

# Pexpect is a tool for interacting with other applications, like ssh, sftp, etc.
# It sends shell commands and works according with its output.
# See the docs at: https://pexpect.readthedocs.org/en/stable/
import pexpect


#  I've created this function, as debug, to print the user with which the script is being running.
def running_user():
    user = pexpect.spawn('whoami')
    user.expect(pexpect.EOF)
    print(str(user.before))

# Defines the most common terminals that should be expected from a successful connection.
prompt = ['#','>>>','>','\$']


# Defines how the commands are sent to the target host.
def send_cmd (child, cmd):
    # Sends it.
    child.sendline(cmd)
    # Expects as return one of the items on prompt list.
    child.expect(prompt)
    # Returns the output from child.sendline. Isn't pretty but I won't spend time with it now.
    print(child.before)


# Define the connections for the target host.
def connect(user, host, password):

    # Defines what should be expected as return from a ssh connection to a host if it
    # wasn't located in the user's know_host list.
    ssh_newkey = 'Are you sure you want to continue'
    connStr = 'ssh ' + user + '@' + host

    # The 'spawn' function executes the argument in the local shell. In this case, it starts a ssh connection.
    child = pexpect.spawn(connStr)

    # Sets three possible expected returns from 'spawn' command.
    # A timeout, which indicates that the server is busy or that we are being blocked out by firewall and/or IDS.
    # 'ssh_newkey' indicates that the server is reachable and returns the connection request with its public key for
    # the first time and 'Password' or 'password' when the ssh server is waiting for a password.
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    print(ret)
    print(child.before)

    # Returns 0, 1 or 2, according with the list defined on child.expect.
    # 0 - if returns a TIMEOUT
    # 1 - if it is a ssh_newkey
    # 2 - if it is the string [P|p]assword:
    # and so on....
    if ret == 0:
        print('[-]Error connecting')
        return

    # I couldn't simulate a new key connection. I've removed my know_host file, but even so,
    # every connection falls on case 2, no matter if the connecting to a newly discovered host.
    if ret == 1:
        print("Teste")
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])

        if ret == 0:
            print('[-]Error connecting')
            return

    child.sendline(password)
    child.expect(prompt)
    return child

def main():
    running_user()
    host = 'localhost'
    user = 'quintiliano'
    password = 'itisntmypass'
    child = connect(user, host, password)
    send_cmd(child, 'date')

if __name__ == '__main__':
    main()