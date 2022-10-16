#!/bin/bash

##
##      Project: SDDC.Lab
##      Authors: Luis Chanu & Rutger Blom
##     Filename: utils/Util_CreateAllPodConfigs.sh
##
## This script is used to run playbooks/CreatePodConfig.yml against all of the "config*.yml" files, 
## except for config_sample.yml which it skips, in the directory from which this is run.  This script
## is NON recursive, and only processes files in the current directly.
##
## Instructions
## ============
##   Run this utility in the root of the SDDC.Lab project directory
##   All of the configuration files must be located in the root of the SDDC.Lab project directory
##   The configuration files must all be using the following naming scheme: config*.yml
##
## Observations
## ============
##   When running this script, for some reason two (2) processes are visible in "ps -ef" output.
##   Due to limited testing, it's unclear if this will cause a problem.
##

# Loop through config files
for file in config*.yml; do
    # Process all config.* files except config_sample.yml
    if [[ -f "$file" ]] && [[ $file != "config_sample.yml" ]]; then
        echo -e "Processing Config File: \033[33m$file\033[0m"
#        ansible-playbook -e "SourceConfigPath=$(pwd) SourceConfigFile=$file" tests/TestVarsPrompt.yml 1> /dev/null &
        ansible-playbook -e "SourceConfigPath=$(pwd) SourceConfigFile=$file" playbooks/CreatePodConfig.yml 1> /dev/null &
    fi
done
