# Python script for parse IP GeoLocation

# Depends on:
# pygeoip, scapy and a MaxMind database.
# Python 2.7 - as needed by scapy.

# This product includes GeoLite data created by MaxMind available from:
# http://www.maxmind.com
# Database file can be found at http://dev.maxmind.com/geoip/legacy/geolite/
# TODO: print this in google maps =)


import pygeoip

# Supress scapy IPV6 and others warnings.
import logging
import argparse
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff

gip = pygeoip.GeoIP('GeoLiteCity.dat')


def sniffer(interface):
    sniff(iface=interface, prn=printRecord, store=0)


def printRecord(pkt):
    try:
        record = gip.record_by_name(pkt.payload.dst)
        city = record['city']
        region = record['region_code']
        country = record['country_name']
        longitude = record['longitude']
        latitude = record['latitude']

        print("########")
        print('[*] Target: {0} Geo-located.'.format(pkt.payload.dst))
        print('[+] {0} - {1} - {2}'.format(str(city),
                                           str(region),
                                           str(country)))

        print('[+] Latitude: {0} / Longitude {1}'.format(str(latitude),
                                                         str(longitude)))

    except:
        # When parse L2 packets (ARP) raises an exception.
        pass


def main():

    # Defines the options and the help menu.
    parser = argparse.ArgumentParser(
             description="A sniffer wich points the Geo location of an IP.")

    parser.add_argument('interface', metavar='Interface',
                        help="Interface to sniff.")

    # Receives the arguments sent by the user.
    args = parser.parse_args()
    interface = args.interface

    if interface is None:
        print(parser.usage)
        exit(0)

    sniffer(interface)


if __name__ == '__main__':
    main()
