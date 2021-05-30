     _________________  _____       _           _               ___ 
    /  ___|  _  \  _  \/  __ \     | |         | |             /   |                 Developed By
    \ `--.| | | | | | || /  \/     | |     __ _| |__   __   __/ /| |          --------------------------
     `--. \ | | | | | || |         | |    / _` | '_ \  \ \ / / /_| |          Rutger Blom  &  Luis Chanu
    /\__/ / |/ /| |/ / | \__/\  _  | |___| (_| | |_) |  \ V /\___  |          NSX vExpert     VCDX #246
    \____/|___/ |___/   \____/ (_) \_____/\__,_|_.__/    \_/     |_/

# Deploying your first SDDC.Lab Pod

## Table of Contents
* [Configure your physical network](#Configure-your-physical-network)
* [Configure your physical ESXi host](#Configure-your-physical-ESXi-host)
* [Install your Ansible Controller](#Install-your-Ansible-Controller)
* [Prepare your Pod configuration files](#Prepare-your-Pod-configuration-files)
  * [config.yml](#configyml)
  * [licenses.yml](#licensesyml)
  * [software.yml](#softwareyml)
* [Create your software library](#Create-your-software-library)
* [Generate your Pod configuration](#Generate-your-Pod-configuration)
* [Start your Pod deployment](#Start-your-Pod-deployment)
* [Access your Pod's components](#Access-your-Pod's-components)

## Configure your network
For detailed information regarding the Pod networking, please see the [README](README.md) file.

As setting up the physical networking is one area where many of our users run into issues, we are providing a sample configuration from a working environment.  The configuration is provided "as-is", without any support, warranty, or guarantees.  The configuration may require additional modifications for your environment.

| Manufacture | Switch Model | Configuration File |
|-------------|--------------|--------------------|
| Cisco Systems | [Nexus 3048](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-3000-series-switches/data_sheet_c78-685363.html?dtid=osscdc000283) | [Cisco Nexus 3048 Configuration](misc/Cisco_Nexus-3048_Running-Configuration) |

## Configure your physical ESXi host(s)
The scripts support deploying Pods on a standalone ESXi host or on ESXi managed by vCenter. ESXi/vCenter must be on version 6.7 or newer. Regardless of deployment target you need to make sure that the following is availble to the ESXi host(s):

* A datastore where the Pod VMs will be stored
* A portgroup configured with the VLAN ID of the Router Uplink segment (i.e. Lab-Routers)

## Install your Ansible controller

The Ansible controller is the machine from which you will run the Ansible scripts. We recommend installing a modern version of [Ubuntu](https://ubuntu.com/download) on a dedicated virtual machine. This VM can be connected to any VLAN as long as it:

* Can access the physical ESXi host or the vCenter Server
* Can reach the Router Uplink segment and the Pod networks behind the [VyOS](https://www.vyos.io/) router
* Has Internet access

### Software
After you've installed the Ubuntu OS and applied the latest updates, some additional software is required to turn this machine into an Ansible controller for your SDDC.Lab Pods. You can simply copy and paste the commands below. Installation of the additional software will only take some minutes.  This project requires Ansible
version 2.10.x.

1. Python, pip, and xorriso:  
**udo apt install python3 python3-pip xorriso git**

1. Ansible and the required Python modules:  
**sudo pip3 install ansible pyvim pyvmomi netaddr jmespath dnspython**

1. The required Ansible modules
**ansible-galaxy collection install community.general community.vmware ansible.posix**

1. The SDDC.Lab repository cloned to an appropriate location on your Ubuntu machine (e.g. $HOME) with:  
**git clone https://github.com/rutgerblom/SDDC.Lab.git**

## Prepare your Pod configuration files
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
    templates_sample.yml
    undeploy.yml

Four files in the root of the SDDC.Lab directory require your attention:
* config_sample.yml
* licenses_sample.yml
* software_sample.yml
* templates_sample.yml

Start by creating your own copies of the sample configuration files:
* cp config_sample.yml config.yml
* cp licenses_sample.yml licenses.yml
* cp software_sample.yml software.yml
* cp templates_sample.yml templates.yml

### config.yml
This file contains all of the configuration and settings for the Pod you're about to deploy. Its contents are organized in several different sections and data structures.
<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="images/config_yml.png" alt="licenses.yml" width="50%"/>
<br>
<br>
There are many settings that you ***can*** change, but only a few that you ***must*** change. Especially when deploying your first Pod we strongly recommend that you keep changes to a minimum.

- The table below contains the settings that ***must*** match your environment:

    | Setting                                          | Description                                                                                                          | Default Value
    | :---                                             | :---                                                                                                                 | :---
    | Common.Password.Physical                         | The password used to log in as root (standalone ESXi) or as administrator@vsphere.local (vCenter)                    | VMware1!
    | Common.DNS.Server1.IPv4/IPv6                     | The IP address of the DNS server to be used by the nested environment. You only need to change this if you decide not to deploy the SDDC.Lab DNS/NTP server | 10.203.0.5
    | Common.NTP.Server1.IPv4/IPv6                     | The IP address of the NTP server to be used by the nested environment. You only need to change this if you decide not to deploy the SDDC.Lab DNS/NTP server | 10.203.0.5
    | TargetConfig.Deployment                          | The deployment target. Can be either "Host" or "vCenter"                                                              | Host    
    | TargetConfig.Host/vCenter.FQDN                   | The FQDN of your physical ESXi host or your vCenter Server                                                           | Host32.NetLab.Home/NetLab-vCenter.NetLab.Local 
    | TargetConfig.vCenter.DataCenter                  | The DataCenter object where the lab Pods are deployed (only required when deploying to vCenter)                      | SDDC
    | TargetConfig.vCenter.Cluster                     | The vSphere cluster within DataCenter wher the lab Pods are deployed (only required when deploying to vCenter)       | Lab-Cluster 
    | TargetConfig.Host/vCenter.Datastore              | The datastore that will be used to store Pod VMs                                                                     | Local_VMs/Shared_VMs
    | TargetConfig.Host/vCenter.PortGroup.RouterUplink | The portgroup that connects your Pod to the transit segment (e.g. the physical network)                              | Lab-Routers
    | Nested_Router.Protocol                           | The routing protocol used for routing traffic between your Pod and your physical network. Valid options are "Static", "BGP", "OSPF" or "BOTH" (OSPF and BGP)                                    | BOTH

Change either your environment or these settings so that they match.

### licenses.yml
Licenses.yml contains the licenses that you want to assign to the software within the Pod. Just like config.yml this file is organized in a data structure.
<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="images/licenses_yml.png" alt="licenses.yml" width="50%"/>
<br>
<br>
The file contains many example entries which you are free to change or remove. A typical licenses.yml might look something like this:

    ---
    License:
      VMware:
        vCenter:
          Name: vCenter Server
          Licenses:
          - Quantity: 2
            Version: "7.[0-9]"
            Measure: Instance
            KeyCode: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
            Edition: Standard
            Comment:
        ESXi:
          Name: vSphere ESXi Host
          Licenses:
          - Quantity: 16
            Version: "7.[0-9]"
            Measure: CPU
            KeyCode: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
            Edition: Enterprise Plus
            Comment: 
        NSXT:
          Name: NSX Transformers
          Licenses:
          - Quantity: 16
            Version: "[23].[0-9]"
            Measure: CPU
            KeyCode: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
            Edition: Enterprise Plus
            Comment: 
        vSAN:
          Name: vSAN
          Licenses:
          - Quantity: 16
            Version: "[7].[0-9]"
            Measure: CPU
            KeyCode: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
            Edition: Enterprise
            Comment: 
        vRLI:
          Name: vRealize Log Insight
          Licenses:
          - Quantity: 25
            Version: "[8].[0-9]"
            Measure: OSI
            KeyCode: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
            Edition: N/A
            Comment: 

Are license keys required? Only for NSX-T. The other components will deploy fine without license keys and are operational for a limited amount of time.<br>
NSX-T license keys can be obtained via [VMUG Advantage](https://www.vmug.com/membership/vmug-advantage-membership) or the [NSX-T Product Evaluation Center](https://my.vmware.com/web/vmware/evalcenter?p=nsx-t-eval).

### software.yml
Software.yml contains a data structure with the software that can currently be deployed using the scripts. It's used by most of the Ansible scripts as well. The directory structure of the [software library](#Create-your-software-library) is based on the entries in this file.<br> 
You would normally not make any changes to this file and even more so when you're deploying your first Pod. Leave it as it is.
<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="images/software_yml.png" alt="software.yml" width="50%"/>
<br>
## Create your software library
Now that your configuration files have been prepared, you can continue with creating the software library. The first thing you need to do is create the software library's directory structure. We've created an Ansible script that does this for you. Simply run:

* **sudo ansible-playbook utils/util_CreateSoftwareDir.yml**

This script creates an empty directory structure at **/Software** on your Ansible controller that will look something like this:

    /Software/
    ├── Ubuntu
    │   └── Server
    │       └── v20.04.1
    ├── VMware
    │   ├── ESXi
    │   │   ├── v6.7.0U3B
    │   │   ├── v7.0.0
    │   │   └── v7.0.0B
    │   ├── NSX-T
    │   │   ├── v3.0.0
    │   │   ├── v3.0.1
    │   │   └── v3.0.1.1
    │   ├── vCenter
    │   │   ├── v6.7.0U3B
    │   │   ├── v6.7.0U3G
    │   │   ├── v7.0.0
    │   │   ├── v7.0.0A
    │   │   ├── v7.0.0B
    │   │   └── v7.0.0C
    │   └── vRLI
    │       └── v8.1.1
    └── VyOS
        └── Router
            ├── Latest
            └── v1.1.8

The next step is to populate the structure with the required installation media. Some deployment scripts will download the installation media for you when it's missing in the software library. Currently both Ubuntu Server and VyOS Router are downloaded when absent. VMware products always need to be downloaded by you.


In **config.yml** under **Deploy.Software** you can see (and change) which version of a particular software is going to be deployed and thus needs to be present in the software library. The default setting is to deploy the latest supported combination of versions. For your first Pod we recommend that you leave it like that.

A populated software library could look something like this:

    /Software/
    ├── Ubuntu
    │   └── Server
    │       └── v20.04.1
    ├── VMware
    │   ├── ESXi
    │   │   ├── v6.7.0U3B
    │   │   ├── v7.0.0
    │   │   └── v7.0.0B
    │   │       └── VMware-VMvisor-Installer-7.0b-16324942.x86_64.iso
    │   ├── NSX-T
    │   │   ├── v3.0.0
    │   │   ├── v3.0.1
    │   │   └── v3.0.1.1
    │   │       └── nsx-unified-appliance-3.0.1.1.0.16556500.ova
    │   ├── vCenter
    │   │   ├── v6.7.0U3B
    │   │   ├── v6.7.0U3G
    │   │   ├── v7.0.0
    │   │   ├── v7.0.0A
    │   │   ├── v7.0.0B
    │   │   └── v7.0.0C
    │   │       └── VMware-VCSA-all-7.0.0-16620007.iso
    │   └── vRLI
    │       └── v8.1.1
    │           └── VMware-vRealize-Log-Insight-8.1.1.0-16281169_OVF10.ova
    └── VyOS
        └── Router
            ├── Latest
            └── v1.1.8

## Generate your Pod configuration
You can now continue with generating your Pod configuration. This is the process where all of your settings are combined into a static configuration file. To generate this configuration file you run:

* **ansible-playbook playbooks/createPodConfig.yml**

The script needs to know where your configuration file is located:

    In which directory is the Pod-Config file you want to have prepared located? [/home/ubuntu/SDDC.Lab/]: 

The default path is the current working directory. If this is correct you simply press **\<Enter>**.

The script then wants to know the name of your configuration file:

    What is the name of the configuration file that you would like to have prepared? [config.yml]:

If you have been following this guide, the name of your configuration file will be **config.yml** and you can simply press **\<Enter>** here.

The static configuration file is now generated. On average this process will take between 5-15 minutes, but may vary depending on the size of your lab, and the speed of your Ansible controller. 

The static configuration file will have the following name format **Pod-\<SiteCode>-Config.yml**.

## Start your Pod deployment (TBD)

## Access your Pod's components (TBD)