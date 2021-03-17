# Changelog

## 3.0.0 16-MARCH-2021

### Added

- Changed Lab-Routers area from 666 to 0 (i.e. Backbone area) to facilitate sharing of routes between sites if NSX-T is reconfigured to use OSPF versus eBGP.
  This reconfiguration to use OSPF is not supported by automation, and would have to be done manually afterwards by the user.

