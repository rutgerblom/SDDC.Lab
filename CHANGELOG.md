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
  - Moved NSX-T Local Manager licensing playbook immediately after it's deployment in deploy.yml
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
  - Renamed playbooks/registerNsxLocalManager.yml to playbooks/federateNsxLocalManager.yml
  - Added the following playbooks to deploy.yml:
    - configureNsxBackup.yml
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
  - Added conditional to updateDNS.yml to only populate Global Manager records in DNS if the deploying SiteCode == Global Manager SiteCode.  It should be noted that the conditional was NOT added to cleanupDNS.yml, as they should always be removed if present.
  - Originally, Deploy.Product.NSXT.GlobalManager.Deploy was used to signify if GM was being deployed.  That has now been changed, and now Deploy.Product.NSXT.Federation.Enable is used.  If it is set to True, then when the deployment SiteCode matches the GlobalManager.SiteCode, the Global Manager is deployed.
  - Modify EULA structure for Nested_NSXT
  - Added automated EULA acceptance to the NSX-T Global and Local Manager deployment playbooks.  EULA must be accepted in the config.yml file (under Nested_NSXT.Question.EULA)
  - The following file(s) were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 10-OCT-2021

### Added by Luis Chanu
  - Changes made to the configureNsxBackup.yml playbook, and it appears to be functioning properly.
  - Added comments to playbook to document what backups are created, and which ones are run.
  - Additional changes to federateNsxLocalManager.yml...still work in progress.
  - Enabled configureNsxBackup.yml in deploy.yml.

## Dev-v4.0.0 11-OCT-2021

### Added by Luis Chanu
  - Changed expected "ready" state for GlobalManager in deployNsxGlobalManager.yml from "NONE" to "ACTIVE".
  - Increased delay before VIP in an attempt to address a race condition.
  - Modified deploy.yml to support the following:
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
  - Made slight modifications to federateNsxLocalManager.yml around order of operations and delays
  - Began developing federateNsxEdgeNodes.yml playbook to make the necessary changes to the Edge Nodes for Federation.  Initial thoughts on tasks include:
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
  - Modified deployNsxLocalManager.yml to include task to automatically answer CEIP.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 27-OCT-2021

### Added by Luis Chanu
  - In federateNsxLocalManager.yml, doubled length of time we'll loop to see if Global Manager is ready from 1 hour to 2 hours.
  - Updated deployNsxLocalManager.yml to obtain current _revision number for CEIP config and telemetry settings
  - To determine if Pod-Router VM is actually powered off, replaced timer with module to query VM state
  
## Dev-v4.0.0 28-OCT-2021

### Added by Luis Chanu
  - The "SEG-Example-Complicated-VLAN-Segment" segment was deleted from sample_config.yml to remove collisions during Federation onboarding. 
  - Changed few tasks in deployNsxGlobalManager.yml to use FQDN instead of IPv4 address
  - Removed "lower" filters from deployNsxLocalManager.yml playbook
  - Modified deployNsxGlobalManager and deployNsxLocalManager playbooks to use NSX-T REST API with a verification loop to configure VIPs rather than NSX-T Ansible Module
  - Modified deployNsxLocalManager to use NSX-T LM VIP rather than appliance IP's after VIP is configured
  - Added vCenter Server v7.0 Update 3A to software repository
  - The following files were updated so please update your non-sample files:
    - config_sample.yml
    - software_sample.yml
    - templates_sample.yml

## Dev-v4.0.0 31-OCT-2021

