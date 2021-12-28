# Known Deprecated REST API Calls Used In SDDC.Lab

## NSX-T REST API Documentation (Main Page)
  - [NSX-T v3.1.2](https://developer.vmware.com/apis/1163/nsx-t)
  - [NSX-T v3.2.0](https://developer.vmware.com/apis/1198/nsx-t)
  - [NSX-T v3.2.0 Release Notes (shows all deprecated REST API calls)](https://docs.vmware.com/en/VMware-NSX-T-Data-Center/3.2/rn/vmware-nsxt-data-center-32-release-notes/index.html)


## Additional Notes
  - When an NSX-T depreacated REST API call is used, the header returns a warning in the error as follows:\
"warning": "299 - \\"Deprecated API\\""

If we do a full deployment, and can log the console output, then we can track which API calls are showing up as being deprecated.


## Deprecated API Usage

| Playbook(s) | NSX-T v3.2.0 API Section | Deprecated API | Replacement API | New API Works in v3.1.x | New API Works in v3.2.0 | Comments |
| :---        | :---        | :---        | :---        | :---        | :---        | :---        |
| createNsxEdgeTn.yml | [Transport Nodes](https://vdc-download.vmware.com/vmwb-repository/dcr-public/ce4128ae-8334-4f91-871b-ecce254cf69e/488f1280-204c-441d-8520-8279ac33d54b/api_includes/system_administration_configuration_fabric_nodes_transport_nodes.html) | [GET /api/v1/transport-nodes](https://vdc-download.vmware.com/vmwb-repository/dcr-public/ce4128ae-8334-4f91-871b-ecce254cf69e/488f1280-204c-441d-8520-8279ac33d54b/api_includes/method_ListTransportNodesWithDeploymentInfo.html) | [GET /policy/api/v1/infra/sites/\<site-id\>/enforcement-points/\<enforcementpoint-id\>/host-transport-nodes/state](https://vdc-download.vmware.com/vmwb-repository/dcr-public/ce4128ae-8334-4f91-871b-ecce254cf69e/488f1280-204c-441d-8520-8279ac33d54b/api_includes/method_ListHostTransportNodesByState.html) | No | Yes | When used against a Local Manager, use "default" for both \<site-id\> and \<enforcementpoint-id\>. |

