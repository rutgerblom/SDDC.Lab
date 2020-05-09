# Changelog

## 1.2.6

### Added

- Variable "router_version" to control which version of VyOS wil be deployed.
- With "router_version == latest" (default) the "management" VIF will listen for NTP queries.
- Changelog moved from README.md to CHANGELOG.md

### Changed

- vSAN configuration now working
- vSAN enabled on clusters (answerfile_sample.yml)
- IP addresses of vCenter, NSX Manager, and Edge vESXi hosts (answerfile_sample.yml)
- Host names of the vESXi hosts (answerfile_sample.yml)

## 1.2.5

### Added

- Variable "pod" for easier deployment with less configuration to fill out.
- vESX now has a "cores" variable so the user can better control CPU sockets and cores of the virtual ESXi host.
- The default vESXi host configuration now has 2 CPU sockets instead of 8.
- "VM Network" VLAN for virtual machine networking within the nested environment.
- The VyOS router provides a DHCP service for the "VM Network" VLAN.
- The "ntp1" variable is now used in the VyOS configuration as well.
- A default route is now configured on the VyOs router using the new "router_default_gw" variable.

### Changed

- vMotion VMkernel adapter is now created on the vMotion TCP/IP stack.
- The "dns2" variable is now used when DNS is configured on the nested ESXi hosts. 
- Improved format and structure for the answerfile for better readibility.
- The "answerfile.yml" has been renamed to "answerfile_sample.yml" to prevent overwriting of the user's local "answerfile.yml" (see [Usage](#Usage)).

## 25/04/2020

### Added

- An optional VyOS router to the deployment.

## 12/04/2020

- Initial release