### Added by Luis Chanu
  - Created tests/TestFailure.yml playbook to test various failure handling scenarios
  - Many changes to federateNsxLocalManager.yml playbook:
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
  - Added filter in deployNsxLocalManager.yml and deployNsxGlobalManager.yml to force 'Deployment Size' to lower as a safety net in case user accidentally changes case.  OVFTool requires Size to be in lower case.
  - Added 'upper' filter in templates/vars_NSXT_EdgeTransportNodes.j2 to ensure FormFactor sizing is always in upper case, as required by the NSX-T API.
  - Modified createNsxEdgeTn.yml to disable password expiration for all users on NSX-T Edges
  - Modified deployNsxLocalManager.yml and deployNsxGlobalManager.yml to also disable password expiration for 'root' user
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
  - Added code to federateNsxEdgeNodes.yml which:
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
  - Added playbooks/configureNsxFabricMTU.yml to project
  - Added configureNsxFabricMTU.yml to deploy.yml
  - NSX-T Global Fabric MTU settings are now configured to match the values defined in Net.Transport.MTU and Net.RTEP.MTU.  Make sure these values supported by your physical networking environment.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 23-NOV-2021

### Added by Luis Chanu
  - Added BGP Neighbor description to vars_NSXT_T0Gateways.j2 template.
  - Added federateNsxT0BGPNeighbors.yml playbook to project, which configures BGP Neighbors to the stretched Tier-0 Gateway.
  - Added federateNsxT0RouteReDist.yml playbook to project.  This handles configuration of Tier-0 Gateway Route Re-Distribution on non-GM SiteCodes.
  - Added federateNsxT0RouteReDist.yml playbook to deploy.yml.
  - Corredted issue with T0Edges variable.
  - Increased time on some loops to support large deployments.
  - In config_sample.yml, changed Tier-0 Gateway Locale-Service from "T0-Gateway-01_Locale_Service" to "{{ SiteCode }}" to aid with Federation automation.
  - Added federateNsxT0BGPNeighbors.yml to deploy.yml
  - Removed 'EdgeTransit' field from all NSX-T Segments in the config_sample.yml file as it is not used.
  - Renamed 'SEG-Example-Overlay-Without-VLANS' segment to 'SEG-Example-Tier0-Overlay-Segment' to better describe its existance/purpose.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 24-NOV-2021

### Added by Luis Chanu
  - Where applicable, playbooks were updated to use Local Manager and Global Manager VIPs instead of direct appliance IP
  - Added task to end of validateConfiguration.yml playbook to recursively delete /tmp/{{ SiteCode }} directory

## Dev-v4.0.0 26-NOV-2021

### Added by Luis Chanu
  - Updated 'createContentLibrary.yml' file implemented which supports additional functionality, including the ability to subscribe to remotely publised content libraries.
  - Updated config_sample.yml configuration file with additional Content Library variables to support the additional functionality
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 21-DEC-2021

### Added by Luis Chanu
  - As the sample_config.yml file has changed over time, the amount of time it takes for createPodConfig.yml to complete is increasing.  Latest testing shows it's now taking just over 2 hours to complete.  You can run multiple in parallel without issue.  We are looking into this, but for now, that's how long to expect.
  - Updated verbiage in createPodConfig.yml on how long it takes to create the static Pod-XXX-Config.yml file.
  - Added Deploy.Product.NSXT.GlobalManager.PodNumber variable to support Federation, as a stretched Tier-0 uses the same ASN across all sites.
  - Added the following updated products to software_sample.yml:
    - NSX-T v3.2.0 (Untested)
    - vRealize Log Insight v6.4.1 (Untested)
  - The following files were updated so please update your non-sample files:
    - config_sample.yml
    - software_sample.yml

## Dev-v4.0.0 23-DEC-2021

### Added by Luis Chanu
  - Modified createPodConfig.yml to include additional fields in created static Pod Config filename.  Those fields are:
    - VCSA version (VCSAvXXXXX) where XXXXX is VCSA version
    - NSXT version (NSXTvYYYYY) where YYYYY is NSX-T version
    - Fed-Z where Z is either Y or N, and indicates whether the Pod Configuration has NSX-T Federation deployment enabled or not

## Dev-v4.0.0 24-DEC-2021

