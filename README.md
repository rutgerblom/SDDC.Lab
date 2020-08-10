**Please note that this branch is not production-ready!!  Use the "master" branch instead.**

     _________________  _____       _           _     
    /  ___|  _  \  _  \/  __ \     | |         | |    
    \ `--.| | | | | | || /  \/     | |     __ _| |__  
     `--. \ | | | | | || |         | |    / _` | '_ \ 
    /\__/ / |/ /| |/ / | \__/\  _  | |___| (_| | |_) |
    \____/|___/ |___/   \____/ (_) \_____/\__,_|_.__/ 
                                                      
                                                      
         _                          _____             
        | |                        / __  \            
      __| | _____   __________   __`' / /'            
     / _` |/ _ \ \ / /______\ \ / /  / /              
    | (_| |  __/\ V /        \ V / ./ /___            
     \__,_|\___| \_/          \_/  \_____/            


## Table of Contents

* [Description](#Description)
* [Requirements](#Requirements)
* [Preparations](#Preparations)
* [Usage](#Usage)


## Description

This repository contains Ansible scripts that perform fully automated deployments of complete VMware SDDC Pods. Each Pod contains:
* A Router 
* vCenter Server
* ESXi Hosts
* NSX-T Manager
* NSX-T Edge Nodes
* vRealize Log Insight
* A DNS Server (multi-Pod)

The primary use case is consistent and speedy provisioning of nested VMware SDDC lab environments.

## Requirements

* A physical standalone ESXi host running version 6.7 or higher
* The physical standalone ESXi host hostname must be resolvable by DNS.
* A virtual machine with a modern version of Ubuntu (used as the Ansible Controller)
* For deploying NSX-T you need an NSX-T license (Check out [VMUG Advantage](https://www.vmug.com/membership/vmug-advantage-membership) or the [NSX-T Product Evaluation Center](https://my.vmware.com/web/vmware/evalcenter?p=nsx-t-eval)).
* Access to VMware product installation media
* A layer-3 switch with an appropriate OSPFv2 configuration matching the OSPFv2 settings in your config.yml file. This is used for dynamic routing between Pods and your physical network.
* The default settings require DNS name resolution. It's recommended to deploy the pre-configured DNS server for this purpose.
* If IPv6 deployment is enabled:
  * The Ansible Controller must be IPv6 enabled
  * DNS server must be IPv6 enabled
  * DNS server must have IPv6 forward and reverse zones
  * Within the Pod, only the following components are currently configured with IPv6:
    * Router (All interfaces)
    * NSX-T Segments
    * NSX-T eBGP Peering with the Router

## Preparations

* Install the required software on your Ansible Controller:
  * sudo apt install python3 python3-pip xorriso
  * pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython
  * git clone https://github.com/rutgerblom/SDDC.Lab.git 
  * git checkout dev-v2

* Copy/rename the sample files:
  * cp config_sample.yml config.yml
  * cp licenses_sample.yml licenses.yml
  * cp software_sample.yml software.yml

* Modify **config.yml** and **licenses.yml** according to your needs and your environment

* Create the Software Library directory structure using:
  * sudo ansible-playbook utils/util_CreateSoftwareDir.yml

* Add installation media to the corresponding directories in the Software Library (/Software)

## Usage

To deploy a Pod:
1. Generate a Pod configuration with:  
**ansible-playbook playbooks/createPodConfig.yml**

1. Start a Pod deployment per the instructions. For example:  
**sudo ansible-playbook -e "@/home/ubuntu/Pod-230-Config.yml" deploy.yml**

Deploying an SDDC Pod will take somewhere between 1 and 1.5 hours depending on your environment and Pod configuration.

Similary you remove a Pod with:  
**sudo ansible-playbook -e "@/home/ubuntu/Pod-230-Config.yml" undeploy.yml**

