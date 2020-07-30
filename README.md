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

## Description

This repository contains Ansible code that performs automated deployments of complete VMware SDDC pods. Each pod contains a router, vCenter, ESXi hosts, NSX-T Manager, and NSX-T Edge nodes. The primary use case is speedy provisioning of consistent nested vSphere/NSX-T lab environments.

## Requirements

* A physical standalone ESXi host running version 6.7 or higher
* The physical standalone ESXi host hostname must be resolvable by DNS.
* An Ubuntu 18.04/20.04 VM (Ansible controller)
* For deploying NSX-T you need an NSX-T license (Check out [VMUG Advantage](https://www.vmug.com/membership/vmug-advantage-membership) or the [NSX-T Product Evaluation Center](https://my.vmware.com/web/vmware/evalcenter?p=nsx-t-eval)).
* A layer-3 switch with an appropriate OSPFv2 configuration matching the OSPFv2 settings in your config.yml file (for dynamic routing between your pods and the physical network).
* The default settings require DNS name resolution.
* If IPv6 deployment is enabled:
  * The Ansible controller must be IPv6 enabled
  * DNS server must be IPv6 enabled
  * DNS server must have IPv6 reverse zone

## Preparations

On the Ansible controller:
1. Install the required software:
  * sudo apt install python3 python3-pip xorriso
  * pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython
  * git clone https://github.com/rutgerblom/SDDC.Lab.git 
  * git checkout dev-v2
1. Copy/rename the sample files:
  * cp config_sample.yml config.yml
  * cp licenses_sample.yml licenses.yml
  * cp software_sample.yml software.yml
1. Modify **config.yml** and **licenses.yml** according to your needs and your environment
1. Create the software library directory structure:
  * sudo ansible-playbook utils/util_CreateSoftwareDir.yml
1. Add installation ISOs and OVAs to the directories in the software library (/Software)


## Usage

To deploy a Pod:
1. Generate a Pod configuration:
  * ansible-playbook playbooks/createPodConfig.yml
1. Start a Pod deployment as instructed by the createPodConfig Playbook. For example: **sudo ansible-playbook -e "@/home/serbl/Pod-230-Config.yml" deploy.yml**
