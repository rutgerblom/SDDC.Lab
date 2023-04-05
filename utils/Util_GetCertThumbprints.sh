#!/bin/bash

##
##      Project: SDDC.Lab
##      Authors: Luis Chanu & Rutger Blom
##     Filename: utils/Util_GetCertThumbprints.sh
##
## Description
## ===========
##   This script is used to query a given site and return various common fingerprints for the
##   x.509 certificate used by the site.
##
## Command Syntax
## ==============
##   From within the SDDC.Lab/utils directory, the command would be run as follows:
##                ./Util_GetCertThumbprints <URL-to-query>
##
## Example Command
## ===============
##   ./Util_GetCertThumbprints www.google.com
##

echo ""
openssl s_client -connect $1:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -md5    -noout -in /dev/stdin
echo ""
openssl s_client -connect $1:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha1   -noout -in /dev/stdin
echo ""
openssl s_client -connect $1:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha256 -noout -in /dev/stdin
echo ""
openssl s_client -connect $1:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha384 -noout -in /dev/stdin
echo ""
openssl s_client -connect $1:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -sha512 -noout -in /dev/stdin