### Added by Luis Chanu
  - **IMPORTANT**: As part of NSX-T Federation, NSX-T v3.2.0 appears to not support importing objects from a Location into the Global Manager.  For this reason, SDDC.Lab can not be used to deploy Federation when deploying NSX-T v3.2.0, as SDDC.Lab utilizes this functionality.  The workaround to this is to deploy Federation using NSX-T v3.1.3.3, then manually upgrade the Pods to v3.2.0.  It's assumed that this functionality will be re-introduced in a later release.  Standalone (i.e. Non-Federated) deployments of NSX-T v3.2.0 has been tested, and works fine.
  - NSX-T v3.2.0 Federation details added to README.md file
  - NSX-T v3.2.0 takes MUCH longer to set the "password_change_frequency" on an Edge Transport Node users than it did under NSX-T v3.1.3.3.  For this reason, the timeout on the task that performs this operation within "createNsxEdgeTn.yml" playbook has been increased from 15 to 60 seconds.
  - NSX-T Version Tested Status:
    - v3.1.3.3: Standalone and Federation
    - v3.1.3.5: We are still looking into an issue when deploying against this version.  Until further testing has been done, please do not deploy directly to this version...use v3.1.3.3 instead, then manually upgrade to v3.1.3.5.
    - v3.2.0:   Standalone only (See 'IMPORTANT' comment above)
  - Manually edited Ansible module "nsxt_fabric_compute_managers.py" to incorporate a change that was made in the VMware NSX-T Ansible modules to support Compute Manager registartion under NSX-T v3.2.0.
  - The "var_NSXT_EdgeTransportNodes.j2" template has been updated to support v3.2.0.  These changes have also been tested against v3.1.3.3, and deployed fine.
  - Modified "createPodConfig.yml" to append the Global Manager Pod to the end of the filename if Federation is enabled.
  - The following playbooks have been modified to support NSX-T v3.2.0:
    - createNsxEdgeTn.yml
    - createNsxTz.yml

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
  - Modified createNsxEdgeCluster.yml play to address the flapping of EdgeVM state when the user password aging is disabled.
  - The following deployment scenarios completed successfully:
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.1.3.3 (2-Site Federation)
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.1.3.5 (Standalone)
    - VCSA v7.00U3A, ESXi 7.00U3, NSX-T v3.2.0   (Standalone)

## Dev-v4.0.0 27-DEC-2021

### Added by Luis Chanu
  - Created utils/util_ApplyConfigToTemplate.yml playbook to be able to test any template quickly.  Modify the variable within to indicate what template you want to have it generate.
  - Began working on createNsxDhcpProfiles.yml playbook to create DHCP Server and DHCP Relay profiles.
  - Added Nested_NSXT.Networking.DHCPProfiles section to config_sample.yml.
  - The following files were updated so please update your non-sample files:
    - config_sample.yml

## Dev-v4.0.0 28-DEC-2021

### Added by Luis Chanu
  - Following changes were made to createNsxEdgeTn.yml playbook:
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
  - Created "deployWorkloadVms.yml" playbook to deploy Workload VM Templates (VM or OVF) from the Content Library after Pod deployment
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
  - Modify createNsxEdgeCluster.yml and vars_NSXT_EdgeClusters.j2 to permit creation of Edge Clusters without any member Edge Nodes.

## Dev-v4.0.0 11-JANUARY-2022

### Added by Luis Chanu
  - Added UplinkTeamingPolicy to Nested_NSXT.Networking.Segments data structure in config_sample.yml
  - Modified createNsxVLANSegments.yml to now apply Uplink Teaming Policy to VLAN Segments.  If UplinkTeamingPolicy is set to "" or not defined, it will default to using the Default teaming policy.
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
  - Updated preparePhysical.yml to remove deprecated and add required parameters to community.vmware.vmware_dvs_portgroup tasks

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
  - In validateConfiguration.yml, changed DIG target from ```www.google.com``` to ```github.com``` because it was oberved that ipaddr returns ```False``` when multiple A records are returned.
  - Change permissions set within ```util_CreateSoftwareDir.yml``` from 775 to 777 to ensure non-root user can update the software repsoritory.
  - Modified ```util_CreateSoftwareDir.yml``` to set 777 permissions to top-level RootDirectory (/Software) directory as well.
  - Enabled ```deployWorkloadVMs.yml``` task in ```deploy.yml```.

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
  - Moved configuring NTP on nested ESXi hosts from kickstart file to an Ansible task in "configureNestedEsxi.yml". 

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


