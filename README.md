# vsphere-nsxt-lab-deploy
A set of Ansible Playbooks that help automate the deployment of vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes. <br/>

#### Table of Contents

1. [Description](#description)
1. [Setup](#setup)
    * [Dependencies](#Dependencies)
    * [Answerfile.yml](#answerfile.yml)
1. [Diagram](#Diagram)
1. [Usage](#usage)
1. [Compatibility](#Compatibility)
1. [Development](#Development)
1. [Credits](#Credits)

## Description

This repository contains a set of Ansible Playbooks that deploy and configure vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes. 

## Setup

Now updated for vSphere 7.0 and NSX-T 3.0. Also verified to work with vSphere 6.7 and NSX-T 2.5.1 (just swap the ISOs/OVAs).<br/>
Tested in an environment with at least one physical ESXi hosts managed by vCenter.<br/>
<br/>
Other components used that are not part of this deployment are a FRRouting VM for routing within the nested environment and an NFS datastore availabe to the nested ESXi hosts. vSAN could be used too, but I have not tested this yet.<br/>
<br/>
I also recommend having a DNS/NTP/AD server available to the nested environment to host something like a "lab.local" zone and have proper time synchronization.<br/>

### Diagram

Below a simple diagram over the physical environment. This will be deployed on the physical ESXi host using the default settings in answerfile.yml<br/>
<br/>
![Physical overview](/images/vsphere-nsxt-deploy-phys.png)

### Dependencies

apt install ansible <br/>
apt install sshpass python-pip git <br/>
pip install vim <br/>
pip install pyvmomi <br/>

ESXi and VCSA ISOs (6.7 or 7.0) as well as the NSX-T Manager and NSX-T Edge OVAs (2.5 or 3.0). Place all of these in the /iso directory of your Ansible control node.<br/>

### answerfile.yml

Edit and adjust the answerfile.yml according to your needs! I've parameterized as much as possible so it's easier to customize your deployment.

## Usage

ansible-playbook deploy.yml

## Compatibility

Ansible => 2.7 is required <br/>
ESXi version 6.7 and above is supported <br/>
VCSA version 6.7 and above is supported <br/>
NSX-T version 2.5 and above is supported <br/>

## Development

TODO: Configure stuff in NSX-T <br/>
TODO: Include more diagrams in README.md<br/>
TODO: Clean up / structurize answerfile.yml<br/>
TODO: Parameterize more<br/>

## Credits

Credits go to Yasen Simeonov and his project at https://github.com/yasensim/vsphere-lab-deploy. This project is largely based on his.