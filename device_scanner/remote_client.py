"""
遠端客戶端模塊 - 連接並控制遠端測試服務

此模塊提供以下功能：
- 連接到遠端測試服務
- 執行遠端掃描
- 查詢遠端測試結果
- 下載和管理結果
- 在本地顯示遠端結果
"""

import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime


class RemoteClient:
    """遠端測試客戶端類"""

    def __init__(self, host: str = "localhost", port: int = 3388):
        """
        初始化遠端客戶端

        Args:
            host: 遠端服務器主機名或 IP
            port: 遠端服務器端口
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.timeout = 60

    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """
        發送 HTTP 請求到遠端服務器

        Args:
            method: HTTP 方法 (GET, POST, DELETE)
            endpoint: API 端點
            data: 請求數據

        Returns:
            響應數據或錯誤信息
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            elif method == "DELETE":
                response = requests.delete(url, timeout=self.timeout)
            else:
                return {"status": "error", "message": f"不支持的方法: {method}"}

            return response.json()
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": f"無法連接到服務器: {self.base_url}",
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "請求超時",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def check_health(self) -> Dict[str, Any]:
        """
        檢查遠端服務器健康狀態

        Returns:
            健康檢查結果
        """
        return self._request("GET", "/api/health")

    def scan_device(self, test_name: str = "device_scan", scan_type: str = "full") -> Dict[str, Any]:
        """
        在遠端執行設備掃描

        Args:
            test_name: 測試名稱
            scan_type: 掃描類型 ('full' 或特定類型)

        Returns:
            掃描開始結果，包含 test_id
        """
        data = {
            "test_name": test_name,
            "scan_type": scan_type,
        }
        return self._request("POST", "/api/scan", data)

    def get_scan_result(self, test_id: str) -> Dict[str, Any]:
        """
        獲取遠端掃描結果

        Args:
            test_id: 測試 ID

        Returns:
            掃描結果或錯誤信息
        """
        return self._request("GET", f"/api/scan/{test_id}")

    def get_result_summary(self, test_id: str) -> Dict[str, Any]:
        """
        獲取遠端掃描結果摘要（不含完整數據）

        Args:
            test_id: 測試 ID

        Returns:
            結果摘要或錯誤信息
        """
        return self._request("GET", f"/api/results/summary/{test_id}")

    def list_results(self, limit: int = None) -> Dict[str, Any]:
        """
        列出遠端服務器上的所有測試結果

        Args:
            limit: 限制返回的數量（可選）

        Returns:
            結果列表或錯誤信息
        """
        endpoint = "/api/results"
        if limit:
            endpoint += f"?limit={limit}"
        return self._request("GET", endpoint)

    def delete_result(self, test_id: str) -> Dict[str, Any]:
        """
        刪除遠端測試結果

        Args:
            test_id: 測試 ID

        Returns:
            刪除結果或錯誤信息
        """
        return self._request("DELETE", f"/api/results/{test_id}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        獲取遠端服務器統計信息

        Returns:
            統計信息或錯誤信息
        """
        return self._request("GET", "/api/statistics")

    def list_available_apis(self) -> Dict[str, Any]:
        """
        列出遠端服務器上的可用 API

        Returns:
            API 列表或錯誤信息
        """
        return self._request("GET", "/api/apis")

    def save_result_locally(self, test_id: str, output_file: str) -> bool:
        """
        從遠端下載結果並保存到本地文件

        Args:
            test_id: 測試 ID
            output_file: 本地輸出文件路徑

        Returns:
            True 如果成功，False 如果失敗
        """
        result = self.get_scan_result(test_id)

        if result.get("status") == "error":
            print(f"❌ 下載失敗: {result.get('message')}")
            return False

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"✅ 結果已保存: {output_file}")
            return True
        except Exception as e:
            print(f"❌ 保存失敗: {str(e)}")
            return False

    def print_result_summary(self, test_id: str):
        """
        打印遠端掃描結果的摘要

        Args:
            test_id: 測試 ID
        """
        summary = self.get_result_summary(test_id)

        if summary.get("status") == "error":
            print(f"❌ 錯誤: {summary.get('message')}")
            return

        print("\n" + "=" * 60)
        print(f"📋 測試結果摘要")
        print("=" * 60)

        print(f"測試 ID: {summary.get('test_id')}")
        print(f"測試名稱: {summary.get('test_name')}")
        print(f"時間: {summary.get('timestamp')}")

        summary_data = summary.get('summary', {})

        # 系統信息
        system = summary_data.get('system', {})
        print(f"\n🖥️  系統信息:")
        print(f"   平台: {system.get('platform', 'N/A')}")
        print(f"   主機名: {system.get('hostname', 'N/A')}")
        print(f"   Python 版本: {system.get('python_version', 'N/A')}")

        # CPU 信息
        cpu = summary_data.get('cpu', {})
        print(f"\n⚙️  CPU 信息:")
        print(f"   物理核心: {cpu.get('physical_cores', 'N/A')}")
        print(f"   邏輯核心: {cpu.get('logical_cores', 'N/A')}")
        print(f"   使用率: {cpu.get('cpu_percent', 'N/A')}%")

        # 內存信息
        memory = summary_data.get('memory', {})
        print(f"\n💾 內存信息:")
        print(f"   總大小: {memory.get('total_gb', 'N/A')} GB")
        print(f"   已用: {memory.get('used_gb', 'N/A')} GB")
        print(f"   使用率: {memory.get('percent', 'N/A')}%")

        # 存儲信息
        disk = summary_data.get('disk', {})
        print(f"\n💿 存儲信息:")
        print(f"   總大小: {disk.get('total_gb', 'N/A')} GB")

        print("\n" + "=" * 60)


def create_remote_client(host: str = "localhost", port: int = 3388) -> RemoteClient:
    """
    創建遠端客戶端實例

    Args:
        host: 遠端服務器主機名或 IP
        port: 遠端服務器端口，默認 3388

    Returns:
        RemoteClient 實例
    """
    return RemoteClient(host=host, port=port)
