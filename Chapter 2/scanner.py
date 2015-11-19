# Network scanner based on chapter 2
# Python 3.4

import optparse
from socket import *

# Function for connect on specific host/port
def connScan(tgtHost, tgtPort):

    try:
        # Opens an IPv4(AF_INET) / TPC(SOCK_STREAM)
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))

        # After a successful connection, send a random string to host/port target and listen to an answer.
        connSkt.send("Random string =)\r\n")
        results = connSkt.recv(100)

        print("[+]%d - tcp open" % tgtPort)
        print("[+] " + str(results))
        connSkt.close()

    except:
        print("[-]%d - tcp closed" % tgtPort)


# Function for port scan. Receive a host and a tuple of TCP ports.
def portScan(tgtHost,tgtPorts):

    try:
        # Returns the ip address (DNS resolver)
        tgtIP = gethostbyname(tgtHost)

    except:
        print("Fail at resolve hostname %s" % tgtHost)
        return

    try:
        # Return the true host name, a list of aliases, and a list of IP addresses, for a host.
        # The host argument is a string giving a host name or IP number.
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan result for: " + tgtName[0])

    except:
        print("\n[+] Scan result for: " + tgtIP)

    # Set timeout for a new socket object
    setdefaulttimeout(1)

    # Loop for port scan
    for tgtPort in tgtPorts:
        print("Scanning port - " + tgtPort)
        connScan(tgtHost,int(tgtPort))


# Good explanation about why use "main" and "if __name__ == __main__"
# http://stackoverflow.com/questions/419163/what-does-if-name-main-do
def main():

    # Define HELP menu
    parser = optparse.OptionParser("Usage scanner.py -t " + "<target host> -p <target port>")

    # Define menu options for target host
    parser.add_option('-t', dest='tgtHost', type='string', help='Specify target host.')

    # Define menu options for target port[s]
    parser.add_option('-p', dest='tgtPort', type='string', help='Specify target port[s] separated by comma.')

    # Receive arguments from user
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost

    # Split the ports using comma as separator
    tgtPorts = str(options.tgtPort).split(', ')

    # If host or port are not set, print HELP and exit.
    if (tgtHost == None) | (tgtPorts[0] == None):
            print(parser.usage)
            exit(0)

    portScan(tgtHost,tgtPorts)

if __name__ == '__main__':
    main()