# Device Scanner Test Tool

A comprehensive Python-based system device information scanner and test tool. This tool provides detailed information about system hardware, performance metrics, and available APIs for device testing and monitoring.

## 📋 Features

- **Complete Device Scanning**: Scan all system devices and hardware information
- **Multi-Category Information**: System, CPU, Memory, GPU, Disk, Network, Process, and Uptime data
- **API Documentation**: Automatic generation of available API methods documentation
- **Markdown Reports**: Generate beautiful markdown documentation of device information
- **JSON Export**: Export device information in JSON format for programmatic use
- **Command-Line Interface**: Easy-to-use CLI with multiple options
- **Performance Monitoring**: Real-time CPU, memory, and process monitoring

## 🚀 Quick Start

### Installation

1. Clone or navigate to the project:
```bash
cd test_tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### 1. Basic Device Scan
```bash
python main.py --scan-all
```

#### 2. Get Specific Information
```bash
# CPU information
python main.py --info cpu

# Memory information
python main.py --info memory

# Disk information
python main.py --info disk

# Network information
python main.py --info network

# System information
python main.py --info system

# GPU information
python main.py --info gpu

# Process information
python main.py --info process

# System uptime
python main.py --info uptime
```

#### 3. Generate Markdown Report
```bash
python main.py --markdown device_info.md
```

This will create a comprehensive markdown report with:
- Device properties and specifications
- Performance metrics
- API reference documentation
- Code examples

#### 4. Export as JSON
```bash
python main.py --json device_info.json
```

#### 5. List Available APIs
```bash
python main.py --list-apis
```

## 📚 Project Structure

```
test_tool/
├── device_scanner/           # Main package
│   ├── __init__.py          # Package initialization
│   ├── device_info.py       # Device information collection module
│   ├── scanner.py           # Main scanner orchestrator
│   └── markdown_generator.py # Markdown report generator
├── main.py                  # Main entry point and CLI
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Module Details

### device_scanner/device_info.py
**Purpose**: Collects detailed system and hardware information

**Key Methods**:
- `get_system_info()` - Operating system and platform information
- `get_cpu_info()` - CPU specifications and usage metrics
- `get_memory_info()` - RAM and memory usage information
- `get_gpu_info()` - GPU details if available
- `get_disk_info()` - Storage and partition information
- `get_network_info()` - Network interface details
- `get_process_info()` - Top processes by CPU and memory usage
- `get_uptime()` - System uptime and boot time
- `scan_all()` - Complete device scan
- `to_dict()` - Convert to dictionary format
- `to_json(indent)` - Convert to JSON string

### device_scanner/scanner.py
**Purpose**: Orchestrates device scanning and provides API documentation

**Key Methods**:
- `scan()` - Perform complete device scan
- `get_specific_info(info_type)` - Get specific information type
- `list_available_apis()` - List all available APIs
- `get_device_json(indent)` - Get device info in JSON format
- `get_device_dict()` - Get device info as dictionary

**Available Info Types**:
- system, cpu, memory, gpu, disk, network, process, uptime

### device_scanner/markdown_generator.py
**Purpose**: Generates comprehensive markdown documentation

**Key Methods**:
- `generate_full_markdown()` - Generate complete markdown report
- `generate_system_info_section()` - System information section
- `generate_cpu_section()` - CPU information section
- `generate_memory_section()` - Memory information section
- `generate_gpu_section()` - GPU information section
- `generate_disk_section()` - Disk information section
- `generate_network_section()` - Network information section
- `generate_process_section()` - Process information section
- `generate_uptime_section()` - Uptime information section
- `generate_api_reference_section()` - API documentation section
- `generate_code_examples_section()` - Code examples section
- `save_to_file(filepath)` - Save report to file

## 💻 Usage Examples

### In Python Script

```python
from device_scanner import DeviceScanner

# Create scanner instance
scanner = DeviceScanner()

# Perform complete scan
device_info = scanner.scan()

# Access specific information
cpu_info = scanner.get_specific_info("cpu")
print(f"CPU Cores: {cpu_info['logical_cores']}")

# Get JSON output
json_data = scanner.get_device_json()
print(json_data)

# List APIs
apis = scanner.list_available_apis()
for api_name, details in apis.items():
    print(f"{api_name}: {details['description']}")
```

### Markdown Report Generation

```python
from device_scanner import DeviceScanner
from device_scanner.markdown_generator import MarkdownGenerator

scanner = DeviceScanner()
device_info = scanner.scan()

generator = MarkdownGenerator(
    device_info, 
    scanner.list_available_apis()
)
generator.save_to_file("report.md")
```

## 📊 Generated Markdown Report

The generated markdown report includes:

1. **System Information**: OS, platform, processor, architecture, hostname
2. **CPU Details**: Physical cores, logical cores, frequency, usage percentage
3. **Memory Details**: Total, used, available RAM and usage percentage
4. **GPU Information**: GPU name, load, memory usage, temperature (if available)
5. **Storage Details**: Disk devices, mount points, total/used/free space
6. **Network Configuration**: Network interfaces, IP addresses, network masks
7. **Process Information**: Top processes by CPU and memory usage
8. **System Uptime**: Boot time and uptime duration
9. **API Reference**: Complete documentation of all available methods
10. **Code Examples**: Practical usage examples for each API

## 🔌 API Reference

All APIs are accessible through the `DeviceScanner` class:

### System APIs
- `get_system_info()` - Platform and OS information
- `get_uptime()` - System boot time and uptime

### Hardware APIs
- `get_cpu_info()` - CPU information and usage
- `get_memory_info()` - RAM information and usage
- `get_gpu_info()` - GPU information and status
- `get_disk_info()` - Storage information

### System APIs
- `get_network_info()` - Network interface information
- `get_process_info(top_n)` - Top processes by resource usage
- `scan_all()` - Complete device scan

### Utility APIs
- `list_available_apis()` - List all available methods
- `get_device_json(indent)` - JSON format output
- `get_device_dict()` - Dictionary format output

## ⚙️ Requirements

- Python 3.7+
- psutil >= 5.9.0 (system and process utilities)
- GPUtil >= 1.4.0 (GPU information - optional for non-GPU systems)

## 📝 Notes

- GPU information requires GPUtil library and compatible GPU drivers
- Some information may require elevated privileges on certain systems
- Network information includes all active network interfaces
- Process information shows top 5 processes by CPU and memory usage

## 🐛 Troubleshooting

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Permission Errors
Some system information may require elevated privileges:
```bash
# Linux/macOS
sudo python main.py --scan-all

# Windows (Run as Administrator)
python main.py --scan-all
```

### GPU Information Not Showing
- Ensure GPU drivers are installed
- Install/update GPUtil: `pip install --upgrade GPUtil`

## 📄 License

This project is provided as-is for educational and testing purposes.

## 🤝 Contributing

Feel free to extend this tool with additional features or API methods.

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-10
