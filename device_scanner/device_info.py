"""
Device Information Module - Collects system and hardware device information
"""

import platform
import psutil
import json
from typing import Dict, Any, List
import subprocess
import os


class DeviceInfo:
    """Gathers comprehensive device information from the system"""

    def __init__(self):
        """Initialize device info collector"""
        self.info = {}

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            Dict containing:
            - platform: Operating system
            - processor: CPU model
            - architecture: System architecture
            - python_version: Python version
            - hostname: Computer name
        """
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
        }

    def get_cpu_info(self) -> Dict[str, Any]:
        """
        Get CPU information
        
        Returns:
            Dict containing:
            - physical_cores: Number of physical CPU cores
            - logical_cores: Number of logical CPU cores
            - cpu_freq: CPU frequency
            - cpu_percent: Current CPU usage percentage
        """
        try:
            return {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "cpu_freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                "cpu_percent": psutil.cpu_percent(interval=1),
                "per_cpu_percent": psutil.cpu_percent(interval=1, percpu=True),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_memory_info(self) -> Dict[str, Any]:
        """
        Get memory information
        
        Returns:
            Dict containing:
            - total_gb: Total RAM in GB
            - available_gb: Available RAM in GB
            - used_gb: Used RAM in GB
            - percent: Memory usage percentage
        """
        try:
            mem = psutil.virtual_memory()
            return {
                "total_gb": round(mem.total / (1024 ** 3), 2),
                "available_gb": round(mem.available / (1024 ** 3), 2),
                "used_gb": round(mem.used / (1024 ** 3), 2),
                "percent": mem.percent,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_gpu_info(self) -> Dict[str, Any]:
        """
        Get GPU information
        
        Returns:
            Dict containing GPU details if available
        """
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            gpu_list = []
            for gpu in gpus:
                gpu_list.append({
                    "id": gpu.id,
                    "name": gpu.name,
                    "load_percent": gpu.load * 100,
                    "memory_total_mb": gpu.memoryTotal,
                    "memory_used_mb": gpu.memoryUsed,
                    "memory_free_mb": gpu.memoryFree,
                    "temperature": gpu.temperature,
                })
            return {"gpus": gpu_list} if gpu_list else {"gpus": []}
        except ImportError:
            return {"gpus": [], "note": "GPUtil not installed"}
        except Exception as e:
            return {"error": str(e)}

    def get_disk_info(self) -> Dict[str, Any]:
        """
        Get disk information
        
        Returns:
            Dict containing disk partition information
        """
        try:
            disks = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks[partition.device] = {
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024 ** 3), 2),
                        "used_gb": round(usage.used / (1024 ** 3), 2),
                        "free_gb": round(usage.free / (1024 ** 3), 2),
                        "percent": usage.percent,
                    }
                except PermissionError:
                    pass
            return disks
        except Exception as e:
            return {"error": str(e)}

    def get_network_info(self) -> Dict[str, Any]:
        """
        Get network interface information
        
        Returns:
            Dict containing network interface details
        """
        try:
            networks = {}
            net_if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addrs in net_if_addrs.items():
                networks[interface_name] = []
                for addr in interface_addrs:
                    networks[interface_name].append({
                        "family": addr.family.name,
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                    })
            return networks
        except Exception as e:
            return {"error": str(e)}

    def get_process_info(self, top_n: int = 5) -> Dict[str, Any]:
        """
        Get top N processes by CPU and memory usage
        
        Args:
            top_n: Number of top processes to return
            
        Returns:
            Dict containing top processes
        """
        try:
            processes_cpu = []
            processes_mem = []

            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes_cpu.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": proc.info['memory_percent'],
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort and get top processes
            top_cpu = sorted(processes_cpu, key=lambda x: x['cpu_percent'], reverse=True)[:top_n]
            top_mem = sorted(processes_cpu, key=lambda x: x['memory_percent'], reverse=True)[:top_n]

            return {
                "top_cpu": top_cpu,
                "top_memory": top_mem,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_uptime(self) -> Dict[str, Any]:
        """
        Get system uptime
        
        Returns:
            Dict containing uptime information
        """
        try:
            boot_time = psutil.boot_time()
            import datetime
            uptime_seconds = (datetime.datetime.now().timestamp() - boot_time)
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            return {
                "boot_timestamp": boot_time,
                "uptime_days": days,
                "uptime_hours": hours,
                "uptime_minutes": minutes,
                "uptime_seconds": int(uptime_seconds),
            }
        except Exception as e:
            return {"error": str(e)}

    def scan_all(self) -> Dict[str, Any]:
        """
        Scan all device information
        
        Returns:
            Complete device information dictionary
        """
        self.info = {
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "gpu": self.get_gpu_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "process": self.get_process_info(),
            "uptime": self.get_uptime(),
        }
        return self.info

    def to_dict(self) -> Dict[str, Any]:
        """Return collected information as dictionary"""
        return self.info

    def to_json(self, indent: int = 2) -> str:
        """Return collected information as JSON string"""
        return json.dumps(self.info, indent=indent, default=str)
