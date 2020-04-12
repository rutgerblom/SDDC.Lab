# vsphere-nsxt-lab-deploy
A set of Ansible Playbooks that automate the deployment and configuration of a complete nested vSphere environment and NSX-T. <br/>

#### Table of Contents

1. [Description](#description)
1. [Setup](#setup)
    * [Deployment](#Deployment)
    * [Requirements](#Requirements)
    * [Answerfile.yml](#Answerfile)
1. [Diagrams](#Diagrams)
1. [Usage](#Usage)
1. [Interoperability](#Interoperability)
1. [Development](#Development)
1. [Credits](#Credits)

## Description

This repository contains a set of Ansible Playbooks that will deploy and configure vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes. The primary use case is speedy provisioning of a consistent nested lab environment. 

## Setup

Now updated for vSphere 7.0 and NSX-T 3.0. Also verified to work with vSphere 6.7 and NSX-T 2.5 (just swap the ISOs/OVAs).<br/>
Tested in an environment with a physical ESXi host managed by its own vCenter.<br/>
<br/>
Other components used that are **not** part of this deployment are a FRRouting VM for routing within the nested environment and an NFS datastore availabe to the nested ESXi hosts. vSAN could be used too, but I have not tested this yet.<br/>
<br/>
I also recommend having DNS/NTP/AD available to the nested environment to host something like a "lab.local" zone and have proper time synchronization and authentication.<br/>

### Deployment

Running the Playbooks as defined in the **deploy.yml** will deploy the following:<br/>
1. Create a vSwitch and port groups on the physical ESXi
1. Deploy and configure a vCenter Sever Appliance
1. Deploy 5 ESXi VMs
1. Configure the nested vSphere environment:
   * Configure the ESXi hosts
   * Create and configure a Distributed Switch
   * Add ESXi hosts to vCenter (3 hosts in the "Compute" vSphere cluster and 2 hosts in the "Edge" cluster)
1. Configure NSX-T:
   * Deploy NSX Manager
   * Register vCenter as a Compute Manager in NSX Manager
   * Create NSX-T Transport Zones
   * Create NSX-T IP pool
   * Create NSX-T Uplink Profiles
   * Deploy two NSX-T Edge Transport Nodes
   * Create NSX-T Edge Cluster
   * Create NSX-T Transport Node Profile
   * Attach NSX-T Transport Node Profile to the "Compute" vSphere cluster (this will effectively install NSX-T bits and configuration on the ESXi hosts in that cluster)

### Diagrams

A simple diagram over the physical environment. This will be deployed on the physical ESXi host when using the default settings in **answerfile.yml**<br/>
<br/>
![Physical overview](/images/vsphere-nsxt-deploy-phys.png)<br/>
Another diagram showing some more details about the nested vSphere environment. Again using the default settings in **answerfile.yml**<br/>
<br/>
![Logical overview](/images/vsphere-nsxt-deploy-log.png)<br/>

### Prerequisites

* A physical ESXi host managed by vCenter
* ovftool (free download from VMware)
* apt install python3
* apt install ansible <br/>
* apt install sshpass python-pip git <br/>
* pip install vim <br/>
* pip install pyvmomi <br/>
* apt install xorriso<br/>

* ESXi and VCSA ISOs (6.7 or 7.0) as well as the NSX-T Manager OVA (2.5 or 3.0). Place these in the /iso directory of your Ansible control node. This path can be changed in **answerfile.yml**.<br/>

### Answerfile

Edit and adjust **answerfile.yml** according to your needs. In **deploy.yml** you control what gets deployed. It's very easy to customize your deployment.

## Usage

ansible-playbook deploy.yml

## Interoperability

Confirmed to be working with:<br/> 
* Ubuntu 18.04 as the OS for the Ansible Controller<br/>
* Ansible 2.9.6 <br/>
* ESXi version 6.7 and 7.0 <br/>
* vCenter version 6.7 and 7.0 <br/>
* NSX-T version 2.5 and 3.0 <br/>

## Development

TODO: Optimize / structurize answerfile.yml<br/>

## Credits

Credits go to **Yasen Simeonov** and his project at https://github.com/yasensim/vsphere-lab-deploy. This project is largely based on his.