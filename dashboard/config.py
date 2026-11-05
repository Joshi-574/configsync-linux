PROJECT_NAME = "ConfigSync"

SERVERS = {
    "Ubuntu": {
        "role": "Ansible Controller",
        "host": "192.168.56.11",
    },
    "Rocky Linux": {
        "role": "Managed Server 1",
        "host": "192.168.56.12",
    },
    "AlmaLinux": {
        "role": "Managed Server 2",
        "host": "192.168.56.13",
    },
}