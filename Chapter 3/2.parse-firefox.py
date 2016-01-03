import re
import argparse
import os
import sqlite3


def print_downloads(downloadDB):

    connection = sqlite3.connect(downloadDB)
    cursor = connection.cursor()
    cursor.execute("SELECT name, source, datetime(endTime/1000000, 'unixepoch') FROM moz_downloads;")

    print("[*] --- Files downloaded --- ")

    for row in cursor:

        print("[+] File: {0} - Source: {1} - at: {2}".format(str(row[0]), str(row[1]), str(row[2])))


def print_cookies(cookiesDB):

    try:

        connection = sqlite3.connect(cookiesDB)
        cursor = connection.cursor()
        cursor.execute('SELECT host, name, value FROM moz_cookies')

        print("\n#######################")
        print("--- Listing cookies ---")
        print("########################\n")

        for row in cursor:

            host = str(row[0])
            name = str(row[1])
            value = str(row[2])

            print("Host: {0} - Cookie: {1} - Value: {2}".format(host, name, value))

    except Exception as error:

        if 'encrypted' in str(error):

            print("\n[*] Error reading your database.")
            print("\n[*] Upgrade your Python-Sqlite3 Library.")


def printHistory (placesDB):

    try:

        connection = sqlite3.connect(placesDB)
        cursor = connection.cursor()
        cursor.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits where"
                       " visit_count > 0 and moz_places.id == moz_historyvisits.place_id;")

        # Create a list from previous SQL with only unique items, removing any duplicated entry.
        unique = set(cursor)

        print("\n###############################")
        print(" --- Listing google query's ---")
        print("################################\n")

        for row in unique:

            url = str(row[0])
            date = str(row[1])

            if 'google' in url.lower():

                recursive = re.findall(r'q=.*\&', url)

                if recursive:

                    search = recursive[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')

                    if search:

                        print("[+] Date: {0} - Searched for: {1}".format(date, search))

        print("\n##############################")
        print("--- Listing accessed URLs ---")
        print("###############################\n")

        for row in unique:

            url = str(row[0])
            date = str(row[1])

            print("[+] Date: {0} - URL: {1}".format(date, url))

    except Exception as error:

        if 'encrypted' in str(error):

            print("\n[*] Error reading your database.")
            print("\n[*] Upgrade your Python-Sqlite3 Library.")


def main():

    # Defines the options and the help menu.
    parser = argparse.ArgumentParser(description="A Python SQLite parser for Firefox DB.")
    parser.add_argument('DB_location', help="Firefox profile location.")

    # Receives the argument sent by the user.
    args = parser.parse_args()
    db_location = args.DB_location

    # If target file was not set, prints the help menu from argparse and exits.
    if db_location is None:
        print(parser.usage)
        exit(0)

    # Verifies if the given path is valid.
    elif os.path.isdir(db_location) is False:

        print("[!] Path does not exist: {0}".format(db_location))

    else:

        # Join path for each Sqlite DB in firefox profile location and call the specific function for it.
        db_download = os.path.join(db_location, 'downloads.sqlite')

        if os.path.isfile(db_download):

            print_downloads(db_download)

        else:

            print("[!] Download DB not found in {0}".format(db_download))

        db_cookies = os.path.join(db_location, 'cookies.sqlite')

        if os.path.isfile(db_cookies):

            print_cookies(db_cookies)

        else:

            print("[!] Cookies DB not found in {0}".format(db_cookies))

        db_places = os.path.join(db_location, 'places.sqlite')

        if os.path.isfile(db_places):

            printHistory(db_places)

        else:

            print("[!] Places DB not found in {0}".format(db_places))


if __name__ == '__main__':
    main()