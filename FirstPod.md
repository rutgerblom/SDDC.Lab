# Deploying your first SDDC.Lab Pod

## Table of Contents
* [Configure the physical network](#Configure-your-physical-network)
* [Configure the physical ESXi host](#Configure-the-physical-ESXi-host)
* [Install the Ansible Controller](#Install-the-Ansible-Controller)
* [Prepare the configuration files](#Prepare-the-configuration-files)
  * [config.yml](#licenses.yml)
  * [licenses.yml](#licenses.yml)
  * [software.yml](#licenses.yml)
* [Create the software library](#Create-the-software-library)
* [Create the Pod configuration](#Create-the-Pod-configuration)
* [Start the Pod deployment](#Start-the-Pod-deployment)
* [Access the Pod's components](#Access-the-Pod's-components)

## Configure the physical network

## Configure the physical ESXi host
Currently the scripts supports deploying Pods on a standalone ESXi host. This host must be running ESXi version 6.7 or higher.

## Install the Ansible controller

The Ansible controller is the machine from which you run the Ansible scripts. We recommend installing a modern version of [Ubuntu](#https://ubuntu.com/download) on a dedicated virtual machine for this purpose. Although not required, we recommended that you deploy the Ansible controller virtual machine on the same ESXi host as where you will deploy your Pod. Consider connecting this VM to the Lab-Routers port group. Internet access from this VM is recommended.

### Software
After installing the Ubuntu OS and the latest updates, some additional software is required. You can simply copy and paste the commands below. Installation of the additional software will only take some minutes.

1. Python, pip, and xorriso are installed with:  
**sudo apt install python3 python3-pip xorriso**

1. Install Ansible and the required Python modules using pip:  
**pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython**

1. Another Python module weasyprint needs to be installed using "sudo":  
**sudo pip3 install weasyprint**

1. And finally, clone this repository to an appropriate location on your Ubuntu machine (e.g. $HOME) with:  
**git clone https://github.com/rutgerblom/SDDC.Lab.git**

## Prepare the configuration files
After cloning the repository you will end up with a directory called "SDDC.Lab" with the following contents:

    hosts
    images
    library
    module_utils
    playbooks
    plugins
    templates
    tests
    utils
    ansible.cfg
    CHANGELOG.md
    FirstPod.md
    README.md
    config_sample.yml
    deploy.yml
    licenses_sample.yml
    software_sample.yml
    undeploy.yml

The **_sample.yml** configurations files in the root of the SDDC.Lab directory need to be copied and modified by you before you can start deploying your first Pod.

### config.yml (TBD)
In config.yml you define the configuration and settings of your Pod.   
cp config_sample.yml config.yml

### licenses.yml (TBD)
In licenses.yml you store your license keys for the different products. 
cp licenses_sample.yml config.yml

### software.yml (TBD)
In software.yml we've defined the poducts and versions that can be deployed with the scripts.
cp software_sample.yml config.yml

## Create the software library

## Create the Pod configuration

## Start the Pod deployment

## Access the Pod's components