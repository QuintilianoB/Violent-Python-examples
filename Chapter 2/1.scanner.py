# Network scanner based on chapter 2
# Python 3.4

import argparse
import socket
import threading

# Define a value for the semaphore state used(ish) bellow.
# An explanation on how Python's Multi-thread works:
# http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/
screenLock = threading.Semaphore(value=1)


# Function for connect on specific host/port
def connScan(tgtHost, tgtPort):

    try:
        # Opens an IPv4(AF_INET) / TPC(SOCK_STREAM)
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))

        # After a successful connection, sends a random string to targets host/port and waits for an answer.
        connSkt.send("Random string =)\r\n")
        results = connSkt.recv(100)

        # Here is where the threading starts to work.
        # It blocks access to a specific resource, in this case the terminal screen,
        # to other threads who must wait for a release before continue.
        screenLock.acquire()

        print("[+]%d - tcp open" % tgtPort)
        print("[+]Server response: " + str(results))

    except:
        # Again, before write to terminal, the process need to acquire the resource.
        screenLock.acquire()
        print("[-]%d - tcp closed" % tgtPort)

    finally:
        # Then finish by releasing the lock on screen and by closing the connection with target host.
        screenLock.release()
        connSkt.close()


# Function for port scan. Receives a host and a tuple of TCP ports.
def portScan(tgtHost,tgtPorts):

    try:
        # Returns the ip address (DNS resolve)
        tgtIP = socket.gethostbyname(tgtHost)

    except:
        print("Fail at resolve hostname %s" % tgtHost)
        return

    try:
        # Return the true host name, a list of aliases, and a list of IP addresses about the targeted host.
        # The host's argument must be a string name or IP number.
        tgtName = socket.gethostbyaddr(tgtIP)
        print("\n[+] Scan result for: " + tgtName[0])

    except:
        print("\n[+] Scan result for: " + tgtIP)

    # Sets the timeout for a new socket object
    socket.setdefaulttimeout(3)

    # Loop for port scan
    for tgtPort in tgtPorts:
        print("Scanning port - %d" % tgtPort)
        connScan(tgtHost,int(tgtPort))


# An explanation about why use "main" and "if __name__ == __main__"
# http://stackoverflow.com/questions/419163/what-does-if-name-main-do
def main():

    # Defines the options and the help menu.
    # I've replaced the "optparse" by "argparse"  because the first on is no longer maintained,
    # as stated by Python's Docs.
    parser = argparse.ArgumentParser(description="Simple Python TCP scanner")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('Ports', help="Target port[s] separated by comma.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    tgtHost = args.Target

    # Splits the ports using comma as separator. The nmap expects 'port' as string, so no str->int conversion here.
    try:
        tgtPorts = map(int, str(args.Ports).split(','))

    except:
        print("Invalid port number")
        exit(0)

    # If anything is not set , prints the help menu from argparse and exits.
    if (tgtHost == None) | (tgtPorts[0] == None):
            print(parser.usage)
            exit(0)

    portScan(tgtHost,tgtPorts)

if __name__ == '__main__':
    main()