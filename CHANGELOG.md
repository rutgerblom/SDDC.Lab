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