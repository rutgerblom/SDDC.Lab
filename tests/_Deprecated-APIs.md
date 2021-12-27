# Known Deprecated REST API Calls Used In SDDC.Lab

## NSX-T REST API Documentation (Main Page)
  - [NSX-T v3.1.2](https://developer.vmware.com/apis/1163/nsx-t)
  - [NSX-T v3.2.0](https://developer.vmware.com/apis/1198/nsx-t)


## Deprecated API Usage

| Playbook(s) | NSX-T v3.2.0 API Section | Deprecated API | Replacement API | New API Works v3.1.x | New API Works v3.2.0 | Comments |
| :---        | :---        | :---        | :---        | :---        | :---        | :---        |
| createNsxEdgeTn.yml | [Transport Nodes](https://vdc-download.vmware.com/vmwb-repository/dcr-public/ce4128ae-8334-4f91-871b-ecce254cf69e/488f1280-204c-441d-8520-8279ac33d54b/api_includes/system_administration_configuration_fabric_nodes_transport_nodes.html) | [GET /api/v1/transport-nodes](https://vdc-download.vmware.com/vmwb-repository/dcr-public/ce4128ae-8334-4f91-871b-ecce254cf69e/488f1280-204c-441d-8520-8279ac33d54b/api_includes/method_ListTransportNodesWithDeploymentInfo.html) | [GET /policy/api/v1/infra/sites/\<site-id\>/enforcement-points/\<enforcementpoint-id\>/host-transport-nodes/state](https://vdc-download.vmware.com/vmwb-repository/dcr-public/ce4128ae-8334-4f91-871b-ecce254cf69e/488f1280-204c-441d-8520-8279ac33d54b/api_includes/method_ListHostTransportNodesByState.html) | No | Yes | When used against a Local Manager, use "default" for both \<site-id\> and \<enforcementpoint-id\>. |

