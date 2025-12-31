billing_network_tool/
│
├── main.py
│   # Точка входа:
│   # - asyncio.run()
│   # - CLI dispatch
│
├── cli/
│   ├── __init__.py
│   ├── args.py
│   │   # argparse (--ipoe, --sn, --uncfg, --help)
│   │
│   ├── commands.py
│   │   # CLI → core.operations mapping
│   │
│   └── help.py
│       # CLI help / usage
│
├── config/
│   └── secrets.py
│       # авторизация / список OLT
│
├── core/
│   ├── connection/
│   │   ├── __init__.py
│   │   └── telnet.py
│   │       # connect()
│   │       # send_bulk()   (GPON)
│   │       # send_ipoe()   (IPoE, prompt-based)
│   │       # TelnetConnectionError
│   │
│   └── operations/
│       │
│       ├── ipoe/
│       │   ├── __init__.py
│       │
│       │   ├── service.py
│       │   │   # run_ipoe()
│       │   │   # connect → detect_vendor → adapter → renderer
│       │
│       │   ├── detect_vendor.py
│       │   │   # detect_vendor(reader, writer)
│       │   │   # show version / show system
│       │   │   # UNKNOWN vendor handling
│       │
│       │   ├── adapter/
│       │   │   ├── __init__.py
│       │   │   ├── base.py
│       │   │   │   # BaseIPoEAdapter
│       │   │   │
│       │   │   ├── factory.py
│       │   │   │   # get_adapter(vendor, reader, writer)
│       │   │   │
│       │   │   └── ZTE/
│       │   │       ├── __init__.py
│       │   │       │
│       │   │       ├── adapter.py
│       │   │       │   # ZTEIPoEAdapter
│       │   │       │   # collect()
│       │   │       │
│       │   │       ├── commands.py
│       │   │       │   # SHOW_VERSION
│       │   │       │   # show_port()
│       │   │       │   # show_port_util()
│       │   │       │   # show_mac()
│       │   │       │   # SHOW_DHCP
│       │   │       │   # show_statistics()
│       │   │       │   # show_mac_protect()
│       │   │       │   # SHOW_LOGS
│       │   │       │
│       │   │       ├── query.py
│       │   │       │   # build_query_plan(port)
│       │   │       │   # key + commands + parser
│       │   │       │
│       │   │       ├── parsers/
│       │   │       │   ├── __init__.py
│       │   │       │   │
│       │   │       │   ├── zte_ipoe_device.py
│       │   │       │   │   # parse_zte_device_info()
│       │   │       │   │
│       │   │       │   ├── zte_ipoe_port.py
│       │   │       │   │   # parse_port_info()
│       │   │       │   │   # parse_port_errors()
│       │   │       │   │   # parse_mac_protect()
│       │   │       │   │
│       │   │       │   ├── zte_ipoe_utilization.py
│       │   │       │   │   # parse_port_utilization()
│       │   │       │   │
│       │   │       │   ├── zte_ipoe_mac.py
│       │   │       │   │   # parse_zte_mac()
│       │   │       │   │
│       │   │       │   ├── zte_ipoe_dhcp.py
│       │   │       │   │   # parse_dhcp_relay()
│       │   │       │   │
│       │   │       │   └── zte_ipoe_logs.py
│       │   │       │       # parse_device_logs()
│       │   │       │
│       │   │       └── tables/
│       │   │           ├── __init__.py
│       │   │           │
│       │   │           ├── zte_device.py
│       │   │           │   # print_device_info()
│       │   │           │
│       │   │           ├── zte_port_status.py
│       │   │           │   # print_port_status()
│       │   │           │
│       │   │           ├── zte_mac.py
│       │   │           │   # print_mac_table()
│       │   │           │
│       │   │           ├── zte_dhcp.py
│       │   │           │   # print_dhcp_table()
│       │   │           │
│       │   │           ├── zte_mac_protect.py
│       │   │           │   # print_mac_protect()
│       │   │           │
│       │   │           └── zte_logs.py
│       │   │               # print_logs()
│       │   │
│       │   └── render/
│       │       ├── __init__.py
│       │       ├── renderer_base.py
│       │       │   # BaseIPoERenderer
│       │       │
│       │       ├── renderer_factory.py
│       │       │   # get_renderer(vendor)
│       │       │
│       │       └── zte.py
│       │           # ZTERenderer
│       │           # orchestrates ZTE tables
│       │
│       └── onu/
│           ├── __init__.py
│           │
│           ├── adapters/
│           │   └── zte_zxan_olt.py
│           │       # ZteZxanOltAdapter
│           │       # search_by_sn()
│           │       # fetch_uncfg()
│           │
│           ├── commands/
│           │   └── zte_zxan.py
│           │       # SHOW_BY_SN
│           │       # SHOW_UNCFG
│           │       # SHOW_ONU_CFG
│           │       # SHOW_IP_SERVICE
│           │       # SHOW_DHCP_SNOOPING
│           │       # SHOW_PON_POWER
│           │       # SHOW_STATUS
│           │       # SHOW_INTERFACE
│           │       # SHOW_DETAIL_LOGS
│           │
│           ├── parsers/
│           │   ├── __init__.py
│           │   │
│           │   ├── common.py
│           │   │   # clean_line()
│           │   │
│           │   ├── search.py
│           │   │   # parse_onu_interface()
│           │   │   # parse_remote_id()
│           │   │
│           │   ├── ip_status.py
│           │   │   # parse_ip_status()
│           │   │
│           │   ├── uncfg.py
│           │   │   # parse_uncfg()
│           │   │
│           │   ├── pon_power.py
│           │   │   # parse_pon_power()
│           │   │
│           │   ├── speed.py
│           │   │   # parse_speed()
│           │   │
│           │   └── detail_logs.py
│           │       # parse_detail_logs()
│           │
│           ├── tables/
│           │   ├── search.py
│           │   │   # print_sn_table()
│           │   │
│           │   ├── ip_status.py
│           │   │   # print_ip_status()
│           │   │
│           │   ├── uncfg.py
│           │   │   # print_uncfg_table()
│           │   │
│           │   ├── pon_power.py
│           │   │   # print_pon_power()
│           │   │
│           │   ├── speed.py
│           │   │   # print_speed()
│           │   │
│           │   └── detail_logs.py
│           │       # print_detail_logs()
│           │
│           └── __init__.py
│
├── output/
│   ├── __init__.py
│   ├── colors.py
│   │   # ANSI color codes
│   │
│   └── table_base.py
│       # render_table()
│       # единый стандарт таблиц
│
└── README.md
