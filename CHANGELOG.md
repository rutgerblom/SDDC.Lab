# Changelog
```
██████  ███████ ██    ██       ██    ██ ██████
██   ██ ██      ██    ██       ██    ██      ██
██   ██ █████   ██    ██ █████ ██    ██  █████
██   ██ ██       ██  ██         ██  ██       ██
██████  ███████   ████           ████   ██████
```

## Dev-v3.0.0 16-MARCH-2021

### Added by Luis

- Changed Lab-Routers area from 666 to 0 (i.e. Backbone area) to facilitate sharing of routes between sites if NSX-T is reconfigured to use OSPF versus eBGP.
  This reconfiguration to use OSPF is not supported by automation, and would have to be done manually afterwards by the user.

## Dev-v3.0.0 31-MARCH-2021

### Added by Luis

- Commented Flash/HHD drive type configuration in ESXi kickstart templates.  Implemented Flash/HDD configuration in custom Ansible module called set_drive_type.  This was needed to support ESXi v7.0 Update 2.
- Updated NSX-T Ansible modules to latest versions found in VMware's NSX-T repository in GitHub.
- Added "SetAsDefault" option for NSX-T TransportZones.  When set to "True", the Transport Zone is set as "Default".
- Added "SetAsDefault" option to existing TransportZones in sample_config.yml file.
- Modified RAM configuration for Nested_ESXi hosts.  Changed all clusters to use 16GB RAM per host.
- Updated sample_config.yml to use the latest versions of ESXi (v7.0U2), NSX-T (v3.1.1), and vRLI (v8.3.0).
- Corrected issue with License_vSphere.yml module where it would fail if a product didn't have licenses.

## Dev-v3.0.0 02-APRIL-2021

### Added by Rutger

- Added new variables to sample_config.yml that enable configuration of NSX-T Edge VM resource reservation settings.
- Updated the diagram in README.md.

## Dev-v3.0.0 6-APRIL-2021

### Added by Rutger

- Vendor, product and product version information is added to the annotation of the deployed virtual machines

## Dev-v3.0.0 06-APRIL-2021

### Added by Luis

- Added support for eBGP peering with physical Layer-3 Lab-Router, and it is currently ALWAYS enabled.  This functionality may change in the future, especially while in a 'dev' branch.  That said, keep a close eye out for changes around this feature.
- Both IPv4 and IPv6 peering implemented.
- Modified config_sample.yml configuration.
- Added flags to control the origination of Default Routes to eBGP Peers
- Corrected filename used for Pod-Router configuration during deployment
- Added "mtu 1500" statement to Eth0 in Pod-Router configuration
- Corrected type-O in config_sample.yml file
- Default ASN Values are as follows:
  - Lab-Router ASN is 65000
  - Pod-Router ASN is 65000 + Pod.Network
  - NSX-T EdgeVMs ASN is 65000 + Pod.Network + 1

## Dev-v3.0.0 07-APRIL-2021

### Added by Luis

- Changes have been made to the config_sample.yml configuration file with this change.
- Added additional options to Nested_Router.Protocol variable.  Valid options are now "Static", "OSPF", "BGP", and "BOTH" (BGP and OSPF).  This determines the routing protocol(s) used by the Pod-Router into the Lab-Routers network segment (i.e. North Bound).
- Within Nested_Router, the Neighboring BGP routers are now broken up into two (2) sections: Routers and NSXEdges.  Each of these sections are a list, so you can add additional neighbors to fit your needs.  The "Routers" list of bgp neighbors is only instantiated when Nested_Router.Protocol == BGP or BOTH.  The "NSXEdges" is always instantiated when a dynamic routing protocol is chosen.
- Changed the Nested_Router.Protocol value in config_sample.yml from OSPF to BOTH.

## Dev-v3.0.0 10-APRIL-2021

### Added by Rutger

- Added utility "utils/util_UpdateConfig.sh" that can be used to update/create a "config.yml" file with settings based on user input.
- Added utility "utils/util_PodState.yml" that can be used to change virtual machine state of all VMs in a Pod.

## Dev-v3.0.0 10-APRIL-2021

### Added by Luis

- Resolved ISO issues which didn't allow for simultaneous deployments.  Multiple Pod deployments can now be run at the same time.
- Changes have been made to the config_sample.yml configuration file with this change.
- Added new Deploy.Software.Option.UnmountISO variable, which controls if ISOs are unmounted during the deployment process.  Be sure to read comments for that new option.
- TargetConfig.ISOMount is now the base location where all ISOs are now mounted.  Individual ISOs are mounted in subdirectories below this location in the form of: Vendor_Product_Version.  So, vCenter would be: VMware_vCenter_7.00U2
- Converted all modules which mount ISOs to this new ISO mounting scheme.
- Pod_Config.j2 template modified to support the new variable

## Dev-v3.0.0 11-APRIL-2021

### Added by Rutger

- Converted to Ansible FQCN in script "UnDeploy.yml"

## Dev-v3.0.0 11-APRIL-2021

### Added by Luis Chanu

- Modified ESXi syslog firewall rule entry to permit the server to source from all local IP addresses.

## Dev-v3.0.0 12-APRIL-2021

### Added by Luis Chanu

- Changes have been made to the Pod_Config.j2 template, so please re-run CreatePodConfig playbook against all of your config files.
- Support for "Legacy" VyOS image (v1.1.8) has been removed/deprecated.  All deployments must now use "Latest" for the Router version.  If you have existing configuration files that are using "Legacy", please be sure to update them.
- ValidateConfiguration.yml playbook updated to verify that the Router version is "Latest".
- Added "FileExt" to all "Software" entries via the Jinja2 template.  This has been added to simplify the ability for an installation process to determine if the installation source is "iso" or "ova".
- The following files were updated, so please update your non-sample files:
  - software_sample.yml
  - templates_sample.yml

## Dev-v3.0.0 13-APRIL-2021

### Added by Luis Chanu

- Added support in concurrent Pod deployment to support vCenter Server Replication Partners.
- Created new 'CheckVcReplicationPartner.yml' playbook to verify Replication Partner vCenter Server is operational.  It pauses the Pod with the Replication Partner until the Replication Partner vCenter Server is operational.
- Added new 'CheckVcReplicationPartner.yml' playbook to Deploy.yml playbook.

## Dev-v3.0.0 14-APRIL-2021

### Added by Rutger

- Added a variable that controls the hardware version of the DNS server virtual machine. Default value is set to 13.
- The following file was updated so please update your non-sample file:
  - config_sample.yml

## Dev-v3.0.0 14-APRIL-2021

### Added by Luis Chanu

- Converted module references within Deploy.yml to use FQCNs
- Correct issue with DeployRouter.yml playbook where it would fail if router was already deployed

## Dev-v3.0.0 15-APRIL-2021

### Added by Rutger

- The generated Pod documentation will now contain information on whether NSX-T Edge was deployed or not.
- Converted module references within PrepareISOInstaller.yml, DeployVc.yml, and DeployDNSServer.yml to use FQCNs (ansible.posix.mount).
- Updated project documentation regarding the ansible.posix collection which is now required by some playbooks. Install this collection by running: **ansible-galaxy collection install ansible.posix** on your Ansible controller.

## Dev-v3.0.0 15-APRIL-2021

### Added by Luis Chanu

- Added additional documentation around Pod networking to the README.md file.
- Created Pod Logical Networking Overview network diagram to clearly show the networking components included in a Pod deployment.
- Added a santized Cisco Nexus 3048 running configuration for users to use as reference.
- Added table of switch configurations to the FirstPod.md document.

## Dev-v3.0.0 16-APRIL-2021

### Added by Rutger Blom

- Added support for deploying vRealize Log Insight 8.4.
- The following file was updated so please update your non-sample file:
  - software_sample.yml
- vRLI is now configured to use the NTP server specified in config.yml.
- Updated the header in the generated Pod HTML documentation.

## Dev-v3.0.0 18-APRIL-2021

### Added by Rutger Blom

- Added support for deploying NSX-T 3.1.2
- Updates to the documentation.

## Dev-v3.0.0 19-APRIL-2021

### Added by Luis Chanu

- Modified CreatePodConfig.yml playbook to redisplay the Pod deployment command at the end of the playbook.
- Due to failure while preparing vSphere 7.0U2 host with NSX-T v3.1.2 due to RAM disk running out of space, increased RAM in config_sample.yml for all clusters to 17GB.  In reality, only needs to be on hosts being prepared for NSX-T, but changed all for consistency.

## Dev-v3.0.0 28-APRIL-2021

### Added by Rutger Blom

- Added support for deploying vCenter 7.0U2A.
- The configured MTU settings for the nested ESXi vmkernel adapters are now applied.

## Dev-v3.0.0 30-APRIL-2021

### Added by Rutger Blom

- Updated the VyOS Router configuration j2 template with the new syntax for BGP configuration.
- A new version of the VyOS Rolling release is required so please remove or replace the following file with the latest version in your software library (if removed the router deployment script will download the latest version during deployment):
  - vyos-rolling-latest.iso  


<br>

***
<h1 style="text-align:center">SDDC.Lab Version 3.0 Released</h1>
<br>


## Release-v3.0.0 30-MAY-2021

### Added by Rutger Blom & Luis Chanu

- Released version 3 of the SDDC.Lab project.


```
██████  ███████ ██    ██       ██    ██ ██   ██
██   ██ ██      ██    ██       ██    ██ ██   ██
██   ██ █████   ██    ██ █████ ██    ██ ███████
██   ██ ██       ██  ██         ██  ██       ██
██████  ███████   ████           ████        ██
```

## Dev-v4.0.0 13-JUNE-2021

### Added by Luis Chanu

- Updated FirstPod.MD file
- Updated utils/util_CreateConfig.sh
- Renamed all instances of "RouterUplink" to "Uplink" in config_sample.yml
- IMPORTANT: Please recreate static Pod-Config files using CreatePodConfig.yml
- Added "Net.<Intf>.MTU" and "NET.<Intf>.Description" fields to config_sample.yml
- Added new "vyos_router_commands.j2" template to project (Name my change).  This is a work in progress of developing the VyOS configuration via the "SET" commands used by VyOS.

## Dev-v4.0.0 15-JUNE-2021

### Added by Luis Chanu

- Added "vyos.vyos" to the list of Ansible collections to install in the [README](README.md) file

## Dev-v4.0.0 15-JUNE-2021

### Added by Rutger Blom

- Added support for deploying NSX-T 3.1.2.1, vCenter 7.0 U2b, and ESXi 7.0 U2a

## Dev-v4.0.0 18-JUNE-2021

### Added by Rutger Blom

- Added VMware Tanzu to licenses_sample.yml (for future use)
- Removed some redundant example entries in licenses_sample.yml

## Dev-v4.0.0 20-JUNE-2021

### Added by Rutger Blom

 - Added a playbook that configures HA on the nested vSphere clusters.
 - The following file was updated so please update your non-sample file:
  - config_sample.yml

## Dev-v4.0.0 21-JUNE-2021

### Added by Rutger Blom

 - The nested ESXi vmkernel adapter MTU value is now fetched from the router interface (e.g. the vmkernel's default gateway)
 - Add support for deploying vRLI 8.4.1
 - The following files were updated so please update your non-sample files:
  - config_sample.yml
  - software_sample.yml

## Dev-v4.0.0 27-JUNE-2021

### Added by Rutger Blom

  - Due to failure while preparing nested ESXi 7.0 U2a hosts with NSX-T v3.1.2.1 due to RAM disk running out of space, increased RAM in config_sample.yml for all clusters to 18GB.  In reality, only needs to be on hosts being prepared for NSX-T, but changed all for consistency.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 27-JUNE-2021

### Added by Luis Chanu

  - VyOS Ansible modules requires the "Paramiko" module, so please be sure to use PIP3 to install it.  The README.md has been updated to now include this module as a requirement.
  - Due to SSH authentication failure with VyOS module, added "host_key_checking = false" to ansible.cfg file to permit SSH connections to succeed without first importing the hash.
  - Changes to VyOS router playbooks
    - Module DeployRouter.yml now not only deploys the VyOS router, but also performs basic configuration (Name, Eth0 IP Address, Floating default route, enable SSH).
    - Due to changing syntax of the VyOS "/config/config.boot" file with newer versions of VyOS, instead of creating that file and copying it to the VyOS router (as was previously done), we now develop the individual VyOS "SET" commands for the target configuration, then send those commands to the provisioned VyOS router.  Once that's done, we then 'commit' and 'save' the configuration.  The creation of the VyOS router configuration is performed by the new ConfigureRouter.yml playbook.
    - Added a pre-login message that shows the VyOS router name, along with a reminder that the login username is "vyos".
    - As a precaution, previous "DeployRouter.yml" and "vyos_router.j2" files have been renamed to *_OLD, respectively.  They will be removed once the new VyOS router deployment has been throughly tested.

## Dev-v4.0.0 05-JULY-2021

### Added by Rutger Blom
  
  - A vSphere Content Library is now created in the nested vCenter as part of the deployment.
  - Module "community.vmware.vmware_content_library_manager" requires the "setuptools" module and the "vSphere Automation SDK", so please be sure to use PIP3 to install them.  The README.md has been updated to now include these modules as a requirement. 
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 07-JULY-2021

### Added by Rutger Blom

  - Added a data structure for NSX-T Compute Managers to config_sample.yml
  - Compute Manager "Trust" enabled by default and configured if vCenter is not version 6
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 08-JULY-2021

### Added by Luis Chanu

  - Added a data structure for Nested_Router UserDefined commands to config_sample.yml
  - Added the ability for users to modify the VyOS Pod-Router configuration after it's deployed and the Pod baseline configuration is applied.  Users put the commands they want to be applied in a special file.  By default (configured in Nested_Router.UserConfig), the Pod specific router user configuration file is placed in the user's home directory, and is called "{{ SiteCode }}-Router-UserConfig.j2".  So, for example, for Pod #10, the file would be called "Pod-010-Router-UserConfig.j2".  This file is a Jinja2 template, so users can also utilize all the templating power of Jinja2 to generate their commands.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 10-JULY-2021

### Added by Rutger Blom

  - Added data structure, playbook, and template for enabling vSphere with Tanzu (Workload Management). These are preparations for including an option for automated deployment of vSphere with Tanzu in the future. This option is not part of the deployment yet.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 11-JULY-2021

### Added by Rutger Blom

  - Added a requirements.yml to the repository for easier installation of the required Ansible collections. The README.md has been updated to include an instruction on how to install the required Ansible collections using the repo's requirements.yml.

## Dev-v4.0.0 11-JULY-2021

### Added by Luis Chanu

  - Corrected missing "{" for annotation variable in DeployRouter.yml
  - Updated all module references in tests and utils directory playbooks to use FQCN
  - Added virtual IPv4 addresses variables to NSX-T GM and LM in config_sample.yml to prepare for future changes
  - The following file was updated so please update your non-sample file:
    - config_sample.yml
  - Created tests/ConfigureNsxLMVIP.yml to validate/verify VIP module functionality (Worked)
  - Added NSX-T LM VIP configuration task to deployNexManager.yml playbook

## Dev-v4.0.0 12-JULY-2021

### Added by Luis Chanu

  - The following changes were made to the config_sample.yml file:
    - Added FQDN_VIP entries for NSX-T LocalManager and GlobalManager
    - Added Common.PKI.ValidateCerts varilable with a default value of 'false'
  - The config_sample.yml file was updated so please update your non-sample configuration files, then rerun the CreatePodConfig.yml playbook to regenerate your static configuration files.

## Dev-v4.0.0 16-JULY-2021

### Added by Luis Chanu

  - Created test module "tests/UpdateDNSVIP.yml" module to populate NSX-T VIP entries into DNS.  This module is working, and the code is ready to be integrated into the two modules with touch DNS records.

## Dev-v4.0.0 17-JULY-2021

### Added by Luis Chanu

  - Integrated DNS VIP code into both "UpdateDNS.yml" and "CleanupDNS.yml" playbooks.  Tested both playbooks, and they completed without any issues.  Verified using utils/showdns that the NSX-T Global Manager and Local Manager VIPs were populated in DNS.

## Dev-v4.0.0 18-JULY-2021

### Added by Rutger Blom

  - Added the vSphere with Tanzu Workload Management playbooks to the deployment playbook.  Automated deployment of Workload Management is controlled in "config.yml" at "Deploy.Product.Tanzu.WorkloadManagement".  The default setting is "false" meaning that vSphere with Tanzu Workload Management is not deployed by default.
  - DNS forwarding is configured on the VyOS router's "VMNetwork" VLAN interface if "Deploy.Product.Tanzu.WorkloadManagement" is set to "true".
  - NSX-T is required for vSphere with Tanzu Workload Management (in this project) and as such conditionals have been added to the vSphere with Tanzu Workload Management playbooks that check whether NSX-T is deployed.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 23-JULY-2021

### Added by Rutger Blom

  - Added support for deploying NSX-T 3.1.3
  - The following file was updated so please update your non-sample file:
    - software_sample.yml

## Dev-v4.0.0 23-JULY-2021

### Added by Luis Chanu

  - Moved NSX-T GlobalManager and LocalManager VIP information to an entry below Nested_NSXT.Components in the config_sample.yml file.
  - Updated DNS playbooks, along with deployNsxManager.yml to use the newly created variables.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml
  - After updating your non-sample configuration files, be sure to recreate your static Pod configuration files by running "CreatePodConfig.yml" against each of the updated config files.

## Dev-v4.0.0 24-JULY-2021

### Added by Luis Chanu

  - Modifed CreateVds.yml to prune VLAN ID range on NSXEdgeUplink1 and NSXEdgeUplink2 uplinks to the VLAN ID range of the Pod being deployed.  Previously, it was allowing all VLANs (0-4094).

## Dev-v4.0.0 25-JULY-2021

### Added by Luis Chanu

  - Enabled OSPFv2 on Pod-Router NSX-T Edge facing interfaces (NSXEdgeUplink1 and NSXEdgeUplink2).
  - Moved OSPFv2 area configuration information below interface sections in Nested_Router.
  - OSPFv2 configuration was not added to NSX-T's Tier-0 Gateway within the configuration file.  If the user wants to configure OSPFv2 within NSX-T, they will have to do it manually.  There are currently no plans to add OSPFv2 configuration to the SDDC.Lab project given BGP is fully functional, supports IPv6, and is the protocol used by Federation.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml
  - After updating your non-sample configuration files, be sure to recreate your static Pod configuration files by running "CreatePodConfig.yml" against each of the updated config files.

## Dev-v4.0.0 21-AUG-2021

### Added by Luis Chanu

  - Renamed playbooks\deployNsxManager.yml to playbooks\DeployNsxLocalManager.yml to prepare for the development of Global Manager specific playbooks.
  - Updated Deploy.yml with updated DeployNsxLocalManager.yml playbook.

## Dev-v4.0.0 22-AUG-2021

### Added by Luis Chanu
  - Began development on playbooks\DeployNsxGlobalManager.yml
  - Updated the following files to support changes to Deploy.Product.NSXT.GlobalManager structure
    - templates\Pod_Config.j2
    - tempaltes\Pod_Doc.j2
  - The following file was updated so please update your non-sample file:
    - config_sample.yml
  - After updating your non-sample configuration files, be sure to recreate your static Pod configuration files by running "CreatePodConfig.yml" against each of the updated config files.

## Dev-v4.0.0 23-AUG-2021

### Added by Luis Chanu
  - Added removal of Global Manager to UnDeploy.yml playbook

  ## Dev-v4.0.0 25-AUG-2021

### Added by Luis Chanu
  - Added task to enable and activate Global Manager within DeployNsxGlobalManager.yml
  - Created "tests/ShowURI.yml" playbook
  - Began working on "registerNsxLocalWithNsxGlobal.yml" playbook
  - Updated software_sample.yml and templates_sample.yml with vCenter Server v7.0 Update 2C details

## Dev-v4.0.0 26-AUG-2021

### Added by Rutger Blom
  - Changed NSX-T version to 3.1.3
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

### Added by Luis Chanu
  - Updated registerNsxLocalWithNsxGlobal.yml, and tested against deployed labs.
  - Updated ansible-galaxy to include community.crypto, as it's needed by community.crypto.x509_certificate_info module in registerNsxLocalWithNsxGlobal.yml playbook.

## Dev-v4.0.0 27-AUG-2021

### Added by Rutger Blom
  - Added data structure to config_sample.yml for an optional "ComputeB" nested cluster
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 28-AUG-2021

### Added by Rutger Blom
  - Began work on making Tanzu configuration cluster-based. 
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 29-AUG-2021

### Added by Luis Chanu
  - Added tests/GeneratePodConfig.yml test playbook to easily generate a Pod Configuration for troubleshooting purposes.

## Dev-v4.0.0 30-AUG-2021

### Added by Luis Chanu
  - Re-organized product deployment settings within "Deploy" branch of config_sample.yml
  - Updated templates/Pod_Config.j2 to match updated Deploy section within config_sample.yml
  - Added additional fields within NSX-T "Deploy" branch
  - Added "EdgeTransit" flag to NSX-T Segments.  This flag indicates if this Segment should be used as the VLAN Transit Segment for the Edge uplinks.
  - Updated various "Deploy.Product.xxx" entries to "Deploy.Product.xxx.Deploy" throughout all files in project
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 31-AUG-2021

### Added by Rutger Blom
  - Tanzu is now configured on a per vSphere cluster basis. 
  - In this early release the user can choose to enable automatic deployment of Tanzu Supervisor Clusters (disabled by default). The default settings should be fine, but can be modified under "Nested_Clusters" for each individual vSphere cluster.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 01-SEP-2021

### Added by Rutger Blom
  - Tanzu worker nodes are now using the globally defined DNS server (Common.DNS.Server1.IPv4)
  - The following file was updated so please update your non-sample file:
    - config_sample.yml

## Dev-v4.0.0 07-SEP-2021

### Added by Rutger Blom
  - Added NSX-T 3.1.3.1 to software_sample.yml
  - The following file was updated so please update your non-sample file:
    - software_sample.yml

## Dev-v4.0.0 17-SEP-2021

### Added by Luis Chanu
  - Moved NSX-T Local Manager licensing playbook immediately after it's deployment in Deploy.yml
  - Added missing ".ova" file extension to NSX-T v3.1.3.1 entry in software_sample.yml

## Dev-v4.0.0 21-SEP-2021

### Added by Rutger Blom
  - Added a route re-distribution rule to the Tier-0 that contains TIER1_NAT and TIER1_LB_VIP
  - Added support for vCenter 7.0 U2d
  - Made vCenter 7.0 U2d the default version
  - Made NSX-T 3.1.3.1 the default version
  - The following files were updated so please update your non-sample files:
    - config_sample.yml
    - software_sample.yml

### Added by Luis Chanu
  - Created new "Backup" section under Common
  - Created new "Backup" section under Nested_NSXT, referencing the "Common" backup server
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 23-SEP-2021

### Added by Luis Chanu
  - Added Port variable to BackupServer structure
  - Updated all BackupServer references to include Port
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 24-SEP-2021

### Added by Luis Chanu
  - Added Passphrase to BackupServers structure
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 25-SEP-2021

### Added by Luis Chanu
  - Added Deploy.Product.NSXT.Federation section to indicate if NSX-T Federation should be configured.  This allows the user to deploy all of the components, then run through NSX-T Federation configuration on their own.
  - Templates/Pod_Config.j2 updated to include new Federation section within Deploy.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 28-SEP-2021

### Added by Rutger Blom
  - Added Ubuntu Server 20.04.3 to software_sample.yml
  - The following files were updated so please update your non-sample files:
    - software_sample.yml
    - templates_sample.yml

## Dev-v4.0.0 03-OCT-2021

### Added by Luis Chanu
  - Renamed playbooks/registerNsxLocalManager.yml to playbooks/FederateNsxLocalManager.yml
  - Added the following playbooks to Deploy.yml:
    - ConfigureNsxBackup.yml
    - registerNsxLocalManager.yml
      - This is still untested, so it is excluded from running.  Remove the "false" flag in order to try it.
  - Added vCenter Server "7.00U2D" entry in sample templates file.
  - The following files were updated so please update your non-sample files:
    - templates_sample.yml

## Dev-v4.0.0 05-OCT-2021

### Added by Rutger Blom
  - Added ESXi and vCenter 7.0 U3 to software_sample.yml
  - The following files were updated so please update your non-sample files:
    - software_sample.yml
    - templates_sample.yml

## Dev-v4.0.0 06-OCT-2021

### Added by Luis Chanu
  - Added conditional to UpdateDNS.yml to only populate Global Manager records in DNS if the deploying SiteCode == Global Manager SiteCode.  It should be noted that the conditional was NOT added to CleanupDNS.yml, as they should always be removed if present.
  - Originally, Deploy.Product.NSXT.GlobalManager.Deploy was used to signify if GM was being deployed.  That has now been changed, and now Deploy.Product.NSXT.Federation.Enable is used.  If it is set to True, then when the deployment SiteCode matches the GlobalManager.SiteCode, the Global Manager is deployed.
  - Modify EULA structure for Nested_NSXT
  - Added automated EULA acceptance to the NSX-T Global and Local Manager deployment playbooks.  EULA must be accepted in the config.yml file (under Nested_NSXT.Question.EULA)
  - The following file(s) were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 10-OCT-2021

### Added by Luis Chanu
  - Changes made to the ConfigureNsxBackup.yml playbook, and it appears to be functioning properly.
  - Added comments to playbook to document what backups are created, and which ones are run.
  - Additional changes to FederateNsxLocalManager.yml...still work in progress.
  - Enabled ConfigureNsxBackup.yml in Deploy.yml.

## Dev-v4.0.0 11-OCT-2021

### Added by Luis Chanu
  - Changed expected "ready" state for GlobalManager in DeployNsxGlobalManager.yml from "NONE" to "ACTIVE".
  - Increased delay before VIP in an attempt to address a race condition.
  - Modified Deploy.yml to support the following:
    - If deployment is Federated, then only provision NSX-T logical objects in the same pod that is deploying Global Manager
    - Federation deployment as been enabled, but will only execute if Federation is enabled (Federation.Enable == true)
  - Removed Deploy.Product.NSXT.Edge.UplinksToUse variable from config_sample.yml and Pod_Config.j2.
  - The following file(s) were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 13-OCT-2021

### Added by Luis Chanu
  - Added vRealize Log Insight v8.6.0 to software_sample.yml (Untested)
  - The following file(s) were updated so please update your non-sample files:
    - software_sample.yml

## Dev-v4.0.0 17-OCT-2021

### Added by Luis Chanu
  - NOTE: Successfully deployed vRealize Log Insight v8.6.0 as part of a deployment
  - Made slight modifications to FederateNsxLocalManager.yml around order of operations and delays
  - Began developing FederateNsxEdgeNodes.yml playbook to make the necessary changes to the Edge Nodes for Federation.  Initial thoughts on tasks include:
    - Connect EdgeNodes to T0-Gateway-01 interfaces
    - Assign IP addresses to the EdgeNode interfaces
    - Configure RTEP interfaces on EdgeNodes

## Dev-v4.0.0 24-OCT-2021

### Added by Rutger Blom
  - Made vCenter 7.00U3 the default version
  - Made ESXi 7.00U3 the default version
  - Made vRLI 8.6.0 the default version
  - Made DNSServer 20.04.3 the default version
  - Changed name of dicts in config_sample.yml to comply with the project's naming standard.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 26-OCT-2021

### Added by Luis Chanu
  - Added additional "Answer" variables and comments to Nested_NSXT.Question.CEIP section.  When "Answer" is set to "true", the CEIP is set accordingly.
  - Modified Global Manager EULA acceptance task to use policy API
  - Modified DeployNsxLocalManager.yml to include task to automatically answer CEIP.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 27-OCT-2021

### Added by Luis Chanu
  - In FederateNsxLocalManager.yml, doubled length of time we'll loop to see if Global Manager is ready from 1 hour to 2 hours.
  - Updated DeployNsxLocalManager.yml to obtain current _revision number for CEIP config and telemetry settings
  - To determine if Pod-Router VM is actually powered off, replaced timer with module to query VM state
  
## Dev-v4.0.0 28-OCT-2021

### Added by Luis Chanu
  - The "SEG-Example-Complicated-VLAN-Segment" segment was deleted from sample_config.yml to remove collisions during Federation onboarding. 
  - Changed few tasks in DeployNsxGlobalManager.yml to use FQDN instead of IPv4 address
  - Removed "lower" filters from DeployNsxLocalManager.yml playbook
  - Modified DeployNsxGlobalManager and DeployNsxLocalManager playbooks to use NSX-T REST API with a verification loop to configure VIPs rather than NSX-T Ansible Module
  - Modified DeployNsxLocalManager to use NSX-T LM VIP rather than appliance IP's after VIP is configured
  - Added vCenter Server v7.0 Update 3A to software repository
  - The following files were updated so please update your non-sample files:
    - config_sample.yml
    - software_sample.yml
    - templates_sample.yml

## Dev-v4.0.0 31-OCT-2021

### Added by Luis Chanu
  - Created tests/TestFailure.yml playbook to test various failure handling scenarios
  - Many changes to FederateNsxLocalManager.yml playbook:
    - Identified race condition, and modified various tasks to address it
    - Identified onboarding issue if multiple simultaneous Pods are being deployed, as only one NSX-T Location can be onboarded at a time.  Resolved by adding logic so that sites can onboard only if NSX-T is accepting onboarding, else the sites keep waiting.
  - Successfully tested NSX-T Federation deployment with three (3) sites.
  - Current Federation Limitations with this project (Solution is to do them manually):
    - Edge Node RTEP configuration is not performed (Still researching REST APIs)
    - BGP is not configured on the Stretched Tier-0 Gateway
    - Stretched Tier-0 Gateway is not streteched across sites beyond the Site where the Global Manager runs

## Dev-v4.0.0 03-NOV-2021

### Added by Luis Chanu
  - Added NSX-T v3.1.3.3 to software_sample.yml file
  - The following files were updated so please update your non-sample files:
    - software_sample.yml

## Dev-v4.0.0 08-NOV-2021

### Added by Luis Chanu
  - Added check to make sure product variables were defined in utils/createSoftwareDir.yml playbook
  - Added check for IPv4 in table header to match table data in templates/Pod_Doc.j2
  - Removed extra ":5480" from vCenter Server CLI URI's in templates/Pod_Doc.j2
  - Added "loop_control" section to disabling user password expiration setting on Local and Global manager to address a potential timeout issue
  - Corrected issue where Edge nodes were not setting 'audit' user password
  - Added Named Teaming Policies to Edge-Uplink-Profile to support pinning to ToR-A and ToR-B
  - Modfied TZ-Edge to take advantage of the new ToR-A and ToR-B named teaming policies
  - Added filter in DeployNsxLocalManager.yml and DeployNsxGlobalManager.yml to force 'Deployment Size' to lower as a safety net in case user accidentally changes case.  OVFTool requires Size to be in lower case.
  - Added 'upper' filter in templates/vars_NSXT_EdgeTransportNodes.j2 to ensure FormFactor sizing is always in upper case, as required by the NSX-T API.
  - Modified CreateNsxEdgeTn.yml to disable password expiration for all users on NSX-T Edges
  - Modified DeployNsxLocalManager.yml and DeployNsxGlobalManager.yml to also disable password expiration for 'root' user
  - Updated software versions in config_sample.yml for NSX-T and vCenter Server to v3.1.3.3 and v7.00U3a, respectively.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 11-NOV-2021

### Added by Luis Chanu
  - Modified VLAN Segments in config_sample.yml to use 3-Digit VLAN IDs so segments sort properly in GUI when Federated
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 13-NOV-2021

### Added by Rutger Blom
  - Added vCenter Server v7.0 Update 3B to software repository
  - Added ESXi v7.0 Update 3B to software repository
  - The following files were updated so please update your non-sample files:
    - config_sample.yml
    - software_sample.yml
    - templates_sample.yml

## Dev-v4.0.0 14-NOV-2021

### Added by Luis Chanu
  - Updated all instances of "validate_certs" to get their effective value from Common.PKI.ValidateCerts
  - Cleaned up dict Lists in Nested_NSXT EdgeClusters and Edge Nodes datastructures to use basic Lists in config_sample.yml.
  - Removed extra "ip_addresses:" entry on line 47 from var_NSXT_EdgeTransportNodes.j2 that appeared to have been left in by accident, and had no function.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 21-NOV-2021

### Added by Luis Chanu
  - Added code to FederateNsxEdgeNodes.yml which:
    - Configures RTEP interface on Edge Nodes
    - Configures Tier-0 Gateway Interfaces on the Edge Node SRs
    - **IMPORTANT**: Only the first Tier-0 Gateway is configured
    - VERY limited testing performed
  - Added RTEP configuration details to Nested_NSXT.System.LocationManager in config_sample.yml
  - InterLocationMTU not yet implemented in RTEP section
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 22-NOV-2021

### Added by Luis Chanu
  - Added NSX-T Federation section to README.md file
  - Modified .gitignore to ignore all files that start with:
    - config*
    - license*
    - licenses*
  - Modified .gitignore to ensure the following sample files are still included in git:
    - config_sample.yml
    - templates_sample.yml
    - software_sample.yml
    - licenses_sample.yml
  - Removed Nested_NSXT.System.LocationManager  from config_sample.yml
  - Added Nested_NSXT.System.Fabric.GlocalSetting to config_sample.yml
  - Added playbooks/ConfigureNsxFabricMTU.yml to project
  - Added ConfigureNsxFabricMTU.yml to Deploy.yml
  - NSX-T Global Fabric MTU settings are now configured to match the values defined in Net.Transport.MTU and Net.RTEP.MTU.  Make sure these values supported by your physical networking environment.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 23-NOV-2021

### Added by Luis Chanu
  - Added BGP Neighbor description to vars_NSXT_T0Gateways.j2 template.
  - Added FederateNsxT0BGPNeighbors.yml playbook to project, which configures BGP Neighbors to the stretched Tier-0 Gateway.
  - Added FederateNsxT0RouteReDist.yml playbook to project.  This handles configuration of Tier-0 Gateway Route Re-Distribution on non-GM SiteCodes.
  - Added FederateNsxT0RouteReDist.yml playbook to Deploy.yml.
  - Corredted issue with T0Edges variable.
  - Increased time on some loops to support large deployments.
  - In config_sample.yml, changed Tier-0 Gateway Locale-Service from "T0-Gateway-01_Locale_Service" to "{{ SiteCode }}" to aid with Federation automation.
  - Added FederateNsxT0BGPNeighbors.yml to Deploy.yml
  - Removed 'EdgeTransit' field from all NSX-T Segments in the config_sample.yml file as it is not used.
  - Renamed 'SEG-Example-Overlay-Without-VLANS' segment to 'SEG-Example-Tier0-Overlay-Segment' to better describe its existance/purpose.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 24-NOV-2021

### Added by Luis Chanu
  - Where applicable, playbooks were updated to use Local Manager and Global Manager VIPs instead of direct appliance IP
  - Added task to end of ValidateConfiguration.yml playbook to recursively delete /tmp/{{ SiteCode }} directory

## Dev-v4.0.0 26-NOV-2021

### Added by Luis Chanu
  - Updated 'CreateContentLibrary.yml' file implemented which supports additional functionality, including the ability to subscribe to remotely publised content libraries.
  - Updated config_sample.yml configuration file with additional Content Library variables to support the additional functionality
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 21-DEC-2021

### Added by Luis Chanu
  - As the sample_config.yml file has changed over time, the amount of time it takes for CreatePodConfig.yml to complete is increasing.  Latest testing shows it's now taking just over 2 hours to complete.  You can run multiple in parallel without issue.  We are looking into this, but for now, that's how long to expect.
  - Updated verbiage in CreatePodConfig.yml on how long it takes to create the static Pod-XXX-Config.yml file.
  - Added Deploy.Product.NSXT.GlobalManager.PodNumber variable to support Federation, as a stretched Tier-0 uses the same ASN across all sites.
  - Added the following updated products to software_sample.yml:
    - NSX-T v3.2.0 (Untested)
    - vRealize Log Insight v6.4.1 (Untested)
  - The following files were updated so please update your non-sample files:
    - config_sample.yml
    - software_sample.yml

## Dev-v4.0.0 23-DEC-2021

### Added by Luis Chanu
  - Modified CreatePodConfig.yml to include additional fields in created static Pod Config filename.  Those fields are:
    - VCSA version (VCSAvXXXXX) where XXXXX is VCSA version
    - NSXT version (NSXTvYYYYY) where YYYYY is NSX-T version
    - Fed-Z where Z is either Y or N, and indicates whether the Pod Configuration has NSX-T Federation deployment enabled or not

## Dev-v4.0.0 24-DEC-2021

### Added by Luis Chanu
  - **IMPORTANT**: As part of NSX-T Federation, NSX-T v3.2.0 appears to not support importing objects from a Location into the Global Manager.  For this reason, SDDC.Lab can not be used to deploy Federation when deploying NSX-T v3.2.0, as SDDC.Lab utilizes this functionality.  The workaround to this is to deploy Federation using NSX-T v3.1.3.3, then manually upgrade the Pods to v3.2.0.  It's assumed that this functionality will be re-introduced in a later release.  Standalone (i.e. Non-Federated) deployments of NSX-T v3.2.0 has been tested, and works fine.
  - NSX-T v3.2.0 Federation details added to README.md file
  - NSX-T v3.2.0 takes MUCH longer to set the "password_change_frequency" on an Edge Transport Node users than it did under NSX-T v3.1.3.3.  For this reason, the timeout on the task that performs this operation within "CreateNsxEdgeTn.yml" playbook has been increased from 15 to 60 seconds.
  - NSX-T Version Tested Status:
    - v3.1.3.3: Standalone and Federation
    - v3.1.3.5: We are still looking into an issue when deploying against this version.  Until further testing has been done, please do not deploy directly to this version...use v3.1.3.3 instead, then manually upgrade to v3.1.3.5.
    - v3.2.0:   Standalone only (See 'IMPORTANT' comment above)
  - Manually edited Ansible module "nsxt_fabric_compute_managers.py" to incorporate a change that was made in the VMware NSX-T Ansible modules to support Compute Manager registartion under NSX-T v3.2.0.
  - The "var_NSXT_EdgeTransportNodes.j2" template has been updated to support v3.2.0.  These changes have also been tested against v3.1.3.3, and deployed fine.
  - Modified "CreatePodConfig.yml" to append the Global Manager Pod to the end of the filename if Federation is enabled.
  - The following playbooks have been modified to support NSX-T v3.2.0:
    - CreateNsxEdgeTn.yml
    - CreateNsxTz.yml

## Dev-v4.0.0 25-DEC-2021

### Added by Luis Chanu
  - Increased retry count on vSphere Replication partner in checkVcReplicaionPartner.yml from 30 to 45.  This is to ensure very large deployments don't timeout during deployment.  Have not run into any issues, just a preventative measure.
  - The following deployment scenarios completed successfully:
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.1.3.3 (2-Site Federation)
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.1.3.5 (Standalone)
  - The following deployment scenarios **FAILED**:
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.2.0   (Standalone) -- Issue with EdgeVM state changes when password aging is cleared (Flaps from SUCCESS to IN_PROGRESS), then Edge Cluster creation fails.

## Dev-v4.0.0 26-DEC-2021

### Added by Luis Chanu
  - Modified CreateNsxEdgeCluster.yml play to address the flapping of EdgeVM state when the user password aging is disabled.
  - The following deployment scenarios completed successfully:
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.1.3.3 (2-Site Federation)
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.1.3.5 (Standalone)
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.2.0   (Standalone)

## Dev-v4.0.0 27-DEC-2021

### Added by Luis Chanu
  - Created utils/util_ApplyConfigToTemplate.yml playbook to be able to test any template quickly.  Modify the variable within to indicate what template you want to have it generate.
  - Began working on CreateNsxDhcpProfiles.yml playbook to create DHCP Server and DHCP Relay profiles.
  - Added Nested_NSXT.Networking.DHCPProfiles section to config_sample.yml.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 28-DEC-2021

### Added by Luis Chanu
  - Following changes were made to CreateNsxEdgeTn.yml playbook:
    - The nested loop to set password aging to 0 was reversed so that each of the EdgeVMs are cycled through for each user.  This permits the EdgeVM to "recover" to the "SUCCESS" state before the next REST API call is attempted to it.
    - Added an additional check at the end of the playbook to verify all EdgeVMs are in a "SUCCESS" state before the playbook is completed.  This hopefully ensures all EdgeVMs are ready for other REST API calls.

## Dev-v4.0.0 29-DEC-2021

### Added by Luis Chanu
  - The SDDC.Lab project was migrated from older local Ansible NSX-T modules to [VMware Ansible modules for NSX-T v3.2.0](https://github.com/vmware/ansible-for-nsxt/tree/v3.2.0).  In order to migrate your installation, follow these steps:
    - Install VMware Ansible for NSX-T Modules (run BOTH commands):
      - ansible-galaxy collection install git+https://github.com/vmware/ansible-for-nsxt.git,v3.2.0
      - sudo ansible-galaxy collection install git+https://github.com/vmware/ansible-for-nsxt.git,v3.2.0
    - If they exist, comment the following two lines from the ansible.cfg file located at the root of the SDDC.Lab project directory by putting "#" in front of each line:
      - library = library
      - module_utils = module_utils
    - Within the "library" directory, delete all files that begin with "nsxt_" except for the ones listed below.  The following files should remain:
      - __Module_Info (This file has been updated, so obtain the updated file from the project)
      - claim_vsan_disks.py
      - enable_vsan.py
      - set_drive_type.py
      - nsxt_gobal_manager_active.py
      - nsxt_gobal_manager_enable_service.py
      - nsxt_gobal_manager_registration.py
      - nsxt_local_manager_registration.py
      - nsxt_local_managers_compatibility.py

## Dev-v4.0.0 30-DEC-2021

### Added by Luis Chanu
  - Updated README.md and FirstPod.md files
  - Within the various playbooks, with the exception of Global Manager modules, all NSX-T module references have been updated to use FQCN naming.  Global Manager modules are still located in the local "library" directory, which is why they were not changed to use FQCN.
  - Added "include_var_DHCPProfilePath.yml" playbook to centrally generate the DHCProfilePath dictionary variable.
  - To assist with test workload VMs, a DHCP Local Server was added to each Overlay segment.  Both IPv4 and IPv6 was configured.
  - Added Common.DHCP section to config_sample.yml
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 01-JANUARY-2022

### Added by Luis Chanu
  - Created "DeployWorkloadVms.yml" playbook to deploy Workload VM Templates (VM or OVF) from the Content Library after Pod deployment
  - Created "include_tasks_deployWorkloadVm.yml" file with plays that does the "heavy lifting" of the VM deployment.
  - Added additional sections to config_sample.yml file, includng:
    - Deploy.WorkloadVMs section enable WorkloadVMs functionality and provide default settings for Cluster and VMFolder placement of VMs.  These default settings can be over-written at a VM level.
    - WorkloadVMs section at the end of the file where the various VM/OVF Template workloads that are to be deployed are defined.  Users will need to modify this section to meet their needs.
  - Added Deploy and WorkloadVMs to Pod_Config.j2 template
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 05-JANUARY-2022

### Added by Luis Chanu
  - Added markdown code blocks "back-ticks" around header of both README.md and FirstPod.md files.
  - Added "Issues With Various Software Versions" section to README.md file.

## Dev-v4.0.0 06-JANUARY-2022

### Added by Luis Chanu
  - Modify CreateNsxEdgeCluster.yml and vars_NSXT_EdgeClusters.j2 to permit creation of Edge Clusters without any member Edge Nodes.

## Dev-v4.0.0 11-JANUARY-2022

### Added by Luis Chanu
  - Added UplinkTeamingPolicy to Nested_NSXT.Networking.Segments data structure in config_sample.yml
  - Modified CreateNsxVLANSegments.yml to now apply Uplink Teaming Policy to VLAN Segments.  If UplinkTeamingPolicy is set to "" or not defined, it will default to using the Default teaming policy.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 11-JANUARY-2022

### Added by Luis Chanu
  - Corrected issue with test code that was accidentally left in a playbook.  Test code has been removed.

## Dev-v4.0.0 13-JANUARY-2022

### Added by Luis Chanu
  - Corrected issue with DHCP Server causing Federation deployment to fail as it's not supported by Federation.  Added logic to not implement DHCP Server when Federation is being deployed.
  - Verified NSX-T Federation deployment completed successfully using NSX-T v3.1.3.5.

## Dev-v4.0.0 15-JANUARY-2022

### Added by Luis Chanu
  - Changed font/type used for commands and filenames in README.md file
  - Included information about the vBrownBag video created for VMworld 2021 that goes over the project

## Dev-v4.0.0 23-JANUARY-2022

### Added by Rutger Blom
  - Updated README.md "Preparations" section so it includes the "testresources" and "cryptography" python packages.

## Dev-v4.0.0 23-JANUARY-2022

### Added by Rutger Blom
  - Added NSX-T collection to requirements.yml
  - Updated PreparePhysical.yml to remove deprecated and add required parameters to community.vmware.vmware_dvs_portgroup tasks

## Dev-v4.0.0 24-JANUARY-2022

### Added by Rutger Blom
  - vRLI 8.6.2 (not tested)

## Dev-v4.0.0 25-JANUARY-2022

### Added by Luis Chanu
  - Updated README.md file
  - Added NSX-T v3.2.0.1 to ```software_sample.yml``` file (Untested)

## Dev-v4.0.0 28-JANUARY-2022

### Added by Luis Chanu
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` to support the following software updates:
    - vCenter Server v7.0 Update 3c
    - ESXi v7.0 Update 3c
  - Please be sure to update your ```software.yml``` and ```templates.yml``` files
  - SDDC.Lab was NOT tested against these new software updates

## Dev-v4.0.0 30-JANUARY-2022

### Added by Luis Chanu
  - Updated VyOS URL repository in ```software_sample.yml``` from [https://downloads.vyos.io/rolling/current/amd64](https://downloads.vyos.io/rolling/current/amd64) to [https://s3.amazonaws.com/s3-us.vyos.io/rolling/current](https://s3.amazonaws.com/s3-us.vyos.io/rolling/current)
  - Please be sure to update your ```software.yml``` file
  - Added section headers to ```config_sample.yml``` file to aid in finding sections while using Visual Studio Code (VSC) IDE.  No functional changes made, just added headers.
  - Removed temporary ```config_sample_WithSections.yml``` file
  - Modified ```templates/vyos_router.j2``` file to:
    - address change in DHCP option for DNS Server.  "dns-server" changed to "name-server"
    - address change in OSPFv3 argument order for associating an area to an interface
  - Added comments about potenial issues we may run into using the VyOS Nightly Build ISO image.

## Dev-v4.0.0 31-JANUARY-2022

### Added by Luis Chanu
  - Increased memory from 18GB to 20GB on all Nested_ESXi clusters to address Host Preparation "Memory Error" failures with NSX-T v3.2.0.1.
  - Updated README.md file with Federation support on NSX-T v3.2.0.1.

## Dev-v4.0.0 5-FEBRUARY-2022

### Added by Luis Chanu
  - Moved ansible-galaxy installation of VMware NSX-T modules from ```requirements.yml``` file to the README document.  This was done because the installation of the NSX-T modules needs to be performed using ```sudo``` to ensure the modules are installed in the appropriate location as the ansible playbooks are run using ```sudo```.
  - Modified ansible-galaxy installation line to install supported v3.2.0 of the modules, rather than the latest versions from the development branch.
  - Added additional comments in README.

## Dev-v4.0.0 6-FEBRUARY-2022

### Added by Luis Chanu
  - Added the following software entries in ```software_sample.yml``` and ```templates_sample.yml```:
    - vCenter Server v6.7 Update 3p
    - NSX-T v3.0.3.1
    - NSX-T v3.1.3.6
  - Please be sure to update your ```software.yml``` and ```templates.yml``` files
  - SDDC.Lab was **NOT** tested against these new software updates
  - Renamed VMFolder for vCenter Server target deployments from "SDDC Labs" to "SDDC Pods" in ```config_sample.yml```.
  - Please be sure to update your configuration files and rename your VM Folder from "SDDC Labs" to "SDDC Pods" within your target vCenter Server.
  - In ValidateConfiguration.yml, changed DIG target from ```www.google.com``` to ```github.com``` because it was oberved that ipaddr returns ```False``` when multiple A records are returned.
  - Change permissions set within ```Util_CreateSoftwareDir.yml``` from 775 to 777 to ensure non-root user can update the software repsoritory.
  - Modified ```Util_CreateSoftwareDir.yml``` to set 777 permissions to top-level RootDirectory (/Software) directory as well.
  - Enabled ```deployWorkloadVMs.yml``` task in ```Deploy.yml```.

## Dev-v4.0.0 20-FEBRUARY-2022

### Added by Luis Chanu
  - Added Tranpsort MTU to NSX-T Uplink Profile creation.
  - Modified ```config_sample.yml``` to configure MTU value on UplinkProfiles dynamically, to the MTU that is set on the Transport (TEP) segment.
  - Modified ```config_sample.yml```, playbooks, and templates, to allow Host Uplink Profile MTU to be empty, which is required for VDS v7 support.
  - Removed MTU value from ```ESXi-Uplink-Profile``` within ```config_sample.yml``` file.
  - As ```config_sample.yml``` was modified, please update your config files accordingly.

## Dev-v4.0.0 9-MARCH-2022

### Added by Luis Chanu
  - Changed DHCP lease time in ```config_sample.yml``` from 1 day (86400 seconds) to 1 hour (3600 seconds)
  - As ```config_sample.yml``` was modified, please update your config files accordingly.

## Dev-v4.0.0 10-MARCH-2022

### Added by Luis Chanu
  - Changed test VM workload to use from [yVM](https://cloudarchitectblog.wordpress.com/2015/11/11/how-to-build-your-own-yvm-step-by-step-process/) to [TinyVM](https://github.com/luischanu/TinyVM) within the WorkloadVMs section of ```config_sample.yml```
  - To leverage [TinyVM](https://github.com/luischanu/TinyVM), but sure to add it to ```SDDC.Lab Content Library``` on the physical vCenter Server, then sync the VM Template to your SDDC.Lab Pods.
  - Corrected Table of Content entries to work correctly in ```README.md``` file.
  - Added instructions to ```README.md``` regarding [TinyVM](https://github.com/luischanu/TinyVM) and how to enable the deployment of Test Workload VMs.
  - As ```config_sample.yml``` was modified, please update your config files accordingly.

## Dev-v4.0.0 11-MARCH-2022

### Added by Luis Chanu
  - Corrected issue with DHCP Lease Time in ```config_sample.yml```.
  - As ```config_sample.yml``` was modified, please update your config files accordingly.

## Dev-v4.0.0 13-MARCH-2022

### Added by Rutger Blom
  - Moved configuring NTP on nested ESXi hosts from kickstart file to an Ansible task in "ConfigureNestedEsxi.yml". 

## Dev-v4.0.0 25-MARCH-2022

### Added by Luis Chanu
  - Added an additional NSX-T Tag to all ```TinyVM``` WorkloadVMs

## Dev-v4.0.0 1-APRIL-2022

### Added by Luis Chanu
  - Added vCenter Server and ESXi versions 7.0U3D to software repository
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` files.


<br>

***
<h1 style="text-align:center">SDDC.Lab Version 4.0 Released</h1>
<br>


## Release-v4.0.0 6-APRIL-2022

### Added by Rutger Blom & Luis Chanu

- Released version 4 of the SDDC.Lab project.

```
██████  ███████ ██    ██       ██    ██ ███████
██   ██ ██      ██    ██       ██    ██ ██
██   ██ █████   ██    ██ █████ ██    ██ ███████
██   ██ ██       ██  ██         ██  ██       ██
██████  ███████   ████           ████   ███████
```

## Dev-v5.0.0 6-APRIL-2022

### Added by Luis Chanu
  - Begin developing version 5.0 in branch ```dev-v5```

## Dev-v5.0.0 10-APRIL-2022

### Added by Rutger Blom
  - Fixed an issue with the port groups not being removed when running "UnDeploy.yml".

## Dev-v5.0.0 10-APRIL-2022

### Added by Luis Chanu
  - Added ```log_path``` parameter to ansible.cfg file to save Ansible playbook deployment output to a file, which is useful for debugging.  As we deploy using sudo, we must use this approach instead of the ```ANSIBLE_LOG_PATH``` environment variable.  Once we remove the use of sudo, we should be able to use the environment variable.  This option is commented out, and needs to be enabled on an as-needed basis.

## Dev-v5.0.0 11-APRIL-2022

### Added by Rutger Blom
  - Added the following software entries in ```software_sample.yml``` and ```templates_sample.yml```:
    - Ubuntu Server v20.04.4
  - Please be sure to update your ```software.yml``` and ```templates.yml``` files

## Dev-v5.0.0 12-APRIL-2022

### Added by Rutger Blom
  - Added the active uplinks teaming policy parameter to vmware_dvs_portgroups tasks in ```CreateVds.yml```. Active uplink configuration is stored in the Nested_vCenter dictionary in ```config_sample.yml```.
  - Modified the active uplinks of port groups NSXEdgeUplink1 and NSXEdgeUplink2 in ```config_sample.yml``` so that these use only Uplink 1 and Uplink 2 respectively. This to support pinning to ToR-A and ToR-B.
  - Changed the following in ```config_sample.yml```:
    - vCenter version 7.00U3D
    - ESXi version 7.00U3D
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 13-APRIL-2022

### Added by Rutger Blom
  - Changed the following in ```config_sample.yml```:
    - vRLI version 8.6.2
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 13-APRIL-2022

### Added by Luis Chanu
  - Changed /Software directory permissions from 0777 to 0775 in ```Util_CreateSoftwareDir.yml```
  - Changed NSX-T version to v3.1.3.6 in ```config_sample.yml```
  - Cleaning up minor spacing issues in ```config_sample.yml```
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 14-APRIL-2022

### Added by Rutger Blom
  - Added the standby uplinks teaming policy parameter to vmware_dvs_portgroups task in ```CreateVds.yml```. Standby uplink configuration is stored in the Nested_vCenter dictionary in ```config_sample.yml```.
  - Modified the standby uplinks of port groups NSXEdgeUplink1 and NSXEdgeUplink2 in ```config_sample.yml``` so that these use only Uplink 2 and Uplink 1 respectively. This to facilitate failover of Geneve traffic in case of a ToR failure. Although this failure scenario is not likely in a nested lab, we want to mirror configuration of a production environment whereever we can. 
  - Updated ```CreateVds.yml``` to loop over the port groups rather than having one task for each port group object.
  - Added network policy parameters (forged_transmits, mac_changes, promiscuous) to the vmware_dvs_portgroups task in ```CreateVds.yml```. Network policy configuration is stored in the Nested_vCenter dictionary in ```config_sample.yml```.
  - The parameters num_ports and port_binding used by the vmware_dvs_portgroups task in ```CreateVds.yml``` now fetch their values from the Nested_vCenter dictionary in ```config_sample.yml``` (instead of having them hard-coded in the Playbook).
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 21-APRIL-2022

### Added by Rutger Blom
  - Replaced the ```ansible.posix.mount``` task in the ```playbooks/PrepareISOInstaller.yml``` playbook with a ```ansible.builtin.command```task running ```7z``` to extract the contents of the ESXi ISO file. The ```ansible.posix.mount``` task requires root or CAP_SYS_ADMIN privileges which is something we want to eliminate in the upcoming version.
  - Added a new variable to the ```TargetConfig``` dictionary in ```config_sample.yml``` called ```ISOExtract``` which is used by the ```playbooks/PrepareISOInstaller.yml``` playbook
  - The 7Zip software package is now required so updated the ```README.md``` with this requirement. 
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 22-APRIL-2022

### Added by Rutger Blom
  - Added variable ```WorkingFolder``` to the ```TargetConfig``` dictionary in ```config_sample.yml```. The location of ```WorkingFolder``` is used for temporary files created during the Pod deployment process. The variable's default value is ```"{{ lookup('env','HOME') }}/SDDC.Lab/{{ SiteCode }}"```. Eventually ```WorkingFolder``` will replace or be renamed to variable ```TempFolder```. This will be done once all playbooks have been updated to make use of the new location.
  - Updated playbook ```playbooks/PrepareISOInstaller.yml``` to use the new ```WorkingFolder``` variable.
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 23-APRIL-2022

### Added by Rutger Blom
  - Replaced the ```ansible.posix.mount``` task in the ```playbooks/DeployDNSServer.yml``` playbook with a ```ansible.builtin.command```task running ```7z``` to extract the contents of the Ubuntu ISO file. The ```ansible.posix.mount``` task requires root or CAP_SYS_ADMIN privileges which is something we want to eliminate in the upcoming version.
  - Updated playbook ```playbooks/DeployDNSServer.yml``` and the associated template files to use the new ```WorkingFolder``` variable.
  - Added a task to ```playbooks/DeployDNSServer.yml``` that conditionaly (```DEBUG.KeepInstallerFiles != true```) deletes the local ISOExtractPoint directory
  - Added a task to ```playbooks/PrepareISOInstaller.yml``` that conditionaly (```DEBUG.KeepInstallerFiles != true```) deletes the local ISOExtractPoint directory

## Dev-v5.0.0 24-APRIL-2022

### Added by Rutger Blom
  - Replaced the ```ansible.posix.mount``` task in the ```playbooks/DeployVc.yml``` playbook with a ```ansible.builtin.command```task running ```7z``` to extract the contents of the vCenter ISO file. The ```ansible.posix.mount``` task requires root or CAP_SYS_ADMIN privileges which is something we want to eliminate in the upcoming version.
  - A non-critical error occurs when 7z extracts vCenter ISO files so added the ```ìgnore_errors: true```parameter to the task.
  - Updated playbook ```playbooks/DeployVc.yml``` to use the new ```WorkingFolder``` variable.
  - Added a task to ```playbooks/DeployVc.yml``` that conditionaly (```DEBUG.KeepInstallerFiles != true```) deletes the local ISOExtractPoint directory.

## Dev-v5.0.0 24-APRIL-2022

### Added by Rutger Blom
  - Updated variable ```TempFolder``` with new value in ```config_sample.yml``` as it replaces variable ```WorkingFolder```.
  - Removed variable ```ISOMount``` from ```config_sample.yml``` as it is not used anymore.
  - Removed variable ```WorkingFolder``` as it is not used anymore.
  - Updated documentation as well as comments in playbooks as Pod deployments can now be performed without using ```sudo``` e.g. ```ansible-playbook -e "@~/Pod-XXX-Config.yml" Deploy.yml```.
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 29-APRIL-2022

### Added by Luis Chanu
  - The following changes are still **UNTESTED**
  - Updated IP Address Assignment table in ```README.md``` file.
    - Moved all vSphere clusters to be between .101 and .199
    - Move vRLI from .6 to .19
    - Renamed vRLI to vRLI-1
    - Moved vRNI entries to .22 and .23
    - Added IP space for vRLI cluster deployment
    - Moved Tanzu IP's to start at .201
    - Added IP space Tanzu Supervisor Control Plane on numerous clusters
    - Added IP space for additional NSX-T EdgeVMs
    - Added IP space for AVI Load Balancer
  - Removed CloudServicesManager from ```config_sample.yml``` and ```templates/Pod_Config.j2```.
  - Updated IP addresses in ```config_sample.yml``` file.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 1-MAY-2022

### Added by Rutger Blom
  - Added NSX-T 3.1.3.7 to ```software_sample.yml```.
  - Please be sure to update your ```software.yml``` file.

## Dev-v5.0.0 8-MAY-2022

### Added by Luis Chanu
  - Added vRLI 8.8.0 to ```software_sample.yml```.
  - Please be sure to update your ```software.yml``` file.
  - Updated vRLI deployment to use v8.8.0 in ```config_sample.yml``` file.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 9-MAY-2022

### Added by Luis Chanu
  - Updated NSX-T deployment to use v3.1.3.7 in ```config_sample.yml``` file. (TESTED)
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 10-MAY-2022

### Added by Luis Chanu
  - Added "Ignore Fatal Error Message" to "Extract vCenter ISO" task in ```playbooks/DeployVc.yml``` playbook.
  - Added vRLI VIP entry in the "IP Address Assignments" table
  - Modified (a) vRLI IP for vRLI-1 and (b) syslog server entry in ```config_sample.yml```
  - Please be sure to update your ```config.yml``` file(s).
  - Changed default permissions for /Software directory structure from 0775 to 0777 to address issue when downloading software directly on ansible host.

## Dev-v5.0.0 24-MAY-2022

### Added by Luis Chanu
  - Updated FirstPod.md banner from v4 to v5
  - Added vCenter Server v7.0.0 Update 3E ```software_sample.yml``` and ```templates_sample.yml``` files.
  - Added NSX-T v3.2.1 to ```software_sample.yml``` file.
  - Above mentioned software versions are UNTESTED.
  - Please be sure to update your ```software.yml``` and ```templates.yml``` files.

## Dev-v5.0.0 16-JUNE-2022

### Added by Rutger Blom
  - Removed the "num_ports" parameter from "community.vmware.vmware_dvs_portgroup" tasks in ```playbooks/PreparePhysical.yml```. This to prevent an error when re-running a failed/broken off deployment and "num_ports" on the distributed port group has increased beyond specified by "num_ports" (we cannot decrease num_ports if ports are in use).

## Dev-v5.0.0 26-JULY-2022

### Added by Luis Chanu
  - All newly added software versions listed below is UNTESTED
  - Added vCenter Server v7.0.0 Update 3F & 3G to ```software_sample.yml``` and ```templates_sample.yml``` files.
  - Added ESXi v7.0.0 Update 3F to ```software_sample.yml``` and ```templates_sample.yml``` files.
  - Added NSX-T v3.2.1.1 to ```software_sample.yml``` file.

## Dev-v5.0.0 29-JULY-2022

### Added by Luis Chanu
  - In Ansible module ```EnableWorkloadManagement.yml```, noticed that the data structure used to enable Workload Managmenet (a.k.a. Tanzu) had extra escapes in it.  After investigating, appeared to be cause by extra JSON conversion in module.
  - Removed extra "| to_json" in last play in the ```EnableWorkloadManagement.yml``` module.
  - Added additional DEBUG play to display data structure when debugging is enabled.
  - Removed extra space from ContentLibrary section of ```config_sample.yml``` file.

## Dev-v5.0.0 31-JULY-2022

### Added by Luis Chanu
  - Removed extra spaces from Nested_Cluster section of ```config_sample.yml``` file.
  - Noticed an issue where if more than 1 vSphere Cluster was configured to be prepared by NSX, only one vSphere cluster would end up being prepared.  Corrected the issue by making the transport node collection display name be unique for each cluster by including the cluster name in the TNC display name field within ```attchNsxTnp.yml```.
  - Added "ignore_errors: true" to Port-Group removal plays in ```UnDeploy.yml``` file.

## Dev-v5.0.0 02-AUGUST-2022

### Added by Rutger Blom
  - Added NSX-T v4.0.0.1 to ```software_sample.yml``` file.

## Dev-v5.0.0 03-AUGUST-2022

### Added by Rutger Blom
  - Changed default version of vCenter to 7.00U3G in ```config_sample.yml``` file.
  - Changed default version of ESXi to 7.00U3F in ```config_sample.yml``` file.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 03-AUGUST-2022

### Added by Luis Chanu
  - Modified NSXT version in ```licenses_sample.yml``` to include version 4 by changing RegEx from '[23]' to '[234]'
  - Please be sure to update your ```licenses.yml``` file.
  - NSX v4.0.0.1 successfully deployed.

## Dev-v5.0.0 04-AUGUST-2022

### Added by Rutger Blom
  - Updated the "community.vmware.vmware_guest" task in the ```playbooks/DeployNestedEsxi.yml``` playbook. It now adds the advanced setting "featMask.vm.cpuid.pdpe1gb:Val1" to the nested ESXi virtual machines. This setting enables hosting VMs that require 1 GB page support (PDPE1GB). NSX-T Edge VMs require 1 GB page support since NSX-T version 3.2.

## Dev-v5.0.0 08-AUGUST-2022

### Added by Luis Chanu
  - Added the ability to create multiple Content Libraries as part of a Pod deployment. (Initial tests are successful, but more testing is needed)
  - To aid with pre-populating TKG Content Library, added support to subscribe to Content Libraries via URLs.
  - Added additional libraries, including the the default TKG Content Library.  Because of it's size, this library is configured as an "On-Demand" library, which of course can be changed in the config.
  - New content libraries can be found in the ```config_sample.yml``` file, in the ```Nested_vCenter.ContentLibraries``` section.
  - New ansible playbook added to project: ```include_tasks_CreateContentLibrary.yml```
  - Moved individual content library creation to ```include_tasks_CreateContentLibrary.yml```.  The existing ```CreateContentLibrary.yml``` playbook now dispatches the creation of each content library to the ```include_tasks_CreateContentLibrary.yml``` playbook, one-by-one.
  - WorkloadVMs playbooks modified to support new content library structure.
  - Changes made to ```config_sample.yml``` does increase the time it takes for ```playbooks/CreatePodConfig.yml``` to generate the static Pod configuration, so please be patient.  You may want to consider running the ```utils/utils_CreateAllPodConfigs.sh``` script, which will generate the static Pod Configuration files for ALL of your configurations.  Please see description in the documentation included in the header of the script file for more details about the utility.
  - There were changes in ```config_sample.yml``` file.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 09-AUGUST-2022

### Added by Luis Chanu
  - Renamed ```Nested_vCenter.ContentLibraries``` structure to ```Nested_vCenter.ContentLibrary``` in all project files, to follow existing project naming conventions.
  - There were changes in ```config_sample.yml``` file.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 14-AUGUST-2022

### Added by Luis Chanu
  - Updated ```README.md``` file with information about the NSX v4.0.0.1 Federation onboarding bug.
  - Added vRLI v8.8.2 to ```software_sample.yml``` file (UNTESTED).
  - Please be sure to update your ```software.yml``` file.

## Dev-v5.0.0 17-AUGUST-2022

### Added by Luis Chanu
  - As part of the ongoing effort to stop running playbooks using "sudo ansible-playbook", ```utils/Util_CreateSoftwareDir.yml``` was modified to use the ```become``` directive to elevate permissions within the playbook.
  - The ```README.md``` file has been updated to reflect the changes made to the ```utils/Util_CreateSoftwareDir.yml``` playbook.

## Dev-v5.0.0 17-AUGUST-2022

### Added by Rutger Blom
  - The required Python modules are now listed in the ```pip3_requirements.txt``` file. This file can be used when running pip (Package Installer for Python).
  - Updated the "pip3" preparation step in ```README.md``` and ```FirstPod.md``` so that making use of the new ```pip3_requirements.txt``` file is suggested.

## Dev-v5.0.0 18-AUGUST-2022

### Added by Luis Chanu
  - Updated ```utils/util_CreateSwitchConfig.yml``` playbook to use the live VyOS Router Jinja2 template that is used during the deployment.  A more detailed desription was also added inside of the script.
  - As the actual template is now used, the temporary template within utils was deleted.

## Dev-v5.0.0 19-AUGUST-2022

### Added by Luis Chanu
  - Command syntax change found with VyOS "nightly" release.  When configuring bgp, 'local-as' has been changed to 'system-as'.
  - Corrected bgp command in ```templates/vyos_router.j2``` file to support current "nightly" VyOS release ISO.
  - You must delete (yes, delete) your VyOS ISO file, located here: ```/Software/VyOS/Router/Latest/vyos-rolling-latest.iso```.  By default, SDDC.Lab will download the latest VyOS ISO nightly build ISO if the file is not found in ```/Software/VyOS/Router/Latest```.
  - Removed ```Deploy.Software.Router.Version == "Latest"``` conditions from ```playbooks/DeployRouter.yml``` playbook.
  - Added vRLI version 8.8.2 to ```software_sample.yml```.
  - Added VyOS version "Test" to ```software_sample.yml```, which is used for internal testing.  You should continue to use "Latest" in your builds.
  - Update your ```software.yml``` file.

## Dev-v5.0.0 30-AUGUST-2022

### Added by Rutger Blom
  - Updated the Ubuntu Server download URL for some older versions in ```software_sample.yml```.
  - Please be sure to update your ```software.yml``` file.

## Dev-v5.0.0 31-AUGUST-2022

### Added by Rutger Blom
  - Added a Ubuntu Server 22.04.1 entry to ```software_sample.yml``` as well as Ubuntu Server 22.04.1 template files to the ```./templates``` directory. Please note that support for Ubuntu Server version 22.04.1 is not yet implemented. Do not specify version 22.04.1 in your configuration at this time! 
  - Please be sure to update your ```software.yml``` file.

## Dev-v5.0.0 01-SEPTEMBER-2022

### Added by Rutger Blom
  - Updated the "ISO extraction" tasks found in several Playbooks so that these use xorriso instead of 7z. 7z is no longer required.
  - Implemented a workaround for an Ubuntu 20.04.x autoinstall issue in ```playbooks/DeployDNSServer.yml```. More details on the issue and the workaround we implemented can be found here: https://askubuntu.com/questions/1394441/ubuntu-20-04-3-autoinstall-with-embedded-user-data-crashing-i-got-workaround

## Dev-v5.0.0 02-SEPTEMBER-2022

### Added by Luis Chanu
  - Added ESXi v7.0 Update 3G to ```software_sample.yml``` file. (UNTESTED)
  - Added ESXi v7.0 Update 3G to ```templates_sample.yml``` file.
  - Please be sure to update your ```software.yml``` and ```templates.yml``` files.

## Dev-v5.0.0 08-SEPTEMBER-2022

### Added by Rutger Blom
  - Updated the "ansible-galaxy" preparation step in the documentation so that the "--upgrade" parameter is included in the command.

## Dev-v5.0.0 10-SEPTEMBER-2022

### Added by Luis Chanu
  - Updated SDDCLab.Version from 4 to 5 in ```templates/Pod_Config.j2``` file.
  - Modified SDDCLab version check in ```playbooks/ValidateConfiguration.yml``` file to support either 4 or 5.
  - Added automatic IP subnet addressing for NSX-T Segments.  See expanded explanation within the ```config_sample.yml``` file in the NSX-T Segments and ```Pod.BaseOverlay``` sections.
  - Added additional information on how NSX-T Segment Auto-Allocation works in the ```README.md``` file.
  - Modified ```templates/vars_NSXT_Segments.j2``` to support new automatic IP subnet addressing feature.
  - Structural changes made to ```config_sample.yml``` file:
    - Added new ```Pod.BaseOverlay``` structure.
    - Modified NSX-T Segment data structure.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 13-SEPTEMBER-2022

### Added by Rutger Blom
  - Added vCenter v7.0 Update 3H to ```software_sample.yml``` file. (UNTESTED)
  - Added vCenter v7.0 Update 3H to ```templates_sample.yml``` file.
  - Please be sure to update your ```software.yml``` and ```templates.yml``` files.

## Dev-v5.0.0 13-SEPTEMBER-2022

### Added by Luis Chanu
  - Modified comment placement for ```log_path``` entry in ```ansible.cfg``` file.
  - Updated all IP address filters (ie. ```ipaddr```, ```ipsubnet```, ```ipv4```, and ```ipv6```) with their new FQCN ```ansible.utils.xxxx``` path.  This resolved many "Deprecated" messages that were appearing during Pod deployments.
  - Many playbooks and templates were updated, including the ```config_sample.yml``` file.
  - Successfully tested all changes through multiple Pod deployments.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 14-SEPTEMBER-2022

### Added by Rutger Blom
  - Updated ```templates/vsan_silence.rb.j2``` so that less vSAN health alerts are silenced in vCenter.

## Dev-v5.0.0 15-SEPTEMBER-2022

### Added by Rutger Blom
  - Added a workaround for the issue with long creation time for static Pod configuration files (took between 1.5 to 2.5 hours to complete). Variables in the user Pod-Config file are now finalized before templating in ```playbooks/CreatePodConfig.yml```. This brings down static Pod configuration creation time to 5-10 minutes.

## Dev-v5.0.0 18-SEPTEMBER-2022

### Added by Luis Chanu
  - Made the following changes to ```playbooks/CreatePodConfig.yml``` file:
    - Added play to delete Intermediate file containing realized variables once it's no longer needed.
    - Added Intermediate filename to DEBUG play (Shown if debugging is enabled).
    - Revised time estimate for creation of static configuration file.
    - Move time estimate banner before workaround code block.

## Dev-v5.0.0 20-SEPTEMBER-2022

### Added by Rutger Blom
  - Changed default version of vCenter to 7.00U3H in ```config_sample.yml``` file.
  - Please be sure to update your ```config.yml``` file(s).

## Dev-v5.0.0 29-SEPTEMBER-2022

### Added by Luis Chanu
  - Updated ```Deploy.yml``` references in ```FirstPod.md```, ```README.md```, and ```playbooks/CreatePodConfig.yml``` files to upper case.

## Dev-v5.0.0 30-SEPTEMBER-2022

### Added by Luis Chanu
  - Corrected IP Addresses hyperlink within ```README.md``` file.

## Dev-v5.0.0 1-OCTOBER-2022

### Added by Rutger Blom
  - Modified playbooks to become (more) Ansible lint compliant.
  - Added playbook for automatic deployment of NSX Advanced Load Balancer.
  - Updated templates, playbooks, and configuration to support automatic deployment of NSX Advanced Load Balancer as part of a Pod deployment. This is still work in progress.
  - Please be sure to update your ```config.yml``` and ```software.yml``` files.

## Dev-v5.0.0 02-OCTOBER-2022

### Added by Luis Chanu
  - Renamed AVI references to ALB within ```README.md``` file.

## Dev-v5.0.0 03-OCTOBER-2022

### Added by Luis Chanu
  - Updated ```EdgeClusterPath``` to lower case in ```templates/vars_NSXT_DHCPProfiles.j2``` file to match lint changes.
  - Correct type-O in ```playbooks/FederateNsxT0BGPNeighbors.yml``` file.

## Dev-v5.0.0 06-OCTOBER-2022

### Added by Luis Chanu
  - Made the following changes to ```README.md``` file
    - Corrected type-O
    - Added additional content
    - Updated ```Upgrade Consideration``` section to include details on items to consider as part of upgrading to v5
  - Made the following changes to ```FirstPod.md``` file
    - Corrected type-O
    - Updated installation steps to align with new v5 steps listed in ```README.md```
    - Converted commands from **BOLD** to ```command``` syntax.
    - Updated ```Start your Pod deployment``` section
    - Updated ```Access your Pod's components``` section

## Dev-v5.0.0 07-OCTOBER-2022

### Added by Rutger Blom
  - Updated the ```playbooks/EnableWorkloadManagement.yml``` playbook so that the correct vSphere content library is used when Workload Management is enabled.
  - Updated ```templates/Tanzu_Payload.j2``` so that only one vSphere content library is defined in the payload that is send to the vCenter API.

## Dev-v5.0.0 07-OCTOBER-2022

### Added by Luis Chanu
  - Added additional entry to ```Upgrade Consideration``` section.

## Dev-v5.0.0 10-OCTOBER-2022

### Added by Luis Chanu
  - Following changes made to ```README.md``` file:
    - Each entry in the ```Project Features``` section now includes the SDDC.Lab version number it was introduced.
    - For Content Library, expanced on new v5 functionality.
    - Re-ordered some project features around their chronological SDDC.Lab version introduction.
    - Added details about running the ```CreateSoftwareDir.yml``` playbook.
    - Updated table of content links.

## Dev-v5.0.0 11-OCTOBER-2022

### Added by Luis Chanu
  - Added vCenter Server v8.00 and ESXi v8.00 to ```software_sample.yml```.
  - Added templates for vCenter Server and ESXi v8.00.
  - Note the new /Software directory numbering scheme used with vSphere and ESXi v8.00.  Starting with v8.00, all future versions will use that numbering scheme.
  - Successfully deployed vSphere 8 (vCenter and ESXi), but ran into issues with NSX being able to configure it.  Updated ```Known Issues``` section with information about the failure observed.
  - Updated ```license_sample.yml``` with vCenter Server v8 and ESXi v8 examples.

## Dev-v5.0.0 13-OCTOBER-2022

### Added by Luis Chanu
  - Added NSX v4.0.1.1 to ```software_sample.yml``` file.
  - Be sure to update your local ```software.yml``` file.
  - Please take note that NSX v4.0.1.1 has not yet been tested with SDDC.Lab.
  - Increased Nested_ESXi ```BootDiskSize``` parameter in ```config_sample.yml``` from 8 to 16 to support vSphere 8 deployments.  Without this change, there isn't enough space on the bootdisk, and the installation fails with the following error: ```RuntimeError: mpx.vmhba0:C0:T0:L0: disk device does not support OSDATA```.

## Dev-v5.0.0 14-OCTOBER-2022

### Added by Luis Chanu
  - Added vCenter Server v8.00 and ESXi v8.00 entries to ```templates_sample.yml``` file.
  - Added ASCII headers before each application section in ```software_sample.yml``` file to make it easier to find within Visual Studio Code (VSC).
  - Added ASCII headers before each application section in ```templates_sample.yml``` file to make it easier to find within Visual Studio Code (VSC).
  - Added note to ```README.md``` regarding issue with NSX v4.0.1.1 Federation.
  - Updated comment in ```utils/Util_CreateAllPodConfigs.sh```.

## Dev-v5.0.0 16-OCTOBER-2022

### Added by Luis Chanu
  - Added ASCII art banners to Changelog to ease navigation within VSC.
  - Added NSX-T v3.2.1.2 to ```software_sample.yml``` file.
  - Be sure to update your local ```software.yml``` file.


<br>

***
<h1 style="text-align:center">SDDC.Lab Version 5.0 Released</h1>
<br>


## Release-v5.0.0 16-OCTOBER-2022

### Added by Rutger Blom & Luis Chanu

- Released version 5 of the SDDC.Lab project.

```
██████  ███████ ██    ██       ██    ██  ██████
██   ██ ██      ██    ██       ██    ██ ██
██   ██ █████   ██    ██ █████ ██    ██ ███████
██   ██ ██       ██  ██         ██  ██  ██    ██
██████  ███████   ████           ████    ██████
```

## Dev-v6.0.0 16-OCTOBER-2022

### Added by Rutger Blom
  - Added playbook for automatic deployment of NSX Advanced Load Balancer.
  - Updated templates, playbooks, and configuration to support automatic deployment of NSX Advanced Load Balancer as part of a Pod deployment. This is still work in progress.
  - Please be sure to update your ```config.yml``` and ```software.yml``` files.

## Dev-v6.0.0 16-OCTOBER-2022

### Added by Luis Chanu
  - Removed excess spaces from DEV-V6 ASCII ART
  - Aligned comments for ALB.Deploy in ```config_sample.yml``` file.
  - Removed extra '/' from html 'br' tag or DEV-V3 entry.

## Dev-v6.0.0 17-OCTOBER-2022

### Added by Rutger Blom
  - Updates to the data structure for Advanced Load Balancer in ```config_sample.yml```.
  - Updates to ```playbooks/UpdateDNS.yml``` so that DNS records for the Advanced Load Balancer are created.
  - Added the ```vmware.alb``` Ansible Galaxy collection to ```requirements.yml```.
  - Updated ```playbooks/DeployAlb.yml``` to include a task for basic system configuration.
  - Please be sure to update your ```config.yml``` files.
  - Please be sure to run ```ansible-galaxy collection install --upgrade -r ~/git/SDDC.Lab/requirements.yml``` so that the ```vmware.alb``` Ansible Galaxy collection gets installed.

## Dev-v6.0.0 17-OCTOBER-2022

### Added by Luis Chanu
  - Removed extra spaces from ```README.md``` file.
  - Modified ```CreateContentLibrary.yml``` to create Non-TKG Content Libraries first, so that they can start synchronizing before TKG is created.  This was to resolve issue with ```DeployWorkloadVms.yml``` failing due to the WorkloadVms Content Library not being synchronized.
  - Removed excess conditional details from ```Include_Tasks_CreateContentLibrary.yml``` to adhere to lint rules.

## Dev-v6.0.0 18-OCTOBER-2022

### Added by Rutger Blom
  - Updated the ```requirements.yml``` so that a version number can be added to the collections.
  - Added version 3.0.0 to the ```community.vmware``` collection which is required due to changes in the ```community.vmware.vmware_dvs_portgroup```module.
  - Updated ```playbooks/PreparePhysical.yml``` so that the new and required parameter "inherited" is included in ```community.vmware.vmware_dvs_portgroup```tasks.

## Dev-v6.0.0 18-OCTOBER-2022

### Added by Luis Chanu
  - Added ```Test``` version to VyOS Router entry in ```templates_sample.yml```.
  - Be sure to update your ```templates.yml``` file.
  - Issue discovered with latest VyOS Ansible module (v4.0.0), whereas configuration would not be applied to the VyOS Pod-Router.  Solution is to roll back to VyOS Ansible module v3.0.1 via the following command: ```ansible-galaxy collection install --force vyos.vyos:3.0.1```
  - Added ```version: 3.0.1``` to the ```vyos.vyos``` collection in ```~/git/SDDC.Lab/requirements.yml``` file to ensure proper version of VyOS Ansible Module is installed.
  - Updated ```playbooks/CreateVds.yml``` so that the new and required parameter "inherited" is included in ```community.vmware.vmware_dvs_portgroup```tasks.
  - Aligned comments in ```config_sample.yml``` file.

## Dev-v6.0.0 19-OCTOBER-2022

### Added by Rutger Blom
  - Added ```playbooks/DeployAlb.yml``` to ```Deploy.yml```. Advanced Load Balancer is not deployed by default (i.e. ```Deploy.Product.ALB.Deploy: false``` in ```config_sample.yml```). 
  - Added tasks to ```playbooks/DeployAlb.yml``` that perform bootstrap, a cluster name, and cluster VIP.
  - Commented out the newly added tasks for now as investigation is needed.

## Dev-v6.0.0 19-OCTOBER-2022

### Added by Luis Chanu
  - Removed ```no_log``` from playbooks which target nested components, with the exception of licensing playbooks.
  - Indented Jinja within ```templates/vars_License_ESXi.j2``` to improve readablity.
  - Indented Jinja within ```templates/vars_License_vSAN.j2``` to improve readablity.
  - Changed ```License``` to ```KeyCode``` in Jinja templates for consistency with other product license references.
  - Modified ```templates/License_vSphere.yaml``` as follows:
    - Added KeyCode defaults to handle use case where there are insufficiet socket licenses available (as Jinja does not include ```KeyCode``` key in that case)
    - Added additional DEBUG tasks
    - Udded additional comments
    - Changed ESXi and vSAN licensing to use ESXi version rather than vCenter version to match license keys
  - Added vRLI and ALB product versions to static Pod-Config filename within ```playbooks/CreatePodConfig.yml```.
  - In preparation for future playbooks, added the following variables to ```config_sample.yml``` file:
    - ```Common.Syslog.Level```
    - ```Common.Timezone```

## Dev-v6.0.0 20-OCTOBER-2022

### Added by Luis Chanu
  - Updated variable references in ```playbooks/DeployAlb.yml``` file.

## Dev-v6.0.0 20-OCTOBER-2022

### Added by Rutger Blom
  - Added new tasks to ```playbooks/DeployAlb.yml``` for ALB bootstrap, base configuration, and controller cluster configuration.
  - Added new field ```Password``` to the ALB section in ```software_sample.yml``` and ```templates/Pod_Config.j2```. This is field contains a version specific default admin password and is required during ALB bootstrap.
  - Added task to ```playbooks/DeployAlb.yml``` that checks for Web UI availability on cluster VIP FQDN.
  - Fixed a typo in ALB VIP FQDN in ```config_sample.yml```.
  - Be sure to update your ```config.yml``` and ```software.yml``` file.

## Dev-v6.0.0 20-OCTOBER-2022

### Added by Luis Chanu
  - Added additional NSX Advanced Load Balancer versions to ```software_sample.yml``` file.
  - Updated ```SDDCLab.Version``` variable in ```templates/Pod_Config.j2``` from 5 to 6.
  - Updated ```playbooks/ValidateConfiguration.yml``` to accept version 6 configuration files.
  - The following changes were made to ```config_sample.yml```:
    - Modified ```Nested_vRLI``` data structure in to follow NSX-T and ALB data structures
    - Added ```Cluster_VIP``` address
  - Added ```Cluster_VIP``` configuration to ```playbooks/DeployVrli.yml``` file.
  - Change NTP configuration within ```playbooks/DeployVrli.yml``` to use ```Cluster_VIP``` rather than Node IP address.
  - Updated ```playbooks/UpdateDNS.yml``` to populate DNS with the new ```Nested_vRLI``` data structure.
  - Be sure to update your ```config.yml``` file.
  - Updated IP Address Assignment table in ```README.md``` file to show that vRLI VIP is now included as part of the default deployment.
  - Update vRLI FQDN to use Cluster_VIP FQDN address in ```playbooks/License_vRLI.yml``` file.
  - Added ```playbooks/ConfigureNsxCentralNodeConfigProfile.yml``` playbook to SDDC.Lab.  This playbook configures Syslog, NTP, and Timezone settings on all NSX components.
  - Added ```playbooks/ConfigureNsxCentralNodeConfigProfile.yml``` playbook to ```Deploy.yml```.  Currently configured to NOT be run as part of a deployment.

## Dev-v6.0.0 21-OCTOBER-2022

### Added by Luis Chanu
  - Renamed ```playbooks/ConfigureNsxCentralNodeConfigProfile.yml``` to ```playbooks/ConfigureNsxBasicConfiguration.yml```.
  - Enabled ```playbooks/ConfigureNsxBasicConfiguration.yml``` in ```Deploy.yml``` file.

## Dev-v6.0.0 21-OCTOBER-2022

### Added by Rutger Blom
  - Moved ALB basic configuration tasks to a separate playbook ```playbooks/ConfigureAlbBasicConfiguration.yml```.
  - Enabled ```playbooks/ConfigureAlbBasicConfiguration.yml``` in ```Deploy.yml``` file.
  - Added ```BackupServer```section to ```Nested_ALB```in ```config_sample.yml```
  - Added task in ```playbooks/ConfigureAlbBasicConfiguration.yml``` that configures the required backup passphrase and configuration backup.
  - Be sure to update your ```config.yml``` file.

## Dev-v6.0.0 21-OCTOBER-2022

### Added by Luis Chanu
  - Renamed ```Nested_NSXT.BackupServer``` dictionary to ```Nested_NSXT.Backup``` in ```config_sample.yml``` file.
  - Updated ```Nested_NSXT.Backup``` structure to follow new backup structure.
  - Moved credential information within ```BackupServer``` dictionary below a new key called ```Credential``` within ```config_sample.yml`` file.
  - Updated ```playbooks/ConfigureNsxBackup.yml``` playbook to use ```Nested_NSXT.Backup```.
  - Updated ```Nested_ALB.BackupServer``` values to use updated ```BackupServer``` values.
  - Be sure to update your ```config.yml``` file.
  - Added vSphere Replication Appliance to the IP Address Assignment table in ```README.md```.
  - Added ```Replication``` key to ```software_sample.yml``` file.

## Dev-v6.0.0 22-OCTOBER-2022

### Added by Rutger Blom
  - Updated task in ```playbooks/ConfigureAlbBasicConfiguration.yml``` so that the ALB API accepts Basic Authentication.
  - Added new playbook ```playbooks/ConfigureAlbClouds.yml``` that configures Clouds in ALB. For now the Pod's vSphere environment is added as an ALB Cloud.
  - Updated ```Deploy.yml``` so that ```playbooks/ConfigureAlbClouds.yml``` is included.

## Dev-v6.0.0 23-OCTOBER-2022

### Added by Rutger Blom
  - Updated the ```Nested_ALB``` section in ```config_sample.yml``` to include a first piece of data structure for ALB Clouds configuration. This is work in progress.
  - Added conditionals to tasks in ```playbooks/ConfigureAlbClouds.yml``` maing use of the new piece of data structure.
  - Be sure to update your ```config.yml``` file.

## Dev-v6.0.0 25-OCTOBER-2022

### Added by Luis Chanu
  - Merged ```repl``` branch into ```dev_v6``` branch.  This code is not yet complete.
  - Added ```playbooks/DeployReplication.yml``` playbook to SDDC.Lab project to deploy vSphere Replication Appliance onto a nested vSphere cluster.
  - Added ```Deploy.Software.Replication``` section to ```config_sample.yml``` and ```templates/Pod_Config.j2``` files.
  - Added ```Nested_Replication``` section to ```config_sample.yml``` file.
  - Moved ```Deploy.Product.ALB``` up in the configuration file to ease reading due to ```NSXT``` indentations.
  - Added vRealize Log Insight v8.10.0 to the ```software_sample.yml``` file. (UNTESTED)

## Dev-v6.0.0 26-OCTOBER-2022

### Added by Rutger Blom
  - Miscellaneous updates to ```playbooks/ConfigureAlbClouds.yml``` so that a vSphere Cloud is now successfully added.

## Dev-v6.0.0 26-OCTOBER-2022

### Added by Luis Chanu
  - Added ```playbooks/DeployReplication.yml``` playbook to ```Deploy.yml``` file.
  - Updated ```Common.Syslog``` IPv4 and IPv6 addresses to point to vRLI VIP rather than the physical appliance.
  - Changed case of ```NONE``` version entries to lower case in ```playbooks/CreatePodConfig.yml``` file to aid in readability.

## Dev-v6.0.0 27-OCTOBER-2022

### Added by Luis Chanu
  - Added deployment size option to OVF deployment of vSphere Replication.
  - Renamed ```Nested_Replication.Component.Appliance.Deployment.CPU``` key to ```Nested_Replication.Component.Appliance.Deployment.Size``` within ```config_sample.yml```, and changed options to ```light``` and ```standard``` for 2 or 4 CPU deployment, respectively.
  - Updated ```playbooks/DeployReplication.yml``` to use updated variable.
  - Added ```playbooks/ConfigureReplicationBasicConfig.yml``` to configure basic services for vSphere Replication. (TESTED)
  - Added ```playbooks/ConfigureReplicationBasicConfig.yml``` to ```Deploy.yml``` file.
  - Be sure to update your ```config.yml``` file.
  - Renamed ```playbooks/ConfigureNsxBasicConfiguration.yml``` to ```playbooks/ConfigureNsxBasicConfig.yml```.
  - Updated ```Deploy.yml``` to use new ```playbooks/ConfigureNsxBasicConfig.yml``` file.
  - Added task in ```playbooks/DeployReplication.yml``` to deleted vSphere Replication extracted ISO files. (TESTED)
  - For consistency, updated the Pod's temporary directory deletion task in ```playbooks/ValidateConfiguration.yml``` to use the ```Target.TempFolder``` variable that is used by each of the various playbooks throughout SDDC.Lab.  (TESTED)

## Dev-v6.0.0 28-OCTOBER-2022

### Added by Rutger Blom
  - Replaced a static value in the ```playbooks/ConfigureAlbClouds.yml``` playbook.
  - Renamed playbook to ```playbooks/ConfigureAlbBasicConfig.yml```
  - Added tasks to the ```playbooks/ConfigureAlbClouds.yml``` playbook so that the Service Engine "Default-Group" is properly configured.
  - Added task that sets the Service Engine "Default-Group" as the Template Service Engine Group on the vSphere Cloud object.
  - Creation of a "dummy" Virtual Service with VS VIP and Pool on the Pod's VMNetwork VLAN is successful. Two SEs are deployed from the Pod's Content Library into the nested "ComputeA" vSphere Cluster and have their vNICs connected to the ServiceVMs (for management traffic) and VMNetwork (for data traffic) Port Groups.

## Dev-v6.0.0 28-OCTOBER-2022

### Added by Luis Chanu
  - Corrected ```Nested_vRLI``` variable references in ```UpdateDNS.yml```, ```CleanupDNS.yml```, and ```Undeploy.yml``` files. (TESTED)
  - Added vSphere Replication to ```UpdateDNS.yml``` and ```CleanupDNS.yml``` files. (TESTED)

## Dev-v6.0.0 29-OCTOBER-2022

### Added by Rutger Blom
  - Added DHCP service to the "ServiceVM" VLAN in the VyOS configuration.
  - Changed DHCP IP range for the "VMNetwork" and "ServiceVM" VLAN to 200-254 in the VyOS configuration. 

## Dev-v6.0.0 30-OCTOBER-2022

### Added by Rutger Blom
  - Added new items to the ```Nested_ALB``` data structure in ```config_sample.yml```.
  - Added tasks to ```playbooks/ConfigureAlbClouds.yml``` that add and configure an NSX-T Cloud in ALB.
  - Automated ALB deployment is still work in progress and many items still need to be done. Currently we have code that:
    - Deploys an ALB Controller, 
    - Applies basic configuration to this ALB Controller (DNS, NTP, Backup, etc) 
    - Configures a vSphere Cloud utilizing the ```ServiceVMs``` Port Group for Service Engine Management traffic and the ```Pod-xxx Local Content Library``` for storing and deploying Service Engine images.
    - Configures an NSX-T Cloud utilizing overlay segments ```SEG-ALB-SE-Management``` for Service Engine Management Traffic and  ```SEG-ALB-SE-Data``` for Service Engine Data traffic. Both these segments attach to the ```T1-Gateway-ALB``` Tier-1 Gateway. ```Pod-xxx Local Content Library``` is used for storing and deploying Service Engines images.
  - Be sure to update your ```config.yml``` file.

## Dev-v6.0.0 01-NOVEMBER-2022

### Added by Rutger Blom
  - Added tasks to ```playbooks/ConfigureAlbClouds.yml``` that add an IP subnet definition to the ```SEG-ALB-SE-Data``` Network in ALB. Networks in ALB must have a subnet definition before VIPs that should connect to these networks can be created. In the case of the ```SEG-ALB-SE-Data``` Network, IP subnet information is obtained from the NSX-T API which owns and controls the IP subnet configuration of the underlying overlay segment.

## Dev-v6.0.0 02-NOVEMBER-2022

### Added by Rutger Blom
  - Added tasks to ```playbooks/ConfigureAlbClouds.yml``` that add an IP subnet definition to the ```VMNetwork``` Network in ALB. Networks in ALB must have a subnet definition before VIPs that should connect to these networks can be created. In the case of the ```VMNetwork``` Network, IP subnet information is obtained from the Pod configuration which contains IP subnet information of the underlying VLAN.

## Dev-v6.0.0 04-NOVEMBER-2022

### Added by Rutger Blom
  - Added ALB to ```Undeploy.yml```.
  - Added ALB API "polling" tasks replacing static delay tasks in ```playbooks/ConfigureAlbClouds.yml```.
  - Added ASCI art headers to ```playbooks/ConfigureAlbClouds.yml``` to improve readability.

## Dev-v6.0.0 05-NOVEMBER-2022

### Added by Rutger Blom
  - Added a task to ```playbooks/ConfigureAlbClouds.yml``` that checks whether a vCenter Server is already configured for the NSX-T Cloud. The result is used as a conditional on the task that configures the vCenter Server for the NSX-T Cloud. This "check" task is needed to keep the playbook idempotent.

## Dev-v6.0.0 25-NOVEMBER-2022

### Added by Rutger Blom
  - Removed tasks from ```playbooks/ConfigureAlbClouds.yml``` that add an IP subnet definition to the ```SEG-ALB-SE-Data``` Network in ALB. NSX-T Overlay networks in ALB do not require a subnet definition.
  - Updated defaults for ```ServiceEngineNamePrefix``` and ```ServiceEngineFolder``` in ```config_sample.yml```.
  - Be sure to update your ```config.yml``` file.

## Dev-v6.0.0 12-DECEMBER-2022

### Added by Luis Chanu
  - Added vCenter Server v7.0 Update 3I to ```software_sample.yml``` and ```templates_sample.yml``` files.  (NOT TESTED)

## Dev-v6.0.0 05-JANUARY-2023

### Added by Luis Chanu
  - To simplify authentication to SDDC.Lab Pods, added ```SDDCLab_Credentials_for_Firefox.csv``` file to ```misc``` folder.  This file contains the default URLs, usernames, and passwords for the various components that are deployed with each lab.  This file is for Firefox, and other browsers may be added in the future.  Import this file into Firefox to populate the Passwords within Firefox.
  - Added instructions to ```README.md``` and ```FirstPod.md``` files.
  - Added vCenter Server versions 7.0U3J and 8.00a to ```software_sample.yml``` and ```templates_sample.yml``` files.  (NOT TESTED)

## Dev-v6.0.0 06-JANUARY-2023

### Added by Luis Chanu
  - Updated ALB ```Config``` and ```Installer``` variables in ```config_sample.yml``` to reference ALB instead of AVI within it's filename.

## Dev-v6.0.0 08-JANUARY-2023

### Added by Luis Chanu
  - Removed duplicate ```playbooks/ConfigureAlbClouds.yml``` entry from Deploy.yml.

## Dev-v6.0.0 09-JANUARY-2023

### Added by Luis Chanu
  - Corrected ALB password entries in ```misc/SDDCLab_Credentials_for_Firefox.csv``` file.

## Dev-v6.0.0 17-FEBRUARY-2023

### Added by Luis Chanu
  - All newly added software has NOT yet been tested.
  - Added the following updates to the software repository:
    - ESXi v8.00B
    - vCenter Server v8.00B
    - vRealize Log Insight v8.10.2
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` with updated ESXi and vCenter references.  (NOT TESTED)

## Dev-v6.0.0 22-FEBRUARY-2023

### Added by Luis Chanu
  - Added YYYYMMDD date to prepared/static Pod configuration filename.

## Dev-v6.0.0 27-FEBRUARY-2023

### Added by Luis Chanu
  - Added vSphere Replication v8.6.0.1 to ```software_sample.yml```.
  - vSphere Replication is still NOT functional/supported by SDDC.Lab.

## Dev-v6.0.0 28-FEBRUARY-2023

### Added by Luis Chanu
  - Added NSX v4.1.0.0 to ```software_sample.yml```. (TESTED)
  - NSX Federation now works with NSX v4.1.0.0, so updated Federation section of the ```README.md```.

## Dev-v6.0.0 3-MARCH-2023

### Added by Luis Chanu
  - Updated the ```README.md``` file
    - Updated the *temp* path in the documentation to use the correct path, as it was updated since the documentaton was originally written.
    - Added "Known Items" entry regarding licensing when Enhanced Link Mode (ELM) is configured.

## Dev-v6.0.0 4-MARCH-2023

### Added by Luis Chanu
  - Created new ```CreateDrsVmRules.yml``` playbook which creates a DRS VM-VM Rule at the end of the Pod deployment.
  - Added ```CreateDrsVmRules.yml``` playbook to the end of ```Deploy.yml``` playbook
  - Added task in ```Undeploy.yml``` playbook to delete DRS VM-VM rule
  - The following changes were made to ```config_sample.yml```:
    - Added ```Deploy.DRS```section to support new DRS VM Rule functionality
    - Updated ```Nested_Replication``` section
    - Changed default software versions of ESXi, vCenter Server, NSX, and vRLI to latest tested versions
  - Added new ```Deploy.DRS``` variables to ```templates/Pod_Config.j2```
  - Be sure to update your ```config.yml``` file(s).

## Dev-v6.0.0 5-MARCH-2023

### Added by Luis Chanu
  - Aligned Target variable with other variables
  - Modified ```Nested_vCenter.SSO.ReplicationPartner``` variable in ```config_sample.yml``` from "" (empty quotes) to undefined if no replication partner is being used.
  - Modified several playbooks to support the ```Nested_vCenter.SSO.ReplicationPartner``` change.
  - Modified ```License_vSphere.yml``` playbook to install all ESXi and vSAN licenses in vCenter Server when a Pod has ```Nested_vCenter.SSO.ReplicationPartner``` configured.
  - Updated ```README.md``` file to explain how all ESXi and vSAN licenses are added to vCenter Server when ```Nested_vCenter.SSO.ReplicationPartner``` (Enhanced Link MOde) is configured.
  - Be sure to update your ```config.yml``` file(s).

## Dev-v6.0.0 6-MARCH-2023

### Added by Luis Chanu
  - Reverted lint changes back to original settings by changing all ```failed_when: false``` references to ```ignore_errors: true```.
  - Removed duplicate ```ignore_errors: true``` entries.

## Dev-v6.0.0 8-MARCH-2023

### Added by Luis Chanu
  - Added NSX-T v3.2.2 to ```software_sample.yml``` file.
  - Be sure to update your ```software.yml``` file.

## Dev-v6.0.0 9-MARCH-2023

### Added by Luis Chanu
  - Updated all ```community.general.net_tools.nsupdate``` references to ```community.general.nsupdate``` to address deprecation message.
  - Changes made to VyOS Pod-Router configuration
    - Corrected PING issue in newer VyOS ISO image by moving PING after configuration mode is exited.
    - Added additional ```exit``` commands logout of the VyOS router on the console after deployment is complete.
  - Issue found with VyOS v1.4 not supporting CLI configuration commands for NTP.
  - NTP CLI commands commented in ```templates/vyos_router.j2``` template.
  - Added ```utils/Util_GeneratePodRouterConfig.yml``` file.

## Dev-v6.0.0 11-MARCH-2023

### Added by Luis Chanu
  - Updated ```ValidateConfiguration.yml``` playbook to only accept SDDC.Lab version 6 configuration files.
  - Updated outdated Ubuntu URLs in ```software_sample.yml```.
  - Tested download for each Ubuntu server version.
  - Be sure to update your ```software.yml``` file.

## Dev-v6.0.0 12-MARCH-2023

### Added by Luis Chanu
  - Updated ```var_UbuntuConfiguration``` variable references in Ubuntu templates to match case of variable definition in ```DeployDNSServer.yml``` playbook.

## Dev-v6.0.0 20-MARCH-2023

### Added by Luis Chanu
  - Added entry for Ubuntu v22.04.1 to ```templates_sample.yml``` file.
  - Be sure to update your ```templates.yml``` file.

## Dev-v6.0.0 23-MARCH-2023

### Added by Luis Chanu
  - Modified ansible installation within ```pip3_requirements.txt``` to install Ansible v6.4.0 rather than the latest v7.x version.  Ansible v7.x causes ```CreatePodConfig.yml``` playbook to take 30+ minutes to generate a static configuration, while Ansible v6.4.0 and process that same configuration in 3+ minutes.

## Dev-v6.0.0 27-MARCH-2023

### Added by Luis Chanu
  - Issues identified with Ubuntu v22.04.1 deployment.  Upon further digging, appears some folder structures have changed in the ISO.  Additional discovery needed.  For now, use v20.04.x for all DNSServer deployments, then upgrade to v22.04.1 post-deployment if v22.04.x is required/desired.

## Dev-v6.0.0 29-MARCH-2023

### Added by Luis Chanu
  - Updated verbiage in NSX-T Federation section of ```README.md``` file.

## Dev-v6.0.0 4-APRIL-2023

### Added by Luis Chanu
  - Created new utility to display various X.509 certificate thumbprints for a given website.
  - The new utility is ```utils/Util_GetCertFingerprints.sh```.
  - Documentation on how to use the new utility can be found within the file.

## Dev-v6.0.0 5-APRIL-2023

### Added by Luis Chanu
  - All newly added software has NOT yet been tested.
  - Added the following updates to the software repository:
    - vCenter Server v8.00C
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` with updated vCenter references.  (NOT TESTED)

## Dev-v6.0.0 18-APRIL-2023

### Added by Luis Chanu
  - All newly added software has NOT yet been tested.
  - Added the following updates to the software repository:
    - ESXi v7.00 Update 3L
    - vCenter Server v7.00 Update 3L
    - ESXi v8.00 Update 1
    - vCenter Server v8.00 Update 1
    - NSX v3.2.2.1
    - vSphere Replication v8.7.0
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` with updated vCenter references.  (NOT TESTED)
  - Be sure to update your ```software.yml``` and ```templates.yml``` files.

## Dev-v6.0.0 26-APRIL-2023

### Added by Luis Chanu
  - Updated ```README.md``` file
    - Corrected minor gramatical type-O's
    - Added information about DHCP support when automatic deployment of workloads is enabled with Federation.
    - Updated various outdated and non-functional hyperlinks.
    - Added Federation onboarding issue with NSX v3.2.2.1 to the "Issues With Various Software Versions" table.
    - Added additional information around Ubuntu version to use for SDDC.Lab DNS server deployment.

## Dev-v6.0.0 28-JUNE-2023

### Added by Luis Chanu
  - All newly added software has NOT yet been tested.
  - Added the following updates to the software repository:
    - ESXi v8.00 Update 1A
    - vCenter Server v8.00 Update 1A
    - vCenter Server v8.00 Update 1B
    - NSX v4.1.0.2
    - vRealize Log Insight v8.12.0
  - Removed NSX v4.1.0.0 from software repository
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` with updated vCenter references.  (NOT TESTED)
  - Be sure to update your ```software.yml``` and ```templates.yml``` files.

## Dev-v6.0.0 29-JUNE-2023

### Added by Luis Chanu
  - Corrected output file name in comments of ```utils\Util_GeneratePodRouterConfig.yml``` playbook.
  - Configuration of Pod-Router failed due to two VyOS commands which the current nightly-build of VyOS no longer supports.  Issue is with the ```facility all``` before the ```protocol`` argument.
  - Commented the following two command from the ```templates\vyos_router.j2``` Jinja2 template:
    - ```set system syslog global facility protocols level debug```
    - ```set system syslog host 10.203.120.19 facility all protocol udp```
  - Added note to ```pip3_requirements.txt``` file about not using ```ansible-pylibssh``` module, as it causes issues with configuration push within ```ConfigureRouter.yml``` playbook.
  - Changes to ```ConfigureRouter.yml``` playbook:
    - Updated comments at top of playbook
    - Converted playbook to use ```ansible.netcommon.network_cli``` as VyOS module deprecated use of ```provider``` section in its tasks
  - Added note in ```pip3_requirements.txt``` file regarding ```ansible-pylibssh```
  - Added vRLI v8.12.0 filename to ```software_sample.yml```
  - Added vCenter Server v7.0 Update 3M to the software repository:
  - Added vCetner Server v7.0 Update 3M to ```software_sample.yml``` and ```templates_sample.yml``` files (NOT TESTED)
  - Be sure to update your ```software.yml``` and ```templates.yml``` files.
  - Updated user message in ```CreatePodConfig.yml``` to indicate more accurate time of how long it takes to generate the static configuration file
  - Added conditional check of ```network_policy.inherited``` in ```Create Port Groups``` play in ```playbooks/CreateVds.yml``` to omit if ```Target.Deployment == Host``` as there are no vDS's when deploying directly to an ESXi host.

## Dev-v6.0.0 30-JUNE-2023

### Added by Luis Chanu
  - Added ```utils/Util_GetLabInfo.sh``` script to collect lab environment information.
  - Revert ```playbooks/CreateVds.yml``` back to original configuration by removing the conditional check that was added on 29-JUNE-2023.
  - Issue found when ```Target.Deployment == 'Host'``` and subscribed content library is type 'vCenter', as no vCenter exists to subscrube to.  To mitigate the issue, added conditions to ```ansible.builtin.include_tasks``` within ```playbooks/CreateContentLibrary.yml``` to skip the creation of any content libraries when that condition exists.

## Dev-v6.0.0 1-JULY-2023

### Added by Luis Chanu
  - Increased ```ansible.builtin.uri``` timeouts from 15 to 20 seconds in ```DeployNsxLocalManager.yml``` to address timeouts on busy systems
  - In ```Undeploy.yml``` playbook, added condition to ```Delete DRS VM-VM Affinity Rule``` task to only run when deploying to vCenter
  - Added conditions to ```CreateDrsVmRules.yml``` playbook tasks to only execute when ```Target.Deployment == 'vCenter'```

## Dev-v6.0.0 2-JULY-2023

### Added by Luis Chanu
  - Tested ```Deploy.yml``` and ```Undeploy.yml``` playbooks with updated ```community.vmware``` ansible module v3.7.0.
  - Updated ```community.vmware``` install version from v3.0.0 to v3.7.0 in ```requirements.yml``` file.

## Dev-v6.0.0 27-JULY-2023

### Added by Rutger Blom
  - Updated ```pip3_requirements.txt``` to ensure that version 38.0.4 of cryptography is installed. This to avoid the "module 'lib' has no attribute 'OpenSSL_add_all_algorithms" error when connecting to the physical vCenter. 

## Dev-v6.0.0 28-JULY-2023

### Added by Rutger Blom

  - Updated ```licenses_sample.yml``` so it has an example entry for vSAN version 8.

## Dev-v6.0.0 28-JULY-2023

### Added by Rutger Blom

  - Updated ```templates/vsan_silence.rb.j2``` so the "vumconfig" health check is silenced. This so that the user is not faced with a warning on the vSAN
  build recommendation engine which now needs additional configuration.
  - Updated ```requirements.yml``` so that community.vmware 3.8.0 can be used.
  - Added vCenter Server v8.00 Update 1C to ```software_sample.yml```.

## Dev-v6.0.0 02-AUGUST-2023

### Added by Rutger Blom
  - Added NSX Advanced Load Balancer v22.1.3 and v22.1.4 to ```software_sample.yml```.

## Dev-v6.0.0 03-AUGUST-2023

### Added by Luis Chanu
  - Fixed type-O's in ```CHANGELOG.md``` file.
  - Created ```utils/Util_AddIPv4DNSRecord.sh``` which simplifies the manual creation of a single IPv4 DNS record

## Dev-v6.0.0 06-AUGUST-2023

### Added by Luis Chanu
  - Created ```utils/Util_GenerateDNSZoneFiles.yml`` to test and troubleshoot DNS Jinja2 templates.
  - Added ```templates/BIND_v9_db.reversezoneipv4_overlay.j2``` to provide Reverse DNS for IPv4 overlay network space.
  - Added ```templates/BIND_v9_db.reversezoneipv6_overlay.j2``` to provide Reverse DNS for IPv6 overlay network space.  Note that the addres space used for IPv6 overlay is hard coded within this Jinja2 template.
  - Added vCenter v7.00 Update 3M to ```templates_sample.yml``` file.

## Dev-v6.0.0 07-AUGUST-2023

### Added by Luis Chanu
  - Increased delays from 5 seconds to 10 seconds in dialogs 4-7 of ```DeployRouter.yml``` playbook to accomodate busy servers with slow disk performance.
  - Created ```utils/Util_GetLatestVyosISO.sh``` script to download the latest VyOS ISO file.

## Dev-v6.0.0 08-AUGUST-2023

### Added by Luis Chanu
  - Added the following software products to ```software_sample.yml``` file:
    - NSX-T v3.2.3
    - NSX-T v3.2.3.1
    - vSphere Replication v8.7.0.2

## Dev-v6.0.0 09-AUGUST-2023

### Added by Luis Chanu
  - Modified ```ConfigureNestedEsxi.yml``` playbook to "eject" the mounted custom ESXi ISO/CD from the Guest VM's CD-ROM drive by setting CD-ROM type to ```none```.

## Dev-v6.0.0 10-AUGUST-2023

### Added by Rutger
  - Modified ```config_sample.yml``` to correct the values for the DNS server keyboard layout and variant in accordance with ```/usr/share/X11/xkb/rules/xorg.lst```
  - Be sure to update your ```config.yml``` file(s).
  - Update the OS NIC name in ```templates/Ubuntu_v22.04.1_user-data.j2``` to ```ens33``` as that seems what it's called in an Ubuntu 22.04 VM.
  - Added back an updated entry for Ubuntu 22.04 in ```software_sample.yml```
  - 7z required for correct extraction of the Ubuntu 22.04 ISO. Updated README.md with this requirement.
  - Renamed template files and updates ```templates_sample.yml```
  - Be sure to update your ```templates.yml``` file.

## Dev-v6.0.0 11-AUGUST-2023

### Added by Rutger
  - Consolidated the Ubuntu versions for the DNS server. Version 22.04 is now the required and only supported version. The DNS server deployment script will automaticallly download the correct ISO file (https://cdimage.ubuntu.com/ubuntu-server/jammy/daily-live/current/jammy-live-server-amd64.iso) when this ISO file does not exist in the local software library (e.g. /Software/Ubuntu/Server/v22.04/jammy-live-server-amd64.iso)
  - Be sure to update your ```templates.yml``` file.
  - Be sure to update your ```software.yml``` file.
  - Be sure to update your ```config.yml``` file(s).

## Dev-v6.0.0 23-AUGUST-2023

### Added by Luis Chanu
  - Added NSX v4.1.1 to ```software_sample.yml``` file. (UNTESTED)

## Dev-v6.0.0 26-AUGUST-2023

### Added by Luis Chanu
  - Updated ```config_sample.yml``` as follows:
    - Updated software versions to latest releases
    - Added ```DeploymentSetting``` to ```Common``` and most ```Nested_xxx``` sections to prepare for future functionality.
  - Be sure to update your ```config.yml``` file(s).
  - Modified ```DeployNestedEsxi.yml``` playbook to support ```DeploymentSetting``` items on nested ESXi VMs:
    - Reserve all guest memory (All locked)
    - Memory Shares
  - Modified ```DeployRouter.yml``` playbook to support ```DeploymentSetting``` items on VyOS router VM:
    - Reserve all guest memory (All locked)
    - Memory Shares
    
## Dev-v6.0.0 27-AUGUST-2023

### Added by Rutger Blom
  - Created ```utils/Util_ShutdownPod.yml``` playbook that performs graceful shutdown of a Pod.

## Dev-v6.0.0 27-AUGUST-2023

### Added by Luis Chanu
  - Added information about new memory reservation & shares functionality to the ```README.md``` file.
  - Added additional information about the new memory reservation and shares functionality to the ```README.md``` file.
  - Modified ```utils/Util_ShutdownPod.yml``` playbook to support both vCenter and Host based deployments. (UNTESTED)
  - Removed ```DeploymentSetting``` data structure from ```Nested_Replication``` section within ```config_sample.yml``` file because the replication appliance VM is deployed within the nexted vSphere cluster.
  - Be sure to update your ```config.yml``` file(s).
  - Added memory resource & share support to the following playbooks:
    - ```DeployAlb.yml```
    - ```DeployNsxGlobalManager.yml```
    - ```DeployNsxLocalManager.yml```
    - ```DeployVc.yml```
    - ```DeployVrli.yml```
  - Added task to ```DeployVc.yml``` to disable password expiration on Nested vCenter Server

## Dev-v6.0.0 29-AUGUST-2023

### Added by Luis Chanu
  - In an effort to catch issues early in the Pod deployment process, Pod-Router reachability tests were added to both ```DeployRouter.yml``` and ```ConfigureRouter.yml``` playbooks. (TESTED)

## Dev-v6.0.0 30-AUGUST-2023

### Added by Luis Chanu
  - Removed '-' from ```vars:``` declaration in tasks within ```ConfigureRouter.yml``` playbook.

## Dev-v6.0.0 08-SEPTEMBER-2023

### Added by Rutger Blom
  - Increased number of retries to ```60``` on the ```Verify Pod reachability by pinging Pod-Router management interface``` task in ```playbooks/ConfigureRouter.yml```.

## Dev-v6.0.0 13-SEPTEMBER-2023

### Added by Luis Chanu
  - Added ```nslookup``` verification test to end of ```utils/Util_AddIPv4DNSRecord.sh``` script.
  
## Dev-v6.0.0 21-SEPTEMBER-2023

### Added by Aaron Ellis
  - **CONFIG FILE UPDATE**  Updated ```config_sample.yml``` to add DNS protocol and forwarders to common variable section
  - Updated ```software_sample.yml``` VyOS download URL to account for move to Github Releases  NOTE: keeping the generic filename, will only pull if local Software repo is empty
  - Updated memory on pod routers to 1gb from 512 in ```playbooks/DeployRouter.yml``` VyOS increased minimum HW specs around version 1.4.  Pushing config to a 1.5 instance was running it out of memory.
  - Updated ```playbooks/UpdateDNS.yml``` to consume new common DNS vars including selectable protocol for DNS updates
  - Added retry and increased command timeout when applying pod router config in ```playbooks/ConfigureRouter.yml```  Could be enviromental, could be newer builds, if yours is faster it won't matter.
  - Updated ```templates/Ubuntu_v22.04_Netplan.j2``` with new syntax for default route in netplan.

## Dev-v6.0.0 24-SEPTEMBER-2023

### Added by Luis Chanu
  - Removed extra spaces from ```config_sample.yml``` as part of cleanup.  No need to rebuild static configurations, as this is purely cosmetic.
  - Added vCenter Server and ESXi v8.00 Update 2 to Software repository (UNTESTED).
  - Updated ```software_sample.yml``` and ```templates_sample.yml``` to support v8.00 Update 2.
  - Be sure to update your ```software.yml``` and ```templates.yml``` files.

## Dev-v6.0.0 25-SEPTEMBER-2023

### Added by Aaron Ellis
  - Updated ```requirements.yml``` for community.vmware collection version 3.9.0, 3.8.0 intriduced a bug in vmware_deploy_ovf https://github.com/ansible-collections/community.vmware/issues/1808. Please run ```ansible-galaxy collection install --upgrade -r ~/git/SDDC.Lab/requirements.yml``` to update to version 3.9.0
  - Updated ```playbooks/DeployDNSServer.yml``` to correct some errors in dubug output

## Dev-v6.0.0 25-SEPTEMBER-2023

### Added by Luis Chanu
  - Updated software versions in ```config_sample.yml``` to the following versions:
    - vCenter Server: ```8.00U2```
    - ESXi: ```8.00U2```
    - NSXT: ```4.1.1```
  - Updated ```config_sample.yml``` by increasing memory for NSX prepared clusters in ```Nested_ESXi``` from 20G to 24G.  This was done to resolve NSX host prep failing during certain deployment scenarios.
  - Be sure to update your ```config.yml``` files.

## Dev-v6.0.0 14-OCTOBER-2023

### Added by Rutger Blom
  - Added validation tasks for NSX ALB to ```playbooks/ValidateConfiguration.yml```
  - Added NSX ALB version 22.1.5 and 30.1.1 to ```software_sample.yml```
  - Be sure to update your ```software.yml``` file.

## Dev-v6.0.0 17-OCTOBER-2023

### Added by Luis Chanu
  - Updated ```templates/vyos_router.j2``` file to correct DHCP issue with VMNetwork getting served the wrong IP addresses.  This change should now ensure that ServiceVM and VMNetwork workloads get addresses from their respective DHCP ranges.

## Dev-v6.0.0 19-OCTOBER-2023

### Added by Rutger Blom
  - Added NSX 4.1.2 to Software repository (UNTESTED).
  - Be sure to update your ```software.yml``` file.

## Dev-v6.0.0 22-OCTOBER-2023

### Added by Luis Chanu
  - Added vSphere Replication v8.7.0.3 to ```software_sample.yml``` file. (UNTESTED)
  - Be sure to update your ```software.yml``` file.

## Dev-v6.0.0 23-OCTOBER-2023

### Added by Luis Chanu
  - Changed ```Deploy.Product.NSXT.Federation.Enable``` reference to ```Deploy.Product.NSXT.Federation.Deploy``` in ```README.md``` file.
  - Changed ```Deploy.Product.NSXT.Federation.Enable``` references to ```Deploy.Product.NSXT.Federation.Deploy``` in ```config_sample.yml``` file to maintain consistency across all deployment products.
  - Changed ```Deploy.Product.NSXT.Federation.Enable``` references to ```Deploy.Product.NSXT.Federation.Deploy``` in all playbooks, templates, and tests.
  - Added additional check in ```playbooks/ValidateConfiguration.yml``` which verifies ```Deploy.Product.NSXT.LocalManager.Deploy``` must be ```True``` if ```Deploy.Product.NSXT.Federation.Deploy``` is set to ```True```.  This ensures GMs are not deployed without LMs also being deployed.
  - Be sure to update your ```config.yml``` file(s).

## Dev-v6.0.0 04-NOVEMBER-2023

### Added by Rutger Blom
  - Added a "Create" item to NSX-T segments in ```config_sample.yml``` to provide control over whether a segment is created or not.
  The following segments are now created conditionally:
    - NSX T0-Edge Uplink 1 segment - creation depends on whether NSX-T Edge will be deployed (Deploy.Product.NSXT.Edge.Deploy)
    - NSX T0-Edge Uplink 2 segment - creation depends on whether NSX-T Edge will be deployed (Deploy.Product.NSXT.Edge.Deploy)
    - ALB SE Management segment - creation depends on whether NSX ALB will be deployed (Deploy.Product.ALB.Deploy)
    - ALB SE Data segment - creation depends on whether NSX ALB will be deployed (Deploy.Product.ALB.Deploy)
  - Added top-level "if" statement to ```templates/vars_NSXT_Segments.j2``` so that the new "Create" item is evaluated.
  - Added vCenter Server v8.0.0 Update 2a to ```software_sample.yml``` file. (UNTESTED)
  - Be sure to update your ```config.yml```, ```software.yml``` , and ```templates.yml``` files.

## Dev-v6.0.0 05-NOVEMBER-2023

### Added by Rutger Blom
  - Updated the "Create" item to NSX-T segments in ```config_sample.yml``` to use existing value rather than computing a value.
  The following segments are now created conditionally:
    - ALB SE Management segment - creation depends on whether NSX ALB will be deployed (Deploy.Product.ALB.Deploy)
    - ALB SE Data segment - creation depends on whether NSX ALB will be deployed (Deploy.Product.ALB.Deploy)

## Dev-v6.0.0 05-NOVEMBER-2023

### Added by Luis Chanu
  - Corrected vCenter Server v8.00 Update 2A entry in ```software_sample.yml``` and ```templates_sample.yml``` files.
  - If you created the directory in your ```/Software``` repository, you will need to rename it.
  - Added ```BFD``` data structures to ```Nested_Router``` and ```Nested_NSXT```.  Not implemented yet, just preparation for future changes.
  - Updated software versions for various VMware products in ```config_sample.yml```.
  - Be sure to update your ```config.yml```, ```software.yml``` , and ```templates.yml``` files.

## Dev-v6.0.0 07-NOVEMBER-2023

### Added by Rutger Blom
  - Updated the ```Tanzu``` section within ```Nested_Cluster``` in ```config_sample.yml``` so that Tanzu Supervisor Ingress and Tanzu Supervisor Egress are assigned IP CIDRs from the NSX overlay address space (```Pod.BaseOverlay```).
  - Configured the correct Content Library to be used when installing Tanzu Supervisor in ```playbooks/EnableWorkloadManagement.yml```.
  - Be sure to update your ```config.yml``` file(s).