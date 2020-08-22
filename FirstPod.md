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
* [Prepare the Pod configuration files](#Prepare-the-Pod-configuration-files)
  * [config.yml](#config\.yml)
  * [licenses.yml](#licenses\.yml)
  * [software.yml](#software\.yml)
* [Create the software library](#Create-the-software-library)
* [Create the Pod configuration](#Create-the-Pod-configuration)
* [Start the Pod deployment](#Start-the-Pod-deployment)
* [Access the Pod's components](#Access-the-Pod's-components)

## Configure the physical network

## Configure the physical ESXi host
Currently the scripts supports deploying Pods on a standalone ESXi host. This host must be running ESXi version 6.7 or later. After installing ESXi make sure that you configure the following:

* A datastore.
* A portgroup configured with the VLAN ID of the Router Uplink segment. In the default Pod configuration this portgroup is called "Lab-Routers" so giving it that name will save you some time. 

## Install the Ansible controller

The Ansible controller is the machine from which you will run the Ansible scripts. We recommend installing a modern version of [Ubuntu](https://ubuntu.com/download) on a dedicated virtual machine. This VM can be connected to any VLAN as long as it:

* Can access the physical ESXi host
* Can reach the Router Uplink segment and the Pod networks behind the [VyOS](https://www.vyos.io/) router.
* Has Internet access.

### Software
After you've installed the Ubuntu OS and applied the latest updates, some additional software is required to turn this machine into an Ansible controller for your SDDC.Lab Pods. You can simply copy and paste the commands below. Installation of the additional software will only take some minutes.

1. Python, pip, and xorriso:  
**sudo apt install python3 python3-pip xorriso**

1. Ansible and the required Python modules:  
**sudo pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython==1.16.0**

1. And finally you need to clone the SDDC.Lab repository to an appropriate location on your Ubuntu machine (e.g. $HOME) with:  
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

Start by creating your own copies of the sample configuration files:
* cp config_sample.yml config.yml
* cp licenses_sample.yml licenses.yml
* cp software_sample.yml software.yml

### config.yml
This file contains all of the configuration and settings for the Pod you're about to deploy. There are many settings that you *can* change, but only a few that you *must* change. The table below contains the settings that you *must* change:
<br>
| Setting                                  | Description                                                                       | Example
| :---                                     | :---                                                                              | :---
| Common.Password.Physical                 | The root password of your physical ESXi host                                      | VMware1!
| TargetConfig.Host.FQDN                   | The FQDN of your physical ESXi host                                               | Host32.NetLab.Home
| TargetConfig.Host.Datastore              | The datastore on your physical ESXi host                                          | Local_VMs
| TargetConfig.Host.PortGroup.RouterUplink | The portgroup that will connect your Pod to your physical network                 | Lab-Routers
| Nested_Router.Protocol                   | The routing method for routing traffic between your Pod and your physical network | OSPF
 <br>

### licenses.yml (TBD)
In licenses.yml you store your license keys for the different products. 
cp licenses_sample.yml config.yml

### software.yml (TBD)
In software.yml we've defined the poducts and versions that can be deployed with the scripts.
cp software_sample.yml config.yml

## Create the software library (TBD)

## Create the Pod configuration (TBD)

## Start the Pod deployment (TBD)

## Access the Pod's components (TBD)