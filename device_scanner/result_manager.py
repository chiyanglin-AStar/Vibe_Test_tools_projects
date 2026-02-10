"""
結果管理模塊 - 管理和存儲測試結果

此模塊提供以下功能：
- 生成唯一的測試結果 ID
- 保存測試結果到文件
- 讀取和查詢測試結果
- 列出所有測試結果
- 刪除過期的測試結果
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
import hashlib
import uuid


class ResultManager:
    """測試結果管理器 - 負責結果的存儲和檢索"""

    def __init__(self, results_dir: str = "results"):
        """
        初始化結果管理器

        Args:
            results_dir: 存儲結果的目錄路徑
        """
        self.results_dir = results_dir
        self._ensure_results_dir()

    def _ensure_results_dir(self):
        """確保結果目錄存在"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir, exist_ok=True)

    def generate_result_id(self) -> str:
        """
        生成唯一的測試結果 ID

        Returns:
            唯一的結果 ID (UUID 格式)
        """
        return str(uuid.uuid4())

    def save_result(self, scan_data: Dict[str, Any], test_name: str = "device_scan",
                    test_id: str = None) -> Dict[str, Any]:
        """
        保存測試結果到文件

        Args:
            scan_data: 掃描數據字典
            test_name: 測試名稱，默認為 'device_scan'
            test_id: 自定義測試 ID，若不提供則自動生成

        Returns:
            包含結果信息的字典
        """
        if test_id is None:
            test_id = self.generate_result_id()

        # 生成結果文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_filename = f"{test_name}_{timestamp}_{test_id[:8]}.json"
        result_path = os.path.join(self.results_dir, result_filename)

        # 構建結果數據
        result_data = {
            "test_id": test_id,
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "scan_data": scan_data,
            "filename": result_filename,
        }

        # 保存到文件
        try:
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, default=str)

            return {
                "status": "success",
                "test_id": test_id,
                "filename": result_filename,
                "filepath": result_path,
                "message": f"結果保存成功: {result_filename}",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"保存結果失敗: {str(e)}",
            }

    def load_result(self, result_id: str) -> Dict[str, Any]:
        """
        按 ID 加載測試結果

        Args:
            result_id: 測試結果 ID（可以是完整 UUID 或前 8 個字符）

        Returns:
            結果數據
        """
        # 查找文件 - 支持完整 ID 或前 8 個字符
        search_id = result_id[:8] if len(result_id) >= 8 else result_id
        
        for filename in os.listdir(self.results_dir):
            if search_id in filename and filename.endswith('.json'):
                filepath = os.path.join(self.results_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # 驗證完整 ID 是否匹配（如果提供了完整 ID）
                        if len(result_id) > 8 and data.get("test_id") != result_id:
                            continue
                        return data
                except Exception as e:
                    return {"status": "error", "message": str(e)}

        return {"status": "error", "message": f"找不到結果 ID: {result_id}"}

    def list_results(self, limit: int = None) -> Dict[str, Any]:
        """
        列出所有測試結果

        Args:
            limit: 限制返回的數量，None 表示無限制

        Returns:
            結果列表
        """
        results = []
        try:
            files = sorted(
                os.listdir(self.results_dir),
                reverse=True  # 最新的在最前面
            )

            for filename in files:
                if filename.endswith('.json'):
                    filepath = os.path.join(self.results_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            results.append({
                                "test_id": data.get("test_id"),
                                "test_name": data.get("test_name"),
                                "timestamp": data.get("timestamp"),
                                "filename": data.get("filename"),
                            })
                    except Exception:
                        pass

                    if limit and len(results) >= limit:
                        break

            return {
                "status": "success",
                "count": len(results),
                "results": results,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def delete_result(self, result_id: str) -> Dict[str, Any]:
        """
        刪除特定的測試結果

        Args:
            result_id: 測試結果 ID（可以是完整 UUID 或前 8 個字符）

        Returns:
            刪除操作的結果
        """
        try:
            # 支持完整 ID 或前 8 個字符
            search_id = result_id[:8] if len(result_id) >= 8 else result_id
            
            for filename in os.listdir(self.results_dir):
                if search_id in filename and filename.endswith('.json'):
                    filepath = os.path.join(self.results_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # 驗證完整 ID 是否匹配（如果提供了完整 ID）
                            if len(result_id) > 8 and data.get("test_id") != result_id:
                                continue
                    except Exception:
                        pass
                    
                    os.remove(filepath)
                    return {
                        "status": "success",
                        "message": f"結果已刪除: {filename}",
                    }

            return {
                "status": "error",
                "message": f"找不到結果 ID: {result_id}",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"刪除失敗: {str(e)}",
            }

    def get_result_summary(self, result_id: str) -> Dict[str, Any]:
        """
        獲取測試結果摘要（不包括完整的掃描數據）

        Args:
            result_id: 測試結果 ID

        Returns:
            結果摘要
        """
        result = self.load_result(result_id)

        if result.get("status") == "error":
            return result

        # 提取關鍵信息
        scan_data = result.get("scan_data", {})
        summary = {
            "status": "success",
            "test_id": result.get("test_id"),
            "test_name": result.get("test_name"),
            "timestamp": result.get("timestamp"),
            "summary": {
                "system": scan_data.get("system", {}),
                "cpu": {
                    "physical_cores": scan_data.get("cpu", {}).get("physical_cores"),
                    "logical_cores": scan_data.get("cpu", {}).get("logical_cores"),
                    "cpu_percent": scan_data.get("cpu", {}).get("cpu_percent"),
                },
                "memory": {
                    "total_gb": scan_data.get("memory", {}).get("total_gb"),
                    "used_gb": scan_data.get("memory", {}).get("used_gb"),
                    "percent": scan_data.get("memory", {}).get("percent"),
                },
                "disk": {
                    "total_gb": sum(
                        disk.get("total_gb", 0) 
                        for disk in scan_data.get("disk", {}).values()
                    ),
                },
            },
        }

        return summary

    def get_statistics(self) -> Dict[str, Any]:
        """
        獲取結果統計信息

        Returns:
            統計信息
        """
        try:
            result_list = self.list_results()
            files = os.listdir(self.results_dir)
            json_files = [f for f in files if f.endswith('.json')]

            # 計算總大小
            total_size = 0
            for filename in json_files:
                filepath = os.path.join(self.results_dir, filename)
                total_size += os.path.getsize(filepath)

            return {
                "status": "success",
                "total_results": len(json_files),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "results_directory": os.path.abspath(self.results_dir),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
