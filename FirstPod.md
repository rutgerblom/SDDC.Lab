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

## Install the Ansible controller

The Ansible controller is the machine from which you run the Ansible scripts. We recommend installing a modern version of [Ubuntu](#https://ubuntu.com/download) on a dedicated virtual machine for this purpose. Although not required, we recommended that you deploy the Ansible controller virtual machine on the same ESXi host as where you will deploy your Pod. Consider connecting this VM to the Lab-Routers port group. Internet access from this VM is recommended.

### Hardware
The recommended hardware configuration for the Ansible controller virtual machine:
* 2 CPUs
* 16 GB RAM
* 150 GB hard disk
* VMware Paravirtual SCSI controller
* VMXNET 3 network adapter

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

### config.yml

### licenses.yml

### software.yml

## Create the Pod configuration

## Start the Pod deployment

## Access the Pod's components