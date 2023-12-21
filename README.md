# Why
Written primarily for DevNet Expert Studies. Accepts YAML input via CLI tool, converts to XML and validates against a custom YANG model, returns NETCONF edit-config RPC data.

With some work, this could be an effective IaC tool for IOS-XE devices. 



## How it works

1. The user provides a YAML file that contains the network configuration data. This is handled in the cli.py file, where the YAML file is read and its contents are passed to different configuration model classes.
Validation Through YANG Model:

2. The YAML file's contents are validated against YANG models to ensure they adhere to the correct structure and constraints. This is done using various YANG model files like bgp_validator.yang, device_validator.yang, etc. The validation logic is implemented in the UtilityConfig class, which includes methods for YANG model validation.
Creating Python Objects:

3. The validated data from the YAML file is then used to create Python objects representing different network configurations. This is done through various classes in the configuration_models/ios_xe directory, such as ConfigInterface, StaticRoutes, RouterBgp, etc. Each of these classes inherits from the CompositeConfig class, which provides common functionalities for handling configuration data.
Outputting Edit-Config RPC:

4. Finally, the Python objects are used to generate an edit-config RPC in XML format. This is achieved through Jinja2 templates like edit_config.xml. The print_config method in classes like ConfigInterface, StaticRoutes, etc., renders the final XML configuration.

