# ConfigSync – Automated Linux Configuration Management

**Ansible-Based Multi-Distribution Linux Configuration Automation**

## 1. Project Overview

ConfigSync is an Ansible-based infrastructure automation project designed to maintain consistent system configurations and security settings across multiple Linux distributions.

The project uses Ubuntu as the Ansible Controller and Rocky Linux 9.6 and AlmaLinux 9.7 as managed nodes.

It automates package installation, timezone configuration, SSH hardening, firewall verification, and SELinux status monitoring.

## 2. Project Objectives

- Automate Linux system administration tasks.
- Maintain consistent configurations across multiple servers.
- Automate common package installation.
- Improve SSH security through configuration hardening.
- Verify firewall and SELinux security status.
- Maintain Ansible execution logs.
- Demonstrate idempotency and check-mode execution.

## 3. System Architecture

| Component | Configuration |
|---|---|
| Controller | Ubuntu 22.04 |
| Managed Node 1 | Rocky Linux 9.6 |
| Managed Node 2 | AlmaLinux 9.7 |
| Automation Tool | Ansible |
| Infrastructure Tool | Vagrant |
| Configuration Language | YAML |
| Template Engine | Jinja2 |
| Communication | SSH |

### Architecture Flow

```text
             Ubuntu Controller
                    |
                  Ansible
                    |
             SSH Connection
                    |
          ---------------------
          |                   |
     Rocky Linux          AlmaLinux
       9.6                   9.7
          |                   |
     Configuration       Configuration
      Management           Management
```

## 4. Project Structure

```text
configsync/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── group_vars/
│   └── linux_servers.yml
├── roles/
│   ├── common/
│   │   ├── tasks/main.yml
│   │   └── handlers/main.yml
│   └── security/
│       ├── tasks/main.yml
│       ├── handlers/main.yml
│       └── templates/
│           └── sshd_config.conf.j2
├── logs/
│   └── ansible.log
├── playbooks/
├── README.md
└── site.yml
```

## 5. Technologies Used

- Ansible – Configuration management and automation.
- Vagrant – Virtual machine provisioning.
- Ubuntu – Ansible controller.
- Rocky Linux – Managed Linux server.
- AlmaLinux – Managed Linux server.
- YAML – Automation playbooks and variables.
- Jinja2 – Dynamic configuration templates.
- SSH – Secure remote connectivity.

## 6. Implemented Features

1. Automated common package installation.
2. System timezone configuration.
3. SSH security hardening.
4. Firewall status verification.
5. SELinux status verification.
6. SSH configuration syntax validation.
7. Ansible execution logging.
8. Idempotency testing.
9. Ansible check-mode testing.
10. Multi-distribution configuration management.

## 7. Execution Commands

### Check Server Connectivity

```bash
ansible linux_servers -m ping
```

### Check Playbook Syntax

```bash
ansible-playbook site.yml --syntax-check
```

### Execute Configuration Management

```bash
ansible-playbook site.yml
```

### Perform Dry Run

```bash
ansible-playbook site.yml --check
```

### Verify Execution Logs

```bash
tail -20 logs/ansible.log
```

## 8. Testing and Results

| Test | Result |
|---|---|
| Rocky Linux Connectivity | Successful |
| AlmaLinux Connectivity | Successful |
| SSH Configuration Validation | Passed |
| Firewall Status | Active |
| SELinux Status | Enforcing |
| Idempotency Testing | Passed |
| Check Mode Testing | Executed Successfully |
| Final Playbook Execution | Zero Failures |

## 9. Key Benefits

- Reduces manual Linux administration.
- Improves configuration consistency.
- Enhances server security.
- Supports repeatable automation.
- Simplifies multi-server management.
- Provides execution logs for troubleshooting.

## 10. Conclusion

ConfigSync successfully demonstrates automated Linux configuration management across Rocky Linux and AlmaLinux using Ansible.

By implementing roles, templates, handlers, variables, SSH hardening, and security verification, the project provides a repeatable and consistent approach to Linux infrastructure administration.

**Project Status:** Successfully Implemented

**Developed as a Linux Infrastructure Automation Project.**
