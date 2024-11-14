#!/bin/bash

##
##      Project: SDDC.Lab
##      Authors: Luis Chanu & Rutger Blom
##     Filename: utils/Util_DelIPv4DNSRecord.sh
##
## This script is used to manually delete a DNS record to the SDDC.Lab DNS Server.
##
## Shell Script Syntax
## ===================
##   ./Util_DelIPv4DNSRecord.sh <FQDN> <IPv4-Address> <Reverse-DNS-Record>
##
##   Example:
##       ./Util_DelIPv4DNSRecord.sh Pod-110-Server.SDDC.Lab. 10.204.110.100 100.110.204.10.in-addr.arpa.
##

DNS_SERVER="10.203.0.5"
FILENAME="nsupdate_$RANDOM"

echo ""
echo "DNS Server used: $DNS_SERVER"
echo " Temp file used: $FILENAME"
echo ""

# Build commands which nsupdate will process, and store in a tmp file
echo "server $DNS_SERVER"       > /tmp/$FILENAME

# Forward 'A' Record
echo "update delete $1 3600 A $2" >> /tmp/$FILENAME
echo "show"                       >> /tmp/$FILENAME
echo "send"                       >> /tmp/$FILENAME

# Reverse 'PTR' Record
echo "update delete $3 3600 PTR $1" >> /tmp/$FILENAME
echo "show"                         >> /tmp/$FILENAME
echo "send"                         >> /tmp/$FILENAME

# All done, so quit
echo "quit"                      >> /tmp/$FILENAME

# Go perform the operations
nsupdate -v /tmp/$FILENAME

# Cleanup
rm /tmp/$FILENAME

##
## Verify record by querying for it
##

echo
echo "#######################################################"
echo "  Perform nslooup to verify DNS FQDN does NOT resolve"
echo "#######################################################"
echo

sleep 1
nslookup $1