![image](https://github.com/jamesduv9/network_dsl/assets/32336049/93f54aa6-d4eb-4eae-871d-a9767315befb)

## Example
```
python cli.py --file test_pg_change.yml

output -
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    /* Hundreds of lines of XML */
  </native>
</config>
```

## YANG Model

The pyang tree of the custom YANG model follows -
```
module: device_validator
  +--rw device
     +--rw type           enumeration
     +--rw router_bgp
     |  +--rw asn?              uint16
     |  +--rw router_id?        inet:ipv4-address
     |  +--rw peer_group* [name]
     |  |  +--rw name                       string
     |  |  +--rw remote_as                  uint16
     |  |  +--rw ebgp_multihop?             uint16
     |  |  +--rw fallover_bfd?              enumeration
     |  |  +--rw description?               string
     |  |  +--rw shutdown?                  boolean
     |  |  +--rw update_source?             string
     |  |  +--rw peer_group?                -> ../../peer_group/name
     |  |  +--rw disable_connected_check?   boolean
     |  |  +--rw password?                  string
     |  |  +--rw test
     |  |  |  +--rw icmp
     |  |  |  |  +--rw max_latency?   uint16
     |  |  |  |  +--rw max_jitter?    uint16
     |  |  |  +--rw bgp
     |  |  |  |  +--rw received_route*     inet:ipv4-prefix
     |  |  |  |  +--rw advertised_route*   inet:ipv4-prefix
     |  |  |  +--rw interface?   boolean
     |  |  +--rw next_hop_self?             boolean
     |  |  +--rw route_map* [direction]
     |  |  |  +--rw direction    enumeration
     |  |  |  +--rw name?        -> /device/route_map/name
     |  |  +--rw prefix_list* [direction]
     |  |     +--rw direction    enumeration
     |  |     +--rw name?        string
     |  +--rw neighbor* [neighbor_ip]
     |  |  +--rw neighbor_ip                inet:ipv4-address
     |  |  +--rw remote_as                  uint16
     |  |  +--rw ebgp_multihop?             uint16
     |  |  +--rw fallover_bfd?              enumeration
     |  |  +--rw description?               string
     |  |  +--rw shutdown?                  boolean
     |  |  +--rw update_source?             string
     |  |  +--rw peer_group?                -> ../../peer_group/name
     |  |  +--rw disable_connected_check?   boolean
     |  |  +--rw password?                  string
     |  |  +--rw test
     |  |     +--rw icmp
     |  |     |  +--rw max_latency?   uint16
     |  |     |  +--rw max_jitter?    uint16
     |  |     +--rw bgp
     |  |     |  +--rw received_route*     inet:ipv4-prefix
     |  |     |  +--rw advertised_route*   inet:ipv4-prefix
     |  |     +--rw interface?   boolean
     |  +--rw address_family
     |     +--rw ipv4_unicast
     |        +--rw network* [ip_network]
     |        |  +--rw ip_network     inet:ipv4-address
     |        |  +--rw subnet_mask    inet:ipv4-address
     |        +--rw neighbor* [neighbor_ip]
     |           +--rw neighbor_ip      -> ../../../../neighbor/neighbor_ip
     |           +--rw next_hop_self?   boolean
     |           +--rw route_map* [direction]
     |           |  +--rw direction    enumeration
     |           |  +--rw name?        -> /device/route_map/name
     |           +--rw prefix_list* [direction]
     |              +--rw direction    enumeration
     |              +--rw name?        string
     +--rw route_map* [name]
     |  +--rw name        string
     |  +--rw sequence* [seq_num]
     |     +--rw seq_num        string
     |     +--rw operation      enumeration
     |     +--rw description?   string
     |     +--rw match
     |     |  +--rw ip_address
     |     |  |  +--rw (matching_ip)?
     |     |  |     +--:(prefix_list)
     |     |  |     |  +--rw prefix_list?   -> /device/prefix_list/name
     |     |  |     +--:(access_list)
     |     |  |        +--rw access_list?   string
     |     |  +--rw interfaces*   string
     |     +--rw set
     |        +--rw local_preference?   uint32
     |        +--rw ip_next_hop
     |           +--rw address*   inet:ipv4-address
     +--rw prefix_list* [name]
     |  +--rw name        string
     |  +--rw sequence* [seq_num]
     |     +--rw seq_num      uint16
     |     +--rw ip_prefix    inet:ipv4-prefix
     |     +--rw (filter)?
     |     |  +--:(ge)
     |     |  |  +--rw ge?    uint8
     |     |  +--:(le)
     |     |  |  +--rw le?    uint8
     |     |  +--:(eq)
     |     |     +--rw eq?    uint8
     |     +--rw action       enumeration
     +--rw ip_route
     |  +--rw vrf* [prefix vrf mask]
     |  |  +--rw prefix                      inet:ipv4-address
     |  |  +--rw vrf                         string
     |  |  +--rw mask                        inet:ipv4-address
     |  |  +--rw (next_hop_choice)?
     |  |  |  +--:(next_hop_ip)
     |  |  |  |  +--rw next_hop_ip?          inet:ipv4-address
     |  |  |  +--:(next_hop_interface)
     |  |  |  |  +--rw next_hop_interface?   string
     |  |  |  +--:(next_hop_both)
     |  |  |     +--rw next_hop_both
     |  |  |        +--rw next_hop_interface?   string
     |  |  |        +--rw next_hop_ip?          inet:ipv4-address
     |  |  +--rw metric?                     uint8
     |  |  +--rw name?                       string
     |  +--rw global* [prefix mask]
     |     +--rw prefix                      inet:ipv4-address
     |     +--rw vrf?                        string
     |     +--rw mask                        inet:ipv4-address
     |     +--rw (next_hop_choice)?
     |     |  +--:(next_hop_ip)
     |     |  |  +--rw next_hop_ip?          inet:ipv4-address
     |     |  +--:(next_hop_interface)
     |     |  |  +--rw next_hop_interface?   string
     |     |  +--:(next_hop_both)
     |     |     +--rw next_hop_both
     |     |        +--rw next_hop_interface?   string
     |     |        +--rw next_hop_ip?          inet:ipv4-address
     |     +--rw metric?                     uint8
     |     +--rw name?                       string
     +--rw interface
        +--rw physical_interfaces* [name]
           +--rw name                   string
           +--rw encapsulation_dot1q?   valid_vlan
           +--rw switchport?            boolean
           +--rw vrf_forwarding?        string
           +--rw ip_nat_direction?      enumeration
           +--rw ip_access_group* [direction]
           |  +--rw direction       enumeration
           |  +--rw (name_or_number)?
           |     +--:(name)
           |     |  +--rw name?     string
           |     +--:(number)
           |        +--rw number?   uint16
           +--rw ip_address
           |  +--rw address?   inet:ipv4-address
           |  +--rw mask?      inet:ipv4-address
           +--rw switchport_mode
              +--rw (mode)?
                 +--:(access)
                 |  +--rw access
                 |     +--rw vlan?   valid_vlan
                 +--:(trunk)
                    +--rw trunk
                       +--rw allowed_vlans*   valid_vlan
```
