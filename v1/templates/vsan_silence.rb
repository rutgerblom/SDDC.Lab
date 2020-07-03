# Rutger Blom
# www.rutgerblom.com
# RVC script for silencing vSAN warnings

vcenter_name = "{{ vcenter.fqdn }}"
datacenter_name = "{{ vcenter.datacenter }}"
cluster_name = "{{ item.key }}"


puts "Silence vSAN warnings"
rvc_exec("vsan.health.silent_health_check_configure -a controllerdiskmode #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a controllerdriver #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a controllerfirmware #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a controllerreleasesupport #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a controlleronhcl #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a autohclupdate #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a hcldbuptodate #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a releasecataloguptodate #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a perfsvcstatus #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a smalldiskstest #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a vsanenablesupportinsight #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
rvc_exec("vsan.health.silent_health_check_configure -a vumconfig #{vcenter_name}/#{datacenter_name}/computers/#{cluster_name}")
