    # Network scanner based on chapter 2 with nmap module
# Python 3.4
# The nmap module already utilizes multi-threading (way better) than the previous implemented here, so there is no need
# to do it again.

import argparse
import nmap
import json


# Using python-nmap module
# http://xael.org/pages/python-nmap-en.html
def nmapScan(tgtHost,tgtPort):

    # Initializes the nmap module and set target/port.
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)

    # Return the scan status and return it for user.
    # Used Json as solution for an odd behavior of nmap when tryed to print 'args', as described in python-nmap docs.
    # It don't returns nmScan[tgtHost]['tcp'][tgtHost] or anything else after ['tcp'].....
    # This saved me a lot o time https://pymotw.com/2/json/
    temp = json.dumps(nmScan[tgtHost]['tcp'])
    result = json.loads(temp)

    # A different approach for print.
    print("Port tcp/{0} status: {1}".format(tgtPort,result[tgtPort]['state']))

# An explanation about why use "main" and "if __name__ == __main__"
# http://stackoverflow.com/questions/419163/what-does-if-name-main-do
def main():

    # Define HELP menu
    # I've replaced the "optparse" by "argparse"  because the first on is no longer maintained,
    # as stated by Python's Docs.
    parser = argparse.ArgumentParser(description="Simple Python TCP scanner with python-nmap module")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('Ports', help="Target port[s] separated by comma.")

    # Receives arguments from user
    args = parser.parse_args()
    tgtHost = args.Target

    # Splits the ports using comma as separator. The nmap expects 'port' as string, so no str->int conversion here.
    tgtPorts = str(args.Ports).split(',')

    # If host or port are not set, prints out HELP and exit.
    if (tgtHost == None) | (tgtPorts[0] == None):
            print(parser.usage)
            exit(0)

    print("Scan results for {0}".format(tgtHost))
    for tgtPort in tgtPorts:
        nmapScan(tgtHost,tgtPort)

if __name__ == '__main__':
    main()