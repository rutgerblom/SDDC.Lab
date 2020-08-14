     _________________  _____       _           _     
    /  ___|  _  \  _  \/  __ \     | |         | |    
    \ `--.| | | | | | || /  \/     | |     __ _| |__  
     `--. \ | | | | | || |         | |    / _` | '_ \ 
    /\__/ / |/ /| |/ / | \__/\  _  | |___| (_| | |_) |
    \____/|___/ |___/   \____/ (_) \_____/\__,_|_.__/ 

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
Currently the scripts supports deploying Pods on a standalone ESXi host. This host must be running ESXi version 6.7 or later. After installing ESXi make sure that you configure the following:

* DNS name resolution. The ESXi host should be able to resolve its own hostname via DNS and the Ansible controller must be able to resolve the ESXi hostname via DNS.
* A datastore.
* A portgroup configured with the VLAN ID of the Lab-Routers segment. In the default Pod configuration this portgroup is actually called "Lab-Routers" so giving it that name means you have one thing less to think about later on. 

## Install the Ansible controller

The Ansible controller is the machine from which you will run the Ansible scripts. We recommend installing a modern version of [Ubuntu](https://ubuntu.com/download) on a dedicated virtual machine. Although not required, we also recommended that you place the Ansible controller virtual machine on the same ESXi host as where you will deploy your Pod. This VM can be connected to any VLAN as long as it:

* Can Reach the Lab-Routers segment and the Pod networks behind the [VyOS](https://www.vyos.io/) router.
* Has Internet access.

### Software
After you've installed the Ubuntu OS and applied the latest updates, some additional software is required to turn this machine into an Ansible controller for your SDDC.Lab Pods. You can simply copy and paste the commands below. Installation of the additional software will only take some minutes.

1. Python, pip, and xorriso:  
**sudo apt install python3 python3-pip xorriso**

1. Ansible and the required Python modules:  
**pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython**

1. Python module weasyprint needs to be installed using "sudo":  
**sudo pip3 install weasyprint**

1. And finally you clone the SDDC.Lab repository to an appropriate location on your Ubuntu machine (e.g. $HOME) with:  
**git clone https://github.com/rutgerblom/SDDC.Lab.git**

## Prepare the Pod configuration files
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

Three files in the root of the SDDC.Lab directory require your attention:
* config_sample.yml
* licenses_sample.yml
* software_sample.yml


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