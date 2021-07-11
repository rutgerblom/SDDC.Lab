#!/bin/bash

# Print banner
clear
base64 -d <<<"IF9fX19fX19fX19fX19fX19fICBfX19fXyAgICAgICBfICAgICAgICAgICBfICAgICAgICAgICAgICAgX19fIA0KLyAgX19ffCAgXyAgXCAgXyAgXC8gIF9fIFwgICAgIHwgfCAgICAgICAgIHwgfCAgICAgICAgICAgICAvICAgfCAgICAgICAgICAgICAgICAgRGV2ZWxvcGVkIEJ5DQpcIGAtLS58IHwgfCB8IHwgfCB8fCAvICBcLyAgICAgfCB8ICAgICBfXyBffCB8X18gICBfXyAgIF9fLyAvfCB8ICAgICAgICAgIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tDQogYC0tLiBcIHwgfCB8IHwgfCB8fCB8ICAgICAgICAgfCB8ICAgIC8gX2AgfCAnXyBcICBcIFwgLyAvIC9ffCB8ICAgICAgICAgIFJ1dGdlciBCbG9tICAmICBMdWlzIENoYW51DQovXF9fLyAvIHwvIC98IHwvIC8gfCBcX18vXCAgXyAgfCB8X19ffCAoX3wgfCB8XykgfCAgXCBWIC9cX19fICB8ICAgICAgICAgIE5TWCB2RXhwZXJ0ICAgICBWQ0RYICMyNDYNClxfX19fL3xfX18vIHxfX18vICAgXF9fX18vIChfKSBcX19fX18vXF9fLF98Xy5fXy8gICAgXF8vICAgICB8Xy8NCg=="
echo
echo

# Gather input
read -p "Enter the full path to "config_sample.yml" file [$HOME/SDDC.Lab/config_sample.yml]: " sourcepath
read -p "Enter the full path to where you want to save the "config.yml" file [$HOME/SDDC.Lab/config.yml]: " destinationpath
read -p "Enter a Pod Number between 10 and 240 [240]: " podnumber
read -p 'Enter the deployment target. Valid options are "Host" or "vCenter" [Host]: ' target
if [[ $target == 'vCenter' ]] ; then
    read -p 'Enter the vCenter administrator password [VMware1!]: ' physicalpassword
else
    read -p 'Enter your ESXi root password [VMware1!]: ' physicalpassword
fi
read -p 'Enter the IP address of your DNS server [10.203.0.5]: ' dnsserver
read -p 'Enter the IP address of your NTP server [10.203.0.5]: ' ntpserver
if [[ $target == 'vCenter' ]] ; then
    read -p 'Enter the FQDN of your vCenter server [NetLab-vCenter.NetLab.Local]: ' fqdn
else
    read -p 'Enter the FQDN of your ESXi host [Host32.NetLab.Home]: ' fqdn
fi  
if [[ $target == 'vCenter' ]] ; then
    read -p 'Enter the name of the DataCenter object under which the Pods will be deployed [SDDC]: ' datacenter
    read -p 'Enter the name of the Cluster within the Datacenter the Pods will be deployed [Lab-Cluster ]: ' cluster
fi
read -p 'Enter the name of the Datastore where the Pod VMs will be stored [Shared_VMs]: ' datastore
read -p 'Enter the name of the Portgroup that connects your Pod to the physical network (e.g. transit segment) [Lab-Routers]: ' portgroup
read -p 'Enter the routing protocol to be used for routing between your Pod and the physical network. Valid options are "Static", "BGP", "OSPF" or "BOTH" (OSPF and BGP) [BOTH]: ' routing

# Populate the variables with default values if empty
sourcepath=${sourcepath:-$HOME/SDDC.Lab/config_sample.yml}
destinationpath=${destinationpathpath:-$HOME/SDDC.Lab/config.yml}
podnumber=${podnumber:-240}
physicalpassword=${physicalpassword:-VMware1!}
dnsserver=${dnsserver:-10.203.0.5}
ntpserver=${ntpserver:-10.203.0.5}
if [[ $target == 'vCenter' ]] ; then
    fqdn=${fqdn:-NetLab-vCenter.NetLab.Local}
else
    fqdn=${fqdn:-Host32.NetLab.Home}
fi
target=${target:-Host}
datacenter=${datacenter:-SDDC}
cluster=${cluster:-Lab-Cluster}
datastore=${datastore:-Shared_VMs}
portgroup=${portgroup:-Lab-Routers}
routing=${routing:-BOTH}


