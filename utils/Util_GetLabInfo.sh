#!/bin/bash

##
##      Project: SDDC.Lab
##      Authors: Luis Chanu & Rutger Blom
##     Filename: utils/Util_GetLabInfo.sh
##
## This script is used to get information about the lab environment, including:
##    1) Ansible core version
##    2) Ansible settings
##    3) Ansible modules and versions
##
## Instructions
## ============
##   Run this utility in the root of the SDDC.Lab project directory.
##

/bin/echo -e "\n\n\n"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
/bin/echo -e "%%                      Ansible Version & Locations                       %%"
/bin/echo -e "%%                          (ansible --version)                           %%"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"

ansible --version


/bin/echo -e "\n\n\n"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
/bin/echo -e "%%                       Installed Python Packages                        %%"
/bin/echo -e "%%                              (pip3 list)                               %%"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"

pip3 list


/bin/echo -e "\n\n\n"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
/bin/echo -e "%%                       Ansible Module Information                       %%"
/bin/echo -e "%%                    (ansible-galaxy collection list)                    %%"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

ansible-galaxy collection list


/bin/echo -e "\n\n\n"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
/bin/echo -e "%%                        Ansible Core Information                        %%"
/bin/echo -e "%%                         (ansible-config dump)                          %%"
/bin/echo -e "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"

ansible-config dump
