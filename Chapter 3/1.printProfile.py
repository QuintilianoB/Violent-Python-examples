# SQLite connection with python based on chapter 3.
# Python 3.4

"""

    The default location of Skype's main.db on linux is:

            /home/$LINUX_USER_NAME/.Skype/$SKYPE_USER_NAME

"""

import sqlite3
import argparse
import os


def printProfile(skypeDB):

    connection = sqlite3.connect(skypeDB)
    cursor = connection.cursor()
    cursor.execute("SELECT fullname, skypename, city, country, datetime(profile_timestamp, 'unixepoch') FROM Accounts;")

    for row in cursor:

        print("[*] --- Found Account ---")
        print("[+]User: {0}".format(str(row[0])))
        print("[+]Skype Username: {0}".format(str(row[1])))
        print("[+]Location: {0} - {1}".format(str(row[2]), str(row[3])))
        print("[+]Profile Date: {0}".format(str(row[4])))

    cursor.close()


def printContacts(skypeDB):

    connection = sqlite3.connect(skypeDB)
    cursor = connection.cursor()
    cursor.execute("SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;")

    for row in cursor:

        print("[*] --- Found Contact ---")
        print("[+]User: {0}".format(str(row[0])))
        print("[+]Skype Username: {0}".format(str(row[1])))

        if str(row[2]) != '' and str(row[2]) is not None:

            print("[+]Location: {0} - {1}".format(str(row[2]), str(row[3])))

        if str(row[4]) is not None:

            print("[+]Mobile Number: {0}".format(str(row[4])))

        if str(row[5]) is not None:

            print("[+]Birthday: {0}".format(str(row[4])))

    cursor.close()


def printCallLog(skypeDB):

    connection = sqlite3.connect(skypeDB)
    cursor = connection.cursor()
    cursor.execute("SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM calls, conversations WHERE calls.conv_dbid = conversations.id;")

    print("[*] --- Found Calls ---")

    for row in cursor:

        print("[+]Time: {0} | Partner: {1}".format(str(row[0]), str(row[1])))


def printMessages(skypeDB):

    connection = sqlite3.connect(skypeDB)
    cursor = connection.cursor()
    cursor.execute("SELECT datetime(timestamp, 'unixepoch'), dialog_partner, author, body_xml FROM Messages;")

    print("[*] --- Found Contact ---")

    for row in cursor:

        try:

            if 'parlist' not in str(row[3]):

                if str(row[1]) != str(row[2]):

                    msgDirection = "To {0}:".format(str(row[1]))

                else:

                    msgDirection = "From {0}:".format(str(row[2]))

                print("Time: {0} - {1} {2}".format(str(row[0]), msgDirection, str(row[3])))

        except:

            pass


def main():

     # Defines the options and the help menu.
    parser = argparse.ArgumentParser(description="A Python SQLite parser for skype DB.")
    parser.add_argument('DBfile', help="Skypes profile location.")

    # Receives the argument sent by the user.
    args = parser.parse_args()
    dbfile = args.DBfile

    # If target file was not set, prints the help menu from argparse and exits.
    if dbfile is None:
        print(parser.usage)
        exit(0)

    # Verifies if the given path is valid.
    elif os.path.isdir(dbfile) is False:

        print("[!] File does not exist: {0}".format(dbfile))

    else:

        # Join path + main.db and call each function defined above.
        dbfile = os.path.join(dbfile, 'main.db')
        printProfile(dbfile)
        printContacts(dbfile)
        printCallLog(dbfile)
        printMessages(dbfile)


if __name__ == '__main__':
    main()
