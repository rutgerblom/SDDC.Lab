# vsphere-nsxt-lab-deploy
A set of Ansible Playbooks to help automate the deployment of vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes. <br/>

#### Table of Contents

1. [Description](#description)
1. [Setup](#setup)
    * [Requirements](#Requirements)
    * [Answerfile.yml](#Answerfile)
1. [Diagram](#Diagram)
1. [Usage](#Usage)
1. [Compatibility](#Compatibility)
1. [Development](#Development)
1. [Credits](#Credits)

## Description

This repository contains a set of Ansible Playbooks that will deploy and configure vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes.<br/>
The primary use case is speedy provisioning of a consistent lab environment. 

## Setup

Now updated for vSphere 7.0 and NSX-T 3.0. Also verified to work with vSphere 6.7 and NSX-T 2.5.1 (just swap the ISOs/OVAs).<br/>
Tested in an environment with at least one physical ESXi hosts managed by vCenter.<br/>
<br/>
Other components used that are **not** part of this deployment are a FRRouting VM for routing within the nested environment and an NFS datastore availabe to the nested ESXi hosts. vSAN could be used too, but I have not tested this yet.<br/>
<br/>
I also recommend having a DNS/NTP/AD server available to the nested environment to host something like a "lab.local" zone and have proper time synchronization.<br/>

### Diagram

Below a simple diagram over the physical environment. This will be deployed on the physical ESXi host using the default settings in answerfile.yml<br/>
<br/>
![Physical overview](/images/vsphere-nsxt-deploy-phys.png)

### Prerequisites

* apt install ansible <br/>
* apt install sshpass python-pip git <br/>
* pip install vim <br/>
* pip install pyvmomi <br/>

* ESXi and VCSA ISOs (6.7 or 7.0) as well as the NSX-T Manager and NSX-T Edge OVAs (2.5 or 3.0). Place these in the /iso directory of your Ansible control node. This path can be adjusted in the answerfile.<br/>

### Answerfile

Edit and adjust the answerfile.yml according to your needs! It's a very easy way to customize your deployment.

## Usage

ansible-playbook deploy.yml

## Compatibility

Tested to work with:<br/> 
* Ubuntu 18.04 as the control node<br/>
* Ansible 2.9.6 <br/>
* ESXi version 6.7 and 7.0 <br/>
* vCenter version 6.7 and 7.0 <br/>
* NSX-T version 2.5 and 3.0 <br/>

## Development

TODO: Automate configuration of logical networking in NSX-T <br/>
TODO: Include diagram for nested environment in README.md<br/>
TODO: Optimize / structurize answerfile.yml<br/>

## Credits

Credits go to Yasen Simeonov and his project at https://github.com/yasensim/vsphere-lab-deploy. This project is largely based on his.