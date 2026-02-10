"""
Markdown Generator Module - Generates markdown documentation from device information
"""

from typing import Dict, Any
from datetime import datetime


class MarkdownGenerator:
    """Generate markdown documentation from device information and APIs"""

    def __init__(self, device_info: Dict[str, Any], available_apis: Dict[str, Dict[str, Any]]):
        """
        Initialize markdown generator
        
        Args:
            device_info: Device information dictionary
            available_apis: Available API methods dictionary
        """
        self.device_info = device_info
        self.available_apis = available_apis
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_header(self) -> str:
        """Generate markdown header"""
        header = f"""# Device Information Report

**Generated:** {self.timestamp}

---

## 📋 Report Overview

This report contains comprehensive information about the system device properties, configuration, and available APIs.

"""
        return header

    def generate_system_info_section(self) -> str:
        """Generate system information section"""
        system = self.device_info.get("system", {})
        
        markdown = "## 🖥️ System Information\n\n"
        markdown += "| Property | Value |\n"
        markdown += "|----------|-------|\n"
        
        for key, value in system.items():
            property_name = key.replace("_", " ").title()
            markdown += f"| {property_name} | `{value}` |\n"
        
        markdown += "\n"
        return markdown

    def generate_cpu_section(self) -> str:
        """Generate CPU information section"""
        cpu = self.device_info.get("cpu", {})
        
        markdown = "## 🔧 CPU Information\n\n"
        
        if "error" in cpu:
            markdown += f"⚠️ Error: {cpu['error']}\n\n"
            return markdown
        
        markdown += "| Property | Value |\n"
        markdown += "|----------|-------|\n"
        markdown += f"| Physical Cores | `{cpu.get('physical_cores', 'N/A')}` |\n"
        markdown += f"| Logical Cores | `{cpu.get('logical_cores', 'N/A')}` |\n"
        markdown += f"| CPU Frequency (MHz) | `{cpu.get('cpu_freq_mhz', 'N/A')}` |\n"
        markdown += f"| Current CPU Usage | `{cpu.get('cpu_percent', 'N/A')}%` |\n"
        
        markdown += "\n### Per-Core CPU Usage\n\n"
        per_cpu = cpu.get("per_cpu_percent", [])
        for i, usage in enumerate(per_cpu):
            markdown += f"- Core {i}: `{usage}%`\n"
        
        markdown += "\n"
        return markdown

    def generate_memory_section(self) -> str:
        """Generate memory information section"""
        memory = self.device_info.get("memory", {})
        
        markdown = "## 💾 Memory Information\n\n"
        
        if "error" in memory:
            markdown += f"⚠️ Error: {memory['error']}\n\n"
            return markdown
        
        markdown += "| Property | Value |\n"
        markdown += "|----------|-------|\n"
        markdown += f"| Total RAM | `{memory.get('total_gb', 'N/A')} GB` |\n"
        markdown += f"| Used RAM | `{memory.get('used_gb', 'N/A')} GB` |\n"
        markdown += f"| Available RAM | `{memory.get('available_gb', 'N/A')} GB` |\n"
        markdown += f"| Memory Usage | `{memory.get('percent', 'N/A')}%` |\n"
        
        markdown += "\n"
        return markdown

    def generate_gpu_section(self) -> str:
        """Generate GPU information section"""
        gpu_data = self.device_info.get("gpu", {})
        gpus = gpu_data.get("gpus", [])
        
        markdown = "## 🎮 GPU Information\n\n"
        
        if not gpus:
            note = gpu_data.get("note", "No GPU detected or GPUtil not installed")
            markdown += f"ℹ️ {note}\n\n"
            return markdown
        
        for gpu in gpus:
            markdown += f"### GPU {gpu.get('id', 'Unknown')}: {gpu.get('name', 'Unknown')}\n\n"
            markdown += "| Property | Value |\n"
            markdown += "|----------|-------|\n"
            markdown += f"| Load | `{gpu.get('load_percent', 'N/A')}%` |\n"
            markdown += f"| Memory Total | `{gpu.get('memory_total_mb', 'N/A')} MB` |\n"
            markdown += f"| Memory Used | `{gpu.get('memory_used_mb', 'N/A')} MB` |\n"
            markdown += f"| Memory Free | `{gpu.get('memory_free_mb', 'N/A')} MB` |\n"
            markdown += f"| Temperature | `{gpu.get('temperature', 'N/A')}°C` |\n\n"
        
        return markdown

    def generate_disk_section(self) -> str:
        """Generate disk information section"""
        disks = self.device_info.get("disk", {})
        
        markdown = "## 💿 Storage Information\n\n"
        
        if "error" in disks:
            markdown += f"⚠️ Error: {disks['error']}\n\n"
            return markdown
        
        for device, info in disks.items():
            markdown += f"### {device}\n\n"
            markdown += "| Property | Value |\n"
            markdown += "|----------|-------|\n"
            markdown += f"| Mount Point | `{info.get('mountpoint', 'N/A')}` |\n"
            markdown += f"| File System | `{info.get('fstype', 'N/A')}` |\n"
            markdown += f"| Total Space | `{info.get('total_gb', 'N/A')} GB` |\n"
            markdown += f"| Used Space | `{info.get('used_gb', 'N/A')} GB` |\n"
            markdown += f"| Free Space | `{info.get('free_gb', 'N/A')} GB` |\n"
            markdown += f"| Usage | `{info.get('percent', 'N/A')}%` |\n\n"
        
        return markdown

    def generate_network_section(self) -> str:
        """Generate network information section"""
        networks = self.device_info.get("network", {})
        
        markdown = "## 🌐 Network Information\n\n"
        
        if "error" in networks:
            markdown += f"⚠️ Error: {networks['error']}\n\n"
            return markdown
        
        for interface, addrs in networks.items():
            markdown += f"### Interface: {interface}\n\n"
            for addr in addrs:
                markdown += f"**Family:** `{addr.get('family', 'N/A')}`\n\n"
                markdown += "| Property | Value |\n"
                markdown += "|----------|-------|\n"
                markdown += f"| Address | `{addr.get('address', 'N/A')}` |\n"
                markdown += f"| Netmask | `{addr.get('netmask', 'N/A')}` |\n"
                markdown += f"| Broadcast | `{addr.get('broadcast', 'N/A')}` |\n\n"
        
        return markdown

    def generate_process_section(self) -> str:
        """Generate process information section"""
        process = self.device_info.get("process", {})
        
        markdown = "## ⚙️ Process Information\n\n"
        
        if "error" in process:
            markdown += f"⚠️ Error: {process['error']}\n\n"
            return markdown
        
        # Top CPU processes
        markdown += "### Top 5 Processes by CPU Usage\n\n"
        top_cpu = process.get("top_cpu", [])
        if top_cpu:
            markdown += "| PID | Name | CPU % | Memory % |\n"
            markdown += "|-----|------|-------|----------|\n"
            for proc in top_cpu:
                markdown += f"| `{proc.get('pid', 'N/A')}` | {proc.get('name', 'N/A')} | `{proc.get('cpu_percent', 'N/A')}%` | `{proc.get('memory_percent', 'N/A')}%` |\n"
            markdown += "\n"
        
        # Top Memory processes
        markdown += "### Top 5 Processes by Memory Usage\n\n"
        top_mem = process.get("top_memory", [])
        if top_mem:
            markdown += "| PID | Name | CPU % | Memory % |\n"
            markdown += "|-----|------|-------|----------|\n"
            for proc in top_mem:
                markdown += f"| `{proc.get('pid', 'N/A')}` | {proc.get('name', 'N/A')} | `{proc.get('cpu_percent', 'N/A')}%` | `{proc.get('memory_percent', 'N/A')}%` |\n"
            markdown += "\n"
        
        return markdown

    def generate_uptime_section(self) -> str:
        """Generate uptime information section"""
        uptime = self.device_info.get("uptime", {})
        
        markdown = "## 📅 System Uptime\n\n"
        
        if "error" in uptime:
            markdown += f"⚠️ Error: {uptime['error']}\n\n"
            return markdown
        
        markdown += "| Property | Value |\n"
        markdown += "|----------|-------|\n"
        markdown += f"| Uptime | `{uptime.get('uptime_days', 0)} days, {uptime.get('uptime_hours', 0)} hours, {uptime.get('uptime_minutes', 0)} minutes` |\n"
        markdown += f"| Total Uptime (seconds) | `{uptime.get('uptime_seconds', 'N/A')}` |\n"
        
        markdown += "\n"
        return markdown

    def generate_api_reference_section(self) -> str:
        """Generate API reference section"""
        markdown = "## 🔌 API Reference\n\n"
        markdown += "### Available Methods\n\n"
        
        # Group by category
        categories = {}
        for method, details in self.available_apis.items():
            category = details.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append((method, details))
        
        for category in sorted(categories.keys()):
            markdown += f"### {category}\n\n"
            for method, details in categories[category]:
                markdown += f"#### `{method}()`\n\n"
                markdown += f"**Description:** {details.get('description', 'N/A')}\n\n"
                markdown += f"**Returns:** {details.get('returns', 'N/A')}\n\n"
        
        return markdown

    def generate_code_examples_section(self) -> str:
        """Generate code examples section"""
        markdown = """## 💻 Code Examples

### Import and Basic Usage

```python
from device_scanner import DeviceScanner

# Create scanner instance
scanner = DeviceScanner()

# Perform complete scan
device_info = scanner.scan()

# Get specific information
system_info = scanner.get_specific_info("system")
cpu_info = scanner.get_specific_info("cpu")
memory_info = scanner.get_specific_info("memory")
```

### Get Information as JSON

```python
from device_scanner import DeviceScanner

scanner = DeviceScanner()
scanner.scan()

# Get JSON output
json_output = scanner.get_device_json(indent=2)
print(json_output)
```

### Get Information as Dictionary

```python
from device_scanner import DeviceScanner

scanner = DeviceScanner()
scanner.scan()

# Get dictionary output
device_dict = scanner.get_device_dict()
print(device_dict)
```

### List Available APIs

```python
from device_scanner import DeviceScanner

scanner = DeviceScanner()
apis = scanner.list_available_apis()

for api_name, api_details in apis.items():
    print(f"{api_name}: {api_details['description']}")
```

### Get Specific Device Information

```python
from device_scanner import DeviceScanner

scanner = DeviceScanner()

# Get CPU information
cpu_info = scanner.get_specific_info("cpu")
print(f"Cores: {cpu_info['logical_cores']}")
print(f"Usage: {cpu_info['cpu_percent']}%")

# Get memory information
memory_info = scanner.get_specific_info("memory")
print(f"Total RAM: {memory_info['total_gb']} GB")
print(f"Used RAM: {memory_info['used_gb']} GB")
```

"""
        return markdown

    def generate_full_markdown(self) -> str:
        """
        Generate complete markdown report
        
        Returns:
            Complete markdown string
        """
        markdown = self.generate_header()
        markdown += self.generate_system_info_section()
        markdown += self.generate_cpu_section()
        markdown += self.generate_memory_section()
        markdown += self.generate_gpu_section()
        markdown += self.generate_disk_section()
        markdown += self.generate_network_section()
        markdown += self.generate_process_section()
        markdown += self.generate_uptime_section()
        markdown += self.generate_api_reference_section()
        markdown += self.generate_code_examples_section()
        
        return markdown

    def save_to_file(self, filepath: str) -> bool:
        """
        Save markdown report to file
        
        Args:
            filepath: Path to save the markdown file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate_full_markdown())
            return True
        except Exception as e:
            print(f"Error saving markdown: {e}")
            return False