## Dev-v5.0.0 6-APRIL-2022

### Added by Luis Chanu
  - Begin developing version 5.0 in branch ```dev-v5```

## Dev-v5.0.0 10-APRIL-2022

### Added by Rutger Blom
  - Fixed an issue with the port groups not being removed when running "undeploy.yml".

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
  - Added the active uplinks teaming policy parameter to vmware_dvs_portgroups tasks in ```createVds.yml```. Active uplink configuration is stored in the Nested_vCenter dictionary in ```config_sample.yml```.
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
  - Changed /Software directory permissions from 0777 to 0775 in ```util_CreateSoftwareDir.yml```
  - Changed NSX-T version to v3.1.3.6 in ```config_sample.yml```
  - Cleaning up minor spacing issues in ```config_sample.yml```
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 14-APRIL-2022

### Added by Rutger Blom
  - Added the standby uplinks teaming policy parameter to vmware_dvs_portgroups task in ```createVds.yml```. Standby uplink configuration is stored in the Nested_vCenter dictionary in ```config_sample.yml```.
  - Modified the standby uplinks of port groups NSXEdgeUplink1 and NSXEdgeUplink2 in ```config_sample.yml``` so that these use only Uplink 2 and Uplink 1 respectively. This to facilitate failover of Geneve traffic in case of a ToR failure. Although this failure scenario is not likely in a nested lab, we want to mirror configuration of a production environment whereever we can. 
  - Updated ```createVds.yml``` to loop over the port groups rather than having one task for each port group object.
  - Added network policy parameters (forged_transmits, mac_changes, promiscuous) to the vmware_dvs_portgroups task in ```createVds.yml```. Network policy configuration is stored in the Nested_vCenter dictionary in ```config_sample.yml```.
  - The parameters num_ports and port_binding used by the vmware_dvs_portgroups task in ```createVds.yml``` now fetch their values from the Nested_vCenter dictionary in ```config_sample.yml``` (instead of having them hard-coded in the Playbook).
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 21-APRIL-2022

### Added by Rutger Blom
  - Replaced the ```ansible.posix.mount``` task in the ```playbooks/prepareISOInstaller.yml``` playbook with a ```ansible.builtin.command```task running ```7z``` to extract the contents of the ESXi ISO file. The ```ansible.posix.mount``` task requires root or CAP_SYS_ADMIN privileges which is something we want to eliminate in the upcoming version.
  - Added a new variable to the ```TargetConfig``` dictionary in ```config_sample.yml``` called ```ISOExtract``` which is used by the ```playbooks/prepareISOInstaller.yml``` playbook
  - The 7Zip software package is now required so updated the ```README.md``` with this requirement. 
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 22-APRIL-2022

### Added by Rutger Blom
  - Added variable ```WorkingFolder``` to the ```TargetConfig``` dictionary in ```config_sample.yml```. The location of ```WorkingFolder``` is used for temporary files created during the Pod deployment process. The variable's default value is ```"{{ lookup('env','HOME') }}/SDDC.Lab/{{ SiteCode }}"```. Eventually ```WorkingFolder``` will replace or be renamed to variable ```TempFolder```. This will be done once all playbooks have been updated to make use of the new location.
  - Updated playbook ```playbooks/prepareISOInstaller.yml``` to use the new ```WorkingFolder``` variable.
  - Please be sure to update your ```config.yml``` file

## Dev-v5.0.0 23-APRIL-2022

### Added by Rutger Blom
  - Replaced the ```ansible.posix.mount``` task in the ```playbooks/deployDNSServer.yml``` playbook with a ```ansible.builtin.command```task running ```7z``` to extract the contents of the Ubuntu ISO file. The ```ansible.posix.mount``` task requires root or CAP_SYS_ADMIN privileges which is something we want to eliminate in the upcoming version.
  - Updated playbook ```playbooks/deployDNSServer.yml``` and the associated template files to use the new ```WorkingFolder``` variable.
  - Added a task to ```playbooks/deployDNSServer.yml``` that conditionaly (```DEBUG.KeepInstallerFiles != true```) deletes the local ISOExtractPoint directory
  - Added a task to ```playbooks/prepareISOInstaller.yml``` that conditionaly (```DEBUG.KeepInstallerFiles != true```) deletes the local ISOExtractPoint directory