# Check that Pod number is an integer and that it's between 10 and 240
case "$podnumber" in
    ("" | *[!0-9]*)
        echo
        echo 'Pod Number should be a number. Please try again.' >&2
        echo
        exit 0
        ;;
    *)
        if [[ "$podnumber" -lt 10 ]] || [[ "$podnumber" -gt 240 ]] ; then
            echo
            echo 'Pod Number should be a number between 10 and 240. Please try again.' >&2
            echo
            exit 0
        fi
esac

# Display the entered values to the user
echo
echo "You've entered the following settings:"
echo
echo -e "Path to "config_sample.yml": \033[33m$sourcepath\033[0m"
echo -e "Path to "config.yml": \033[33m$destinationpath\033[0m"
echo -e "Pod Number: \033[33m$podnumber\033[0m"
echo -e "Deployment target: \033[33m$target\033[0m"
if [[ $target == 'vCenter' ]] ; then
    echo -e "vCenter administrator password: \033[33m$physicalpassword\033[0m"
else
    echo -e "ESXi root password: \033[33m$physicalpassword\033[0m"
fi
echo -e "DNS server: \033[33m$dnsserver\033[0m"
echo -e "NTP server: \033[33m$ntpserver\033[0m"
if [[ $target == 'vCenter' ]] ; then
    echo -e "vCenter FQDN: \033[33m$fqdn\033[0m"
else
    echo -e "ESXi FQDN: \033[33m$fqdn\033[0m"
fi
if [[ $target == 'vCenter' ]] ; then
    echo -e "DataCenter object: \033[33m$datacenter\033[0m"
    echo -e "Cluster object: \033[33m$cluster\033[0m"
fi
echo -e "Datastore: \033[33m$datastore\033[0m"
echo -e "Portgroup: \033[33m$portgroup\033[0m"
echo -e "Routing protocol: \033[33m$routing\033[0m"
echo

# Continue or exit?
read -p "Do you want to create a configuration file with these values (y/n)?" choice
if [[ $choice =~ ^[Yy]$ ]] ; then

    # Copy "config_sample.yml" to the user specified configuration file
    cp $sourcepath $destinationpath
 
    # Update config.yml with the user supplied settings 
    sed -i -e "19s/Number: 240/Number: $podnumber/g" $destinationpath
    sed -i -e "99s/Physical: VMware1\!/Physical: $physicalpassword/g" $destinationpath
    sed -i -e "104s/IPv4: \"{{ Net.Uplink.IPv4.Network }}.5\"/IPv4: $dnsserver/g" $destinationpath
    sed -i -e "111s/IPv4: \"{{ Net.Uplink.IPv4.Network }}.5\"/IPv4: $ntpserver/g" $destinationpath
    sed -i -e "136s/Deployment: Host/Deployment: $target/g" $destinationpath
    
    # Check deployment target so that we update "FQDN" at the right line number
    if [[ $target == 'Host' ]] ; then
        sed -i -e "138s/FQDN: Host32.NetLab.Home/FQDN: $fqdn/g" $destinationpath
    else
        sed -i -e "160s/FQDN: NetLab-vCenter.NetLab.Local/FQDN: $fqdn/g" $destinationpath
    fi
    
    # Update "DataCenter" and "Cluster" only when the deployment target is vCenter
    if [[ $target == 'vCenter' ]] ; then
        sed -i -e "165s/DataCenter: SDDC/DataCenter: $datacenter/g" $destinationpath
        sed -i -e "166s/Cluster: Lab-Cluster/Cluster: $cluster/g" $destinationpath
    fi
    
    # Check deployment target so that we update "Datastore" at the right line number
    if [[ $target == 'Host' ]] ; then
        sed -i -e "145s/Datastore: Local_VMs/Datastore: $datastore/g" $destinationpath
    else
        sed -i -e "167s/Datastore: Shared_VMs/Datastore: $datastore/g" $destinationpath
    fi
    
    # Check deployment target so that we update "Uplink" at the right line number
    if [[ $target == 'Host' ]] ; then
        sed -i -e "152s/Uplink: Lab-Routers/Uplink: $portgroup/g" $destinationpath
    else
        sed -i -e "174s/Uplink: Lab-Routers/Uplink: $portgroup/g" $destinationpath
    fi
    
    sed -i -e "339s/Protocol: BOTH /Protocol: $routing/g" $destinationpath
else
    echo
    echo "Nothing updated. Exiting the script"
    echo
    exit 0
fi
echo
echo -e "Configuration file \033[33m$destinationpath\033[0m file has been created with the specified settings. You can use this file to generate your static Pod configuration."
echo -e "A static Pod configuration is generated by running \033[33mansible-playbook playbooks/createPodConfig.yml\033[0m."
echo
echo "Have fun!"
echo
exit 0