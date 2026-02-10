"""
Device Scanner Module - Orchestrates device scanning and API documentation generation
"""

from typing import Dict, Any
from .device_info import DeviceInfo


class DeviceScanner:
    """
    Main scanner class that orchestrates device information collection
    and API documentation generation
    """

    def __init__(self):
        """Initialize the device scanner"""
        self.device_info = DeviceInfo()
        self.available_apis = self._define_apis()

    def _define_apis(self) -> Dict[str, Dict[str, Any]]:
        """
        Define all available API methods and their details
        
        Returns:
            Dictionary of available APIs with descriptions
        """
        return {
            "get_system_info": {
                "description": "Retrieve operating system and platform information",
                "returns": "System platform, processor, architecture, Python version, hostname",
                "category": "System",
            },
            "get_cpu_info": {
                "description": "Retrieve CPU specifications and usage",
                "returns": "Physical/logical cores, frequency, CPU usage percentage",
                "category": "CPU",
            },
            "get_memory_info": {
                "description": "Retrieve RAM and memory usage information",
                "returns": "Total, available, used memory in GB, memory percentage",
                "category": "Memory",
            },
            "get_gpu_info": {
                "description": "Retrieve GPU information if available",
                "returns": "GPU name, load, memory usage, temperature",
                "category": "GPU",
            },
            "get_disk_info": {
                "description": "Retrieve disk partitions and usage information",
                "returns": "Disk device, mount point, total/used/free space, usage percentage",
                "category": "Storage",
            },
            "get_network_info": {
                "description": "Retrieve network interface information",
                "returns": "Network interface names, IP addresses, netmask, broadcast",
                "category": "Network",
            },
            "get_process_info": {
                "description": "Retrieve top processes by CPU and memory usage",
                "returns": "Top running processes with PID, name, CPU and memory usage",
                "category": "Process",
            },
            "get_uptime": {
                "description": "Retrieve system uptime and boot time",
                "returns": "System uptime in days/hours/minutes, boot timestamp",
                "category": "System",
            },
            "scan_all": {
                "description": "Perform complete device scan",
                "returns": "All device information combined",
                "category": "Scan",
            },
        }

    def scan(self) -> Dict[str, Any]:
        """
        Perform complete device scan
        
        Returns:
            Complete device information
        """
        return self.device_info.scan_all()

    def get_specific_info(self, info_type: str) -> Dict[str, Any]:
        """
        Get specific device information
        
        Args:
            info_type: Type of information (system, cpu, memory, gpu, disk, network, process, uptime)
            
        Returns:
            Specific device information
        """
        methods = {
            "system": self.device_info.get_system_info,
            "cpu": self.device_info.get_cpu_info,
            "memory": self.device_info.get_memory_info,
            "gpu": self.device_info.get_gpu_info,
            "disk": self.device_info.get_disk_info,
            "network": self.device_info.get_network_info,
            "process": self.device_info.get_process_info,
            "uptime": self.device_info.get_uptime,
        }
        
        if info_type in methods:
            return methods[info_type]()
        else:
            return {"error": f"Unknown info type: {info_type}"}

    def list_available_apis(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available API methods
        
        Returns:
            Dictionary of available APIs with metadata
        """
        return self.available_apis

    def get_device_json(self, indent: int = 2) -> str:
        """
        Get device information in JSON format
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string of device information
        """
        return self.device_info.to_json(indent)

    def get_device_dict(self) -> Dict[str, Any]:
        """
        Get device information as dictionary
        
        Returns:
            Device information dictionary
        """
        return self.device_info.to_dict()
