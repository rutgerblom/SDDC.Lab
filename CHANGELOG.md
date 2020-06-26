# Changelog

## TBD 26-JUNE-2020 by Rutger Blom

### Changed

- Added Python 'interpreter_python = /usr/bin/python3' to ansible.cfg (Thanks Luis).
- Changes to 'hosts/hosts' so warnings about inventory are suppressed.

## TBD 9-JUNE-2020 by Rutger Blom

### Changed

- Hard coded timer for ESXi installation has been replaced with a polling loop.

## 1.2.9.2 6-JUNE-2020 by Rutger Blom

### Added

- Pod documentation generated and saved to "~/pod-{{ pod }}.html".

### Changed

- Replaced most hard coded timers (pauses) with API polling (using uri) in the NSX-T deployment playbooks. 
- Added conditionals to "deployVc.yml" for idempotency.
- Added "ignore_errors" to "configureVsan.yml" for idempotency.
- FQDN for NSX Manager changed to "pod-{{ pod }}-{{ nsxmanager_name }}.{{ domain }}" so it's compliant with pod naming standard.
- Added clarifications and additional information under "Requirements" in "README.md"
- Disabled some more vSAN health checks that do not make sense in a nested environment
- Changed the default value of "vcIso" to match the latest vCenter 7.0 version 

## 1.2.9.1 25-MAY-2020 by Rutger Blom

### Changed

- FQDN for vCenter changed to "pod-{{ pod }}-vcenter.{{ domain }}" so it's compliant with the pod naming standard.
- FQDN for Edge nodes changed to "pod-{{ pod }}-en0x" so it's compliant with pod naming standard.

## 1.2.9 21-MAY-2020 by Rutger Blom

### Changed

- The VyOS configuration templates have been consolidated into one template using jinja conditional statements for the different versions.
- The NSX-T Tier-0 gateway is now configured with four external interfaces and two BGP neighbors leveraging "nsx_edge_uplink_2".
- The VyOS router is now configured with four BGP neighbors leveraging "nsx_edge_uplink_2".

## 1.2.9 19-MAY-2020 by Luis Chanu

### Added

- Support for Vyos router to peer with physical environment over OSPFv2 to share internal routes.  This removes the need to install static routes.
- Ansible modules are now requiring the netaddr library, which can be added via "pip3 install netaddr" on the Ansible control station.
- Added small "router" data structure into answerfile_sample.yml to provide required dynamic routing informaiton.
- Added Jinja2 conditional logic around OSPF and Static configuration so that only the requested configuration is deployed.
- New variable called "router.protocol" controls if deployment uses static routing or OSPF. Variable is set to either "static" or "ospf".

### Changed

- Answerfile_sample.yml variable values were modified to align configuration with "standard" OSPF deployment testbed.
- Modified BGP "router-id" value so that the 3rd octet matches the Pod #, making it easier to identify.
- Set the OSPF "router-id" value to match the IP address of the uplink Vyos router interface, thus making it easier to identify which Vyos instance an entry is referring to from the OSPF process running on the physical lab switch.

## 1.2.8 15-MAY-2020 by Rutger Blom

### Added
 
- Added tasks in the vSAN configuration playbook that silence vSAN warnings

### Changed

- NSX-T Edge nodes are now by default deployed on vSAN storage instead of NFS
- Changed the default value of "use_nfs" to "false" in answerfile_sample.yml
- Updated the diagrams in README.md so that these accurately reflect what is deployed using the default settings

## 1.2.7 10-MAY-2020 by Luis Chanu

### Added

- Created new "nsxt_edge_uplink_1" and "nsxt_edge_uplink_2" networks (for future use)
- Created additional "xxx_netmask_cidr" variables to replace hard coded masks found in script
- Added new segments, includng IP storage and SVM Management, to prepare the lab for additional functionality that a lab user might want
- Added vmk3 on nested vSphere hosts for IP Storage (should lab user need it) 

### Changed

- Modified nested VM naming to use Pod-###-<vm>
- Changed hard coded cidr subnets to "xxx_netmask_cidr" variables in template files
- To preare for NSX-T Global Manager available in v3.0, renamed NSXManager01 to "NSXT-LM", as it's now called the Local Manager
- Changed segment offset values

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
- Miscellaneous fixes

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
