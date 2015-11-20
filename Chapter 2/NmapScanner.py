# Network scanner based on chapter 2 with nmap module
# Python 3.4
# Nmap module already utilize multi-threading (way better) than previous implemented here so there is no
# need to use it.

import argparse
import nmap
import json


# Using python-nmap module
# http://xael.org/pages/python-nmap-en.html
def nmapScan(tgtHost,tgtPort):

    # Initialize the nmap module and set target/port.
    nmScan = nmap.PortScanner()
    print(tgtHost,tgtPort)
    nmScan.scan(tgtHost, tgtPort)

    # Return the scan status and print it for user.
    # Used Json as solution for an odd behavior of nmap when tried to print args as described in python-nmap docs.
    # It can't parse nmScan[tgtHost]['tcp'][tgtHost] or anything else after tcp.....

    temp = nmScan[tgtHost]['tcp']
    print(temp)

# An explanation about why use "main" and "if __name__ == __main__"
# http://stackoverflow.com/questions/419163/what-does-if-name-main-do
def main():

    # Define HELP menu
    # Replaced the "optparse" for "argparse" since the first on is no longer maintained, as stated by Python's Docs.
    parser = argparse.ArgumentParser(description="Simple Python TCP scanner with python-nmap module")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('Ports', help="Target port[s] separated by comma.")

    # Receive arguments from user
    args = parser.parse_args()
    tgtHost = args.Target

    # Split the ports using comma as separator. Nmap expects the ports as string so no str->int conversion here.
    tgtPorts = str(args.Ports).split(',')

    # If host or port are not set, print HELP and exit.
    if (tgtHost == None) | (tgtPorts[0] == None):
            print(parser.usage)
            exit(0)

    for tgtPort in tgtPorts:
        nmapScan(tgtHost,tgtPort)

if __name__ == '__main__':
    main()