## Dev-v5.0.0 24-APRIL-2022

### Added by Rutger Blom
  - Replaced the ```ansible.posix.mount``` task in the ```playbooks/deployVc.yml``` playbook with a ```ansible.builtin.command```task running ```7z``` to extract the contents of the vCenter ISO file. The ```ansible.posix.mount``` task requires root or CAP_SYS_ADMIN privileges which is something we want to eliminate in the upcoming version.
  - A non-critical error occurs when 7z extracts vCenter ISO files so added the ```ìgnore_errors: true```parameter to the task.
  - Updated playbook ```playbooks/deployVc.yml``` to use the new ```WorkingFolder``` variable.
  - Added a task to ```playbooks/deployVc.yml``` that conditionaly (```DEBUG.KeepInstallerFiles != true```) deletes the local ISOExtractPoint directory.

## Dev-v5.0.0 24-APRIL-2022

### Added by Rutger Blom
  - Updated variable ```TempFolder``` with new value in ```config_sample.yml``` as it replaces variable ```WorkingFolder```.
  - Removed variable ```ISOMount``` from ```config_sample.yml``` as it is not used anymore.
  - Removed variable ```WorkingFolder``` as it is not used anymore.
  - Updated documentation as well as comments in playbooks as Pod deployments can now be performed without using ```sudo``` e.g. ```ansible-playbook -e "@~/Pod-XXX-Config.yml" deploy.yml```.
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
  - Added "Ignore Fatal Error Message" to "Extract vCenter ISO" task in ```playbooks/deployVc.yml``` playbook.
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
  - Removed the "num_ports" parameter from "community.vmware.vmware_dvs_portgroup" tasks in ```playbooks/preparePhysical.yml```. This to prevent an error when re-running a failed/broken off deployment and "num_ports" on the distributed port group has increased beyond specified by "num_ports" (we cannot decrease num_ports if ports are in use).

## Dev-v5.0.0 26-JULY-2022

### Added by Luis Chanu
  - All newly added software versions listed below is UNTESTED
  - Added vCenter Server v7.0.0 Update 3F & 3G to ```software_sample.yml``` and ```templates_sample.yml``` files.
  - Added ESXi v7.0.0 Update 3F to ```software_sample.yml``` and ```templates_sample.yml``` files.
  - Added NSX-T v3.2.1.1 to ```software_sample.yml``` file.

## Dev-v5.0.0 29-JULY-2022

### Added by Luis Chanu
  - In Ansible module ```enableWorkloadManagement.yml```, noticed that the data structure used to enable Workload Managmenet (a.k.a. Tanzu) had extra escapes in it.  After investigating, appeared to be cause by extra JSON conversion in module.
  - Removed extra "| to_json" in last play in the ```enableWorkloadManagement.yml``` module.
  - Added additional DEBUG play to display data structure when debugging is enabled.
  - Removed extra space from ContentLibrary section of ```config_sample.yml``` file.

## Dev-v5.0.0 31-JULY-2022

### Added by Luis Chanu
  - Removed extra spaces from Nested_Cluster section of ```config_sample.yml``` file.
  - Noticed an issue where if more than 1 vSphere Cluster was configured to be prepared by NSX, only one vSphere cluster would end up being prepared.  Corrected the issue by making the transport node collection display name be unique for each cluster by including the cluster name in the TNC display name field within ```attchNsxTnp.yml```.
  - Added "ignore_errors: true" to Port-Group removal plays in ```undeploy.yml``` file.

## Dev-v5.0.0 02-AUGUST-2022

### Added by Rutger Blom
  - Added NSX-T v4.0.0.1 to ```software_sample.yml``` file.