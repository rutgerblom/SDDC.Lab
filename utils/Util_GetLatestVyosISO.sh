#!/bin/bash

##
##      Project: SDDC.Lab
##      Authors: Luis Chanu & Rutger Blom
##     Filename: utils/Util_GetLatestVyosISO.sh
##
## This script is used to manually download the latest rolling VyOS ISO file.  The downloaded file
## placed in the /tmp folder.
##
## Shell Script Example Run
## ========================
##   ./Util_Util_GetLatestVyosISO.sh
##
##

# Define Defaults
DEST_PATH="/tmp"
SOURCE_PATH="https://s3.amazonaws.com/s3-us.vyos.io/rolling/current"
FILENAME="vyos-rolling-latest.iso"


# Notify user
echo ""
echo Once the download completes, the VyOS ISO can be found at $DEST_PATH/$FILENAME
echo ""

# Get VyOS ISO file
wget -P $DEST_PATH $SOURCE_PATH/$FILENAME