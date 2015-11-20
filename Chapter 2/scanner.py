# Network scanner based on chapter 2
# Python 3.4

import argparse
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
        print("[+]Server response: " + str(results))
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
    setdefaulttimeout(3)

    # Loop for port scan
    for tgtPort in tgtPorts:
        print("Scanning port - " + tgtPort)
        connScan(tgtHost,int(tgtPort))


# Good explanation about why use "main" and "if __name__ == __main__"
# http://stackoverflow.com/questions/419163/what-does-if-name-main-do
def main():

    # Define HELP menu
    parser = argparse.ArgumentParser(description="Simple Python TCP scanner")

    parser.add_argument('Target', help="Target host.")
    parser.add_argument('Ports', help="Target port[s] separated by comma.")

    # Receiving arguments from user
    args = parser.parse_args()
    tgtHost = args.Target

    # Split the ports using comma as separator and validate if ports are INTEGER
    try:
        tgtPorts = map(int, str(args.Ports).split(','))

    except:
        print("Invalid port number")
        exit(0)

    # If host or port are not set, print HELP and exit.
    if (tgtHost == None) | (tgtPorts[0] == None):
            print(parser.usage)
            exit(0)

    portScan(tgtHost,tgtPorts)

if __name__ == '__main__':
    main()