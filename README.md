# ConfigSync – Automated Linux Configuration Management

## 1. Project Overview

ConfigSync is an Ansible-based automation project that maintains consistent system configurations and security settings across multiple Linux distributions.

The project uses Ubuntu as the Ansible Controller and Rocky Linux 9.6 and AlmaLinux 9.7 as managed nodes.

## 2. Objectives

- Automate Linux system configuration.
- Maintain consistent configurations across multiple servers.
- Automate common package installation.
- Improve SSH security.
- Verify Firewall and SELinux status.
- Maintain execution logs.
- Demonstrate Ansible idempotency.

## 3. Architecture

- Controller: Ubuntu
- Managed Node 1: Rocky Linux
- Managed Node 2: AlmaLinux
- Automation Tool: Ansible
- Infrastructure Tool: Vagrant
- Configuration Language: YAML
- Template Engine: Jinja2

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
│       └── templates/sshd_config.conf.j2
├── logs/
│   └── ansible.log
├── playbooks/
└── site.yml
```

## 5. Technologies Used

- Ansible
- Vagrant
- Ubuntu
- Rocky Linux
- AlmaLinux
- YAML
- Jinja2
- SSH

## 6. Implemented Features

1. Common package installation.
2. System timezone management.
3. SSH hardening.
4. Firewall verification.
5. SELinux verification.
6. SSH configuration validation.
7. Ansible execution logging.
8. Idempotency testing.
9. Check mode testing.

## 7. Execution Commands

Check connectivity:

```bash
ansible linux_servers -m ping
```

Check syntax:

```bash
ansible-playbook site.yml --syntax-check
```

Execute configuration:

```bash
ansible-playbook site.yml
```

Dry-run testing:

```bash
ansible-playbook site.yml --check
```

Verify execution logs:

```bash
tail -20 logs/ansible.log
```

## 8. Testing Results

- Rocky Linux connectivity: Successful.
- AlmaLinux connectivity: Successful.
- SSH configuration: Valid.
- Firewall: Active.
- SELinux: Enforcing.
- Idempotency: Passed.
- Check mode: Executed successfully.
- Final playbook execution: Zero failures.

## 9. Conclusion

ConfigSync successfully automates common configuration and security verification across Rocky Linux and AlmaLinux using Ansible roles, templates, handlers and variables. It improves consistency, reduces manual administration and demonstrates repeatable infrastructure automation.
