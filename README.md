# vsphere-nsxt-lab-deploy
A set of Ansible Playbooks that help automate the deployment of vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes. <br/>

#### Table of Contents

1. [Description](#description)
1. [Setup](#setup)
    * [Dependencies](#Dependencies)
    * [Answerfile.yml](#answerfile.yml)
1. [Usage](#usage)
1. [Compatibility](#Compatibility)
1. [Development](#Development)
1. [Credits](#Credits)

## Description

This repository contains a set of Ansible Playbooks that deploy and configure vCenter, nested ESXi, NSX-T Manager, and NSX-T Edge nodes. 

## Setup

Now updated for vSphere 7.0 and NSX-T 3.0. Also verified to work with vSphere 6.7 and NSX-T 2.5.1<br/>
Tested in an environment with at least one physical ESXi hosts managed by vCenter.<br/>
Other components include a FRRouting VM for routing within the nested environment and a NFS datastore availabe to the nested ESXi hosts. vSAN could be used too, but I did not test this yet.<br/>
I recommend having a DNS server available to the nested environment to host something like a "lab.local" zone.<br/>

### Dependencies

apt install ansible <br/>
apt install sshpass python-pip git <br/>
pip install vim <br/>
pip install pyvmomi <br/>

ESXi and VCSA ISOs (6.7 or 7.0) as well as the NSX-T Manager and NSX-T Edge OVAs (2.5 or 3.0). Place all of these in /iso <br/>

### answerfile.yml

Edit and adjust the answerfile.yml according to your needs!

## Usage

ansible-playbook deploy.yml

## Compatibility

Ansible => 2.7 is required <br/>
ESXi version 6.7 and above is supported <br/>
VCSA version 6.7 and above is supported <br/>
NSX-T version 2.5 and above is supported <br/>

## Development

TODO: Configure stuff in NSX-T <br/>
TODO: Include a diagram in README.md<br/>

## Credits

Credits go to Yasen Simeonov and his project at https://github.com/yasensim/vsphere-lab-deploy. This project is largely based on his.