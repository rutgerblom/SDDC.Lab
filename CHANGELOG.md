# Changelog

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
- Corrected issue with license_vSphere.yml module where it would fail if a product didn't have licenses.

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

- Converted to Ansible FQCN in script "undeploy.yml"

## Dev-v3.0.0 11-APRIL-2021

### Added by Luis Chanu

- Modified ESXi syslog firewall rule entry to permit the server to source from all local IP addresses.

## Dev-v3.0.0 12-APRIL-2021

### Added by Luis Chanu

- Changes have been made to the Pod_Config.j2 template, so please re-run createPodConfig playbook against all of your config files.
- Support for "Legacy" VyOS image (v1.1.8) has been removed/deprecated.  All deployments must now use "Latest" for the Router version.  If you have existing configuration files that are using "Legacy", please be sure to update them.
- ValidateConfiguration.yml playbook updated to verify that the Router version is "Latest".
- Added "FileExt" to all "Software" entries via the Jinja2 template.  This has been added to simplify the ability for an installation process to determine if the installation source is "iso" or "ova".
- The following files were updated, so please update your non-sample files:
  - software_sample.yml
  - templates_sample.yml

## Dev-v3.0.0 13-APRIL-2021

### Added by Luis Chanu

- Added support in concurrent Pod deployment to support vCenter Server Replication Partners.
- Created new 'checkVcReplicationPartner.yml' playbook to verify Replication Partner vCenter Server is operational.  It pauses the Pod with the Replication Partner until the Replication Partner vCenter Server is operational.
- Added new 'checkVcReplicationPartner.yml' playbook to deploy.yml playbook.

## Dev-v3.0.0 14-APRIL-2021

### Added by Rutger

- Added a variable that controls the hardware version of the DNS server virtual machine. Default value is set to 13.
- The following file was updated so please update your non-sample file:
  - config_sample.yml

## Dev-v3.0.0 14-APRIL-2021

### Added by Luis Chanu

- Converted module references within deploy.yml to use FQCNs
- Correct issue with deployRouter.yml playbook where it would fail if router was already deployed

## Dev-v3.0.0 15-APRIL-2021

### Added by Rutger

- The generated Pod documentation will now contain information on whether NSX-T Edge was deployed or not.
- Converted module references within prepareISOInstaller.yml, deployVc.yml, and deployDNSServer.yml to use FQCNs (ansible.posix.mount).
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

- Modified createPodConfig.yml playbook to redisplay the Pod deployment command at the end of the playbook.
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

## v3.0.0 30-MAY-2021

### Added by Rutger Blom & Luis Chanu

- Released version 3 of the SDDC.Lab project.

## Dev-v4.0.0 13-JUNE-2021

### Added by Luis Chanu

- Updated FirstPod.MD file
- Updated utils/util_CreateConfig.sh
- Renamed all instances of "RouterUplink" to "Uplink" in config_sample.yml
- IMPORTANT: Please recreate static Pod-Config files using createPodConfig.yml
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
    - Module deployRouter.yml now not only deploys the VyOS router, but also performs basic configuration (Name, Eth0 IP Address, Floating default route, enable SSH).
    - Due to changing syntax of the VyOS "/config/config.boot" file with newer versions of VyOS, instead of creating that file and copying it to the VyOS router (as was previously done), we now develop the individual VyOS "SET" commands for the target configuration, then send those commands to the provisioned VyOS router.  Once that's done, we then 'commit' and 'save' the configuration.  The creation of the VyOS router configuration is performed by the new configureRouter.yml playbook.
    - Added a pre-login message that shows the VyOS router name, along with a reminder that the login username is "vyos".
    - As a precaution, previous "deployRouter.yml" and "vyos_router.j2" files have been renamed to *_OLD, respectively.  They will be removed once the new VyOS router deployment has been throughly tested.

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

  - Corrected missing "{" for annotation variable in deployRouter.yml
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
  - The config_sample.yml file was updated so please update your non-sample configuration files, then rerun the createPodConfig.yml playbook to regenerate your static configuration files.

## Dev-v4.0.0 16-JULY-2021

### Added by Luis Chanu

  - Created test module "tests/updateDNSVIP.yml" module to populate NSX-T VIP entries into DNS.  This module is working, and the code is ready to be integrated into the two modules with touch DNS records.

## Dev-v4.0.0 17-JULY-2021

### Added by Luis Chanu

  - Integrated DNS VIP code into both "updateDNS.yml" and "cleanupDNS.yml" playbooks.  Tested both playbooks, and they completed without any issues.  Verified using utils/showdns that the NSX-T Global Manager and Local Manager VIPs were populated in DNS.

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
  - After updating your non-sample configuration files, be sure to recreate your static Pod configuration files by running "createPodConfig.yml" against each of the updated config files.

## Dev-v4.0.0 24-JULY-2021

### Added by Luis Chanu

  - Modifed createVds.yml to prune VLAN ID range on NSXEdgeUplink1 and NSXEdgeUplink2 uplinks to the VLAN ID range of the Pod being deployed.  Previously, it was allowing all VLANs (0-4094).

## Dev-v4.0.0 25-JULY-2021

### Added by Luis Chanu

  - Enabled OSPFv2 on Pod-Router NSX-T Edge facing interfaces (NSXEdgeUplink1 and NSXEdgeUplink2).
  - Moved OSPFv2 area configuration information below interface sections in Nested_Router.
  - OSPFv2 configuration was not added to NSX-T's Tier-0 Gateway within the configuration file.  If the user wants to configure OSPFv2 within NSX-T, they will have to do it manually.  There are currently no plans to add OSPFv2 configuration to the SDDC.Lab project given BGP is fully functional, supports IPv6, and is the protocol used by Federation.
  - The following file was updated so please update your non-sample file:
    - config_sample.yml
  - After updating your non-sample configuration files, be sure to recreate your static Pod configuration files by running "createPodConfig.yml" against each of the updated config files.

## Dev-v4.0.0 21-AUG-2021

### Added by Luis Chanu

  - Renamed playbooks\deployNsxManager.yml to playbooks\deployNsxLocalManager.yml to prepare for the development of Global Manager specific playbooks.
  - Updated deploy.yml with updated deployNsxLocalManager.yml playbook.

## Dev-v4.0.0 22-AUG-2021

### Added by Luis Chanu
  - Began development on playbooks\deployNsxGlobalManager.yml
  - Updated the following files to support changes to Deploy.Product.NSXT.GlobalManager structure
    - templates\Pod_Config.j2
    - tempaltes\Pod_Doc.j2
  - The following file was updated so please update your non-sample file:
    - config_sample.yml
  - After updating your non-sample configuration files, be sure to recreate your static Pod configuration files by running "createPodConfig.yml" against each of the updated config files.

## Dev-v4.0.0 23-AUG-2021

### Added by Luis Chanu
  - Added removal of Global Manager to undeploy.yml playbook

  ## Dev-v4.0.0 25-AUG-2021

### Added by Luis Chanu
  - Added task to enable and activate Global Manager within deployNsxGlobalManager.yml
  - Created "tests/ShowURI.yml" playbook
  - Began working on "registerNsxLocalWithNsxGlobal.yml" playbook
  