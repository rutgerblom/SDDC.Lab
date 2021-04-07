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

