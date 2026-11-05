import streamlit as st
import subprocess
import re
from pathlib import Path
from config import PROJECT_NAME

# ---------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="ConfigSync | Infrastructure",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------
# CUSTOM CSS
# ---------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background-color: #111c30;
}

[data-testid="stMetric"] {
    background: #172238;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #293750;
}

.server-box {
    background: #172238;
    border: 1px solid #293750;
    padding: 20px;
    border-radius: 14px;
}

h1, h2, h3, h4 {
    color: #e5e7eb !important;
}

p, label {
    color: #cbd5e1;
}

hr {
    border-color: #293750;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------
# COMMAND EXECUTION
# ---------------------------------------

def run_ubuntu(command):

    try:
        result = subprocess.run(
            [
                "vagrant", "ssh", "ubuntu",
                "-c",
                f"cd ~/configsync && {command}"
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=60
        )

        return result.stdout + result.stderr

    except Exception as e:
        return f"ERROR: {e}"


# ---------------------------------------
# METRICS COLLECTION
# ---------------------------------------

METRIC_COMMAND = r"""printf 'HOST=%s\n' "$(hostname)";
printf 'CPU=';
LC_ALL=C top -bn1 | awk -F',' '/Cpu\(s\)/ {
gsub(/[^0-9.]/,"",$4);
print 100-$4;
found=1
} END {if (!found) print 0}';
free -b | awk '/Mem:/ {
printf "MEM_USED=%s\nMEM_TOTAL=%s\n",$3,$2
}';
df -B1 / | awk 'NR==2 {
printf "DISK_USED=%s\nDISK_TOTAL=%s\n",$3,$2
}'"""


def get_managed_metrics():

    return run_ubuntu(
        f"""ansible all -i inventory/hosts.ini
        -m shell -a '{METRIC_COMMAND}'"""
    )


def get_controller_metrics():

    return run_ubuntu(METRIC_COMMAND)


# ---------------------------------------
# PARSE METRICS
# ---------------------------------------

def parse_key_values(output):

    data = {}

    for line in output.splitlines():

        line = line.strip()

        if "=" in line:

            key, value = line.split("=", 1)

            if key in [
                "HOST", "CPU",
                "MEM_USED", "MEM_TOTAL",
                "DISK_USED", "DISK_TOTAL"
            ]:
                data[key] = value.strip()

    return data


def parse_ansible_metrics(output):

    servers = {}
    current = None

    for line in output.splitlines():

        header = re.match(
            r"^([A-Za-z0-9_.-]+)\s+\|\s+(SUCCESS|CHANGED|FAILED|UNREACHABLE)",
            line.strip()
        )

        if header:

            hostname = header.group(1)
            current = {}
            servers[hostname] = current

            continue

        if current is not None and "=" in line:

            key, value = line.strip().split("=", 1)

            if key in [
                "HOST", "CPU",
                "MEM_USED", "MEM_TOTAL",
                "DISK_USED", "DISK_TOTAL"
            ]:
                current[key] = value.strip()

    return servers


def to_gb(value):

    return int(value) / (1024 ** 3)


# ---------------------------------------
# SERVER STATUS
# ---------------------------------------

def get_connectivity():

    return run_ubuntu(
        "ansible all -i inventory/hosts.ini -m ping"
    )


def check_status(output, hostname):

    pattern = rf"^{re.escape(hostname)}\s+\|\s+(SUCCESS|CHANGED)"

    return bool(
        re.search(pattern, output, re.MULTILINE)
    )


# ---------------------------------------
# SECURITY MONITORING
# ---------------------------------------

def get_security():

    command = r"""ansible all -i inventory/hosts.ini -m shell -a 'echo HOST=$(hostname); echo FIREWALL=$(systemctl is-active firewalld 2>/dev/null || echo inactive); echo SELINUX=$(getenforce 2>/dev/null || echo unavailable); echo SSH=$(systemctl is-active sshd 2>/dev/null || echo inactive)'"""

    return run_ubuntu(command)


# ---------------------------------------
# SERVER CARD
# ---------------------------------------

def show_server(name, role, online, metrics):

    with st.container(border=True):

        st.markdown(f"### 🖥️ {name}")

        st.caption(role)

        if online:
            st.success("● ONLINE")
        else:
            st.error("● OFFLINE")

        st.divider()

        if not online:

            st.warning("Server is not reachable.")
            return

        if not metrics:

            st.warning("Metrics unavailable.")
            return

        try:

            cpu = float(metrics["CPU"])

            cpu = min(100, max(0, cpu))

            mem_used = to_gb(metrics["MEM_USED"])
            mem_total = to_gb(metrics["MEM_TOTAL"])

            disk_used = to_gb(metrics["DISK_USED"])
            disk_total = to_gb(metrics["DISK_TOTAL"])

            # CPU

            st.markdown("**⚡ CPU Usage**")

            st.metric(
                "Processor Utilization",
                f"{cpu:.1f}%"
            )

            st.progress(cpu / 100)

            # MEMORY

            st.markdown("**🧠 Memory Usage**")

            mem_percent = (
                mem_used / mem_total
                if mem_total else 0
            )

            st.metric(
                "RAM Utilization",
                f"{mem_percent * 100:.1f}%"
            )

            st.caption(
                f"{mem_used:.2f} GB used / {mem_total:.2f} GB total"
            )

            st.progress(min(1.0, mem_percent))

            # DISK

            st.markdown("**💾 Disk Space**")

            disk_percent = (
                disk_used / disk_total
                if disk_total else 0
            )

            st.metric(
                "Disk Utilization",
                f"{disk_percent * 100:.1f}%"
            )

            st.caption(
                f"{disk_used:.2f} GB used / {disk_total:.2f} GB total"
            )

            st.progress(min(1.0, disk_percent))

        except (KeyError, ValueError, ZeroDivisionError):

            st.warning("Unable to parse server resource information.")


# ---------------------------------------
# HEADER
# ---------------------------------------

st.title("🖥️ ConfigSync")

st.caption(
    "LINUX INFRASTRUCTURE & CONFIGURATION MANAGEMENT"
)

st.markdown(
    "Monitor your Linux servers, system resources, "
    "Ansible connectivity and security."
)

st.divider()


# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.title("⚙️ CONTROL PANEL")

st.sidebar.success("Vagrant Environment")

st.sidebar.markdown("### Infrastructure")

st.sidebar.write("🟢 Ubuntu Controller")
st.sidebar.write("🟢 Rocky Linux")
st.sidebar.write("🟢 AlmaLinux")

st.sidebar.divider()

refresh = st.sidebar.button(
    "🔄 Refresh Monitoring",
    use_container_width=True
)

st.sidebar.caption(
    "ConfigSync | Ansible + Linux"
)


# ---------------------------------------
# COLLECT DATA
# ---------------------------------------

with st.spinner("Connecting to Linux servers..."):

    ping_output = get_connectivity()

    controller_raw = get_controller_metrics()

    managed_raw = get_managed_metrics()

controller_metrics = parse_key_values(controller_raw)

managed_metrics = parse_ansible_metrics(managed_raw)

ubuntu_online = (
    "ERROR:" not in controller_raw
    and "HOST" in controller_metrics
)

rocky_online = check_status(ping_output, "rocky")
alma_online = check_status(ping_output, "alma")

online_count = sum([
    ubuntu_online,
    rocky_online,
    alma_online
])


# ---------------------------------------
# OVERVIEW
# ---------------------------------------

st.subheader("📊 Infrastructure Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Servers", 3)

c2.metric(
    "Online Servers",
    online_count
)

c3.metric(
    "Offline Servers",
    3 - online_count
)

c4.metric("Managed Nodes", 2)

st.divider()


# ---------------------------------------
# COMBINED SERVER MONITORING
# ---------------------------------------

st.subheader("🖥️ Server Monitoring")

st.caption(
    "Individual CPU, Memory and Disk utilization "
    "for all Linux infrastructure nodes."
)

rocky_metrics = managed_metrics.get("rocky", {})
alma_metrics = managed_metrics.get("alma", {})

col1, col2, col3 = st.columns(3)

with col1:

    show_server(
        "Ubuntu",
        "Ansible Controller",
        ubuntu_online,
        controller_metrics
    )

with col2:

    show_server(
        "Rocky Linux",
        "Managed Server 1",
        rocky_online,
        rocky_metrics
    )

with col3:

    show_server(
        "AlmaLinux",
        "Managed Server 2",
        alma_online,
        alma_metrics
    )


st.divider()


# ---------------------------------------
# ANSIBLE CONNECTIVITY
# ---------------------------------------

st.subheader("🔗 Ansible Connectivity")

if rocky_online and alma_online:

    st.success(
        "Both managed servers are reachable through Ansible."
    )

else:

    st.warning(
        "One or more managed servers are unreachable."
    )

with st.expander("View Ansible Ping Logs"):

    st.code(ping_output or "No output available.")


# ---------------------------------------
# SECURITY MONITORING
# ---------------------------------------

st.subheader("🛡️ Security Monitoring")

if st.button("Check Security Configuration"):

    with st.spinner("Checking Linux security..."):

        security_output = get_security()

    st.code(security_output or "No security data received.")


# ---------------------------------------
# EXECUTION LOGS
# ---------------------------------------

st.subheader("📋 Infrastructure Execution Logs")

with st.expander("View Controller Information"):

    st.code(controller_raw or "No controller information.")

with st.expander("View Managed Server Metrics Output"):

    st.code(managed_raw or "No metrics output.")


# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "ConfigSync | Linux Configuration Management "
    "| Powered by Ansible, Vagrant and Streamlit"
)