import psutil

from tools.system_monitor.resource_usage import show_usage, ResourceUsage


def get_cpu():
    return psutil.cpu_percent(interval=1)
def get_memory():
    return psutil.virtual_memory()
def get_disk():
    return psutil.disk_usage('/')
def bytes_to_gb(val):
    return float(val) / 1024**3

sources = {
    "RAM": get_memory,
    "CPU": get_cpu,
    "DISK": get_disk
}
def run():
    print("System Monitor")
    components = []
    for name, usage in sources.items():
        usage = usage()
        if hasattr(usage, "percent"):
            percent = usage.percent
            details = f"{bytes_to_gb(usage.used):.1f} GB / {bytes_to_gb(usage.total):.1f} GB"
        else:
            percent = usage
            details = ""
        ru = ResourceUsage(name, percent, details)
        components.append(ru)

    show_usage("SYSTEM MONITOR",components)


if __name__ == "__main__":
    run()