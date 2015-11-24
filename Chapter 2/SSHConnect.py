# SSH connection with pexpect library based on chapter 2
# Python 3.4

# Pexpect is a tool for interacting with other applications, like ssh, sftp, etc.
# It sends shell commands and works according with the output.
# See the docs at: https://pexpect.readthedocs.org/en/stable/
import pexpect


# I've created this function, as debug, to print with which user the script is being running.
def running_user():
    user = pexpect.spawn('whoami')
    user.expect(pexpect.EOF)
    print(str(user.before))

# Define the most commons terminals that should be expect from a successful connection.
prompt = ['#','>>>','>','\$']


# Define how the commands are send to the target host.
def send_cmd (child, cmd):
    # Send commands.
    child.sendline(cmd)
    # Expect on of those items on prompt list.
    child.expect(prompt)
    # Returns the output from child.sendline. Isn't pretty but I'll not spend time changing it now.
    print(child.before)


# Define the connections for the target host.
def connect(user, host, password):

    # Define what should expect from a ssh connection to a new host, before the host be add to user's know_host list.
    ssh_newkey = 'Are you sure you want to continue'
    connStr = 'ssh ' + user + '@' + host

    # The 'spawn' function execute the argument in the local shell. In this case, it starts a ssh connection.
    child = pexpect.spawn(connStr)

    # Set three possible expected returns from spawn command. A timeout, which indicates that the server is busy or we
    # are blocked out. ssh_newkey indicates that the server is reachable and returns the connection request with its
    # public key and finally Password or password as the ssh server wait's for password input.
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    print(ret)
    print(child.before)

    # It returns 0, 1 or 2, according with the list defined on child.expect.
    # 0 - if returns a TIMEOUT
    # 1 - if it is a ssh_newkey
    # 2 - if it is the string [P|p]assword:
    # and so on....
    if ret == 0:
        print('[-]Error connecting')
        return

    # I couldn't simulate a new key connection. I've removed my local host form my own user know_host list but
    # nevertheless every connection falls on case number 2.
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