# A FPT anonymous login script, based on chapter 2.
# Python 3.4

"""

    I've changed from the book's example just to try adapt it with previous examples.
    No big deal here. Just a tool for ftp login without password. The main point here is how to send only one arg for
    the thread target. It MUST be passed as tuple and not as a single argument. Took me 1 hour to realize it.

"""

import ftplib
import argparse
import threading

max_connections = 5
connection_lock = threading.BoundedSemaphore(value=max_connections)
Success = 0
Hosts = 0


def anon_login(hostname):

    global Success

    try:

        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'anon@ymous.com')
        print("[+] FTP anonymous login successful on - {0}".format(hostname))
        ftp.quit()
        Success += 1

    except Exception as error:

        print("[+] FTP anonymous login failed on - {0}".format(hostname))
        return False

    finally:

        connection_lock.release()


def main():

    global Hosts

    # Defines the options and the help menu.
    parser = argparse.ArgumentParser(description="Python FTP anonymous login")
    parser.add_argument('TargetFile', help="File with target hosts, one per line.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    targetFile = args.TargetFile

    # If target file is not set, prints the help menu from argparse and exits.
    if targetFile is None:
        print(parser.usage)
        exit(0)

    with open(targetFile, 'r') as hosts:

        for host in hosts.readlines():

            connection_lock.acquire()

            Hosts += 1
            host = host.strip('\r').strip('\n')
            print("[-] Testing login on host: {0}".format(host))

            # Defines and starts the thread. Notice the coma in args=(host,).
            threading.Thread(target=anon_login, args=(host,)).start()

if __name__ == '__main__':
    main()