
     _________________  _____       _           _     
    /  ___|  _  \  _  \/  __ \     | |         | |    
    \ `--.| | | | | | || /  \/     | |     __ _| |__  
     `--. \ | | | | | || |         | |    / _` | '_ \ 
    /\__/ / |/ /| |/ / | \__/\  _  | |___| (_| | |_) |
    \____/|___/ |___/   \____/ (_) \_____/\__,_|_.__/ 


## Table of Contents

* [Description](#Description)
* [Requirements](#Requirements)
* [Recommendations](#Recommendations)
* [Preparations](#Preparations)
* [Usage](#Usage)
* [More Information](More-Information)


## Description

This repository contains Ansible scripts that perform fully automated deployments of complete VMware SDDC Pods. Each Pod contains:
* A [VyOS](https://www.vyos.io/) Router
* vCenter Server
* ESXi Hosts
* NSX-T Local Manager
* NSX-T Edge Nodes
* vRealize Log Insight
* A DNS Server (multi-Pod)

The primary use case is consistent and speedy provisioning of nested VMware SDDC lab environments.

## Requirements
The following are the requirements for successful Pod deployments:

* A physical standalone ESXi host running version 6.7 or higher.
* The physical standalone ESXi host hostname must be resolvable by DNS.
* A virtual machine with a modern version of Ubuntu (used as the Ansible controller)
* The default deployment settings require DNS name resolution. Your can leverage an existing DNS server, but it must be configured with the required forward and reverse zones and support dynamic updates.
* Access to VMware product installation media.
* For deploying NSX-T you will need an NSX-T license (Check out [VMUG Advantage](https://www.vmug.com/membership/vmug-advantage-membership) or the [NSX-T Product Evaluation Center](https://my.vmware.com/web/vmware/evalcenter?p=nsx-t-eval)).
* If IPv6 deployment is enabled (Deploy.Setting.IPv6 = True):
  * Pod.BaseNetwork.IPv6 must be a fully expanded /48 IPv6 network prefix.  By default, [RFC4193](https://tools.ietf.org/html/rfc4193) ULA fd00::/48 prefix is used.
  * Router Version should be set to "Latest" (default)
  * Nested_Router.Protocol must be set to "OSPF" (default), as "Static" is not supported
  * It is recommended that the physical layer-3 switch be configured with OSPFv3 enabed on the Lab-Routers segment
  * The Ansible Controller must be IPv6 enabled
  * DNS server must be IPv6 enabled
  * DNS server must have IPv6 forward and reverse zones
  * Within each Pod, only the following components are currently configured with IPv6:
    * Nested VyOS Router (All interfaces)
    * NSX-T Segments
    * NSX-T eBGP Peering with the Router

## Recommendations
The following are recommendations based on our experience with deploying Pods:

* Use a physical layer-3 switch with appropriate OSPF configuration matching the OSPF settings in your config.yml file. Dynamic routing between your Pods and your physical network and will make your life easier.
* Hardware configuration of the physical standalone ESXi host:
  * 2 CPUs (10 cores per CPU)
  * 320 GB RAM
  * 1 TB storage capacity (preferably SSD). Either DAS or 10 Gbit NFS/iSCSI
* Virtual hardware configuration of the Ansible controller VM:
  * 2 CPUs
  * 16 GB RAM
  * 150 GB hard disk
  * VMware Paravirtual SCSI controller
  * VMXNET 3 network adapter
* Deploy the Ansible controller VM on the same ESXi host as where you will deploy your Pod.
* Deploy the pre-configured DNS server for DNS name resolution within Pods instead of using your own.

## Preparations

* Configure your physical network:
  * Create an Lab-Routers VLAN used as transit segment between your layer-3 switch and the Pod [VyOS](https://www.vyos.io/) router.
  * Configure OSPFv2/OSPFv3 on the Lab-Routers segment.

* Install the required software on your Ansible Controller:
  * sudo apt install python3 python3-pip xorriso
  * pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython
  * sudo pip3 install weasyprint
  * git clone https://github.com/rutgerblom/SDDC.Lab.git 

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

## More Information
For detailed installation, preparation, and deployment steps, please see the "[Deploying your first SDDC.Lab Pod](FirstPod.md)" document.