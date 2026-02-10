# 設備掃描遠端測試工具 - 繁體中文文檔

**Device Scanner Remote Test Tool - Traditional Chinese Documentation**

---

## 📖 目錄

1. [項目概述](#項目概述)
2. [功能特性](#功能特性)
3. [安裝與配置](#安裝與配置)
4. [快速開始](#快速開始)
5. [遠端服務器](#遠端服務器)
6. [遠端客戶端](#遠端客戶端)
7. [API 文檔](#api-文檔)
8. [使用示例](#使用示例)
9. [結果管理](#結果管理)
10. [程式說明](#程式說明)

---

## 項目概述

這是一個完整的 Python 設備掃描和遠端測試工具。它可以：

- ✅ **本地掃描**: 掃描本機設備信息（CPU、內存、磁盤、網絡等）
- ✅ **遠端服務**: 在固定端口 (3388) 上提供遠端測試服務
- ✅ **遠端客戶端**: 連接到遠端服務並執行掃描
- ✅ **結果管理**: 自動保存和管理測試結果到 `results` 文件夾
- ✅ **Markdown 報告**: 自動生成美化的 Markdown 文檔
- ✅ **JSON 導出**: 以 JSON 格式保存詳細測試數據
- ✅ **Web UI**: 通過瀏覽器查看和管理結果

## 功能特性

### 🖥️ 設備掃描功能

| 功能 | 描述 |
|------|------|
| 系統信息 | 操作系統、平台、架構、主機名等 |
| CPU 信息 | 物理/邏輯核心、頻率、使用率 |
| 內存信息 | 總大小、已用、可用、使用百分比 |
| GPU 信息 | GPU 型號、負載、內存、溫度 |
| 存儲信息 | 磁盤分區、大小、已用空間、使用率 |
| 網絡信息 | 網絡接口、IP 地址、子網掩碼 |
| 進程信息 | 進程列表、CPU 和內存使用率 |
| 運行時間 | 系統啟動時間和運行時長 |

### 🌐 遠端服務特性

| 特性 | 說明 |
|------|------|
| 端口號 | 3388（可自定義） |
| 協議 | HTTP REST API |
| Web UI | 內置完整的 Web 用戶界面 |
| 結果存儲 | 自動保存到 `results` 文件夾 |
| 數據格式 | JSON 格式存儲 |
| 並發支持 | 支持多客戶端連接 |

### 💾 結果管理特性

| 特性 | 說明 |
|------|------|
| 唯一 ID | 每個結果都有唯一標識符 |
| 時間戳 | 自動記錄掃描時間 |
| 自動保存 | 掃描完成後自動保存 |
| 快速查詢 | 支持按 ID 快速查找 |
| 統計信息 | 提供結果統計和大小信息 |

---

## 安裝與配置

### 1️⃣ 前置要求

- Python 3.7 或更高版本
- pip 包管理工具
- Linux/macOS/Windows 操作系統

### 2️⃣ 安裝步驟

```bash
# 進入項目目錄
cd test_tool

# 安裝依賴包
pip install -r requirements.txt
```

### 3️⃣ 依賴包說明

```
psutil>=5.9.0      # 系統和進程信息
GPUtil>=1.4.0      # GPU 信息（可選）
Flask>=2.0.0       # Web 框架
requests>=2.28.0   # HTTP 客戶端
```

### 4️⃣ 項目結構

```
test_tool/
├── device_scanner/              # 主要模塊包
│   ├── __init__.py
│   ├── device_info.py           # 設備信息收集模塊
│   ├── scanner.py               # 掃描器主類
│   ├── markdown_generator.py     # Markdown 生成器
│   ├── result_manager.py         # 結果管理模塊
│   ├── remote_server.py          # 遠端服務器模塊
│   └── remote_client.py          # 遠端客戶端模塊
│
├── main.py                       # 本地命令行工具
├── remote_server.py              # 遠端服務器啟動腳本
├── remote_client.py              # 遠端客戶端腳本
├── results/                      # 測試結果存儲目錄
├── requirements.txt              # 依賴清單
├── README.md                     # 英文文檔
└── README_zh_TW.md              # 繁體中文文檔
```

---

## 快速開始

### 🚀 本地快速掃描

```bash
# 執行完整掃描並打印結果
python3 main.py --scan-all

# 獲取 CPU 信息
python3 main.py --info cpu

# 獲取內存信息
python3 main.py --info memory

# 列出所有可用 API
python3 main.py --list-apis
```

### 📝 生成報告

```bash
# 生成 Markdown 報告
python3 main.py --markdown device_info.md

# 導出 JSON 數據
python3 main.py --json device_info.json
```

### 🌐 遠端服務快速開始

```bash
# 終端 1：啟動遠端服務
python3 remote_server.py

# 終端 2：在瀏覽器中打開
http://localhost:3388

# 或使用客戶端執行掃描
python3 remote_client.py --scan

# 查看結果列表
python3 remote_client.py --list

# 查看詳細結果
python3 remote_client.py --summary <test_id>

# 下載結果
python3 remote_client.py --save <test_id> --output result.json
```

---

## 遠端服務器

### 🚀 啟動服務器

```bash
# 使用默認設置（端口 3388）
python3 remote_server.py

# 指定自定義端口
python3 remote_server.py --port 3389

# 調試模式運行
python3 remote_server.py --debug

# 自定義結果目錄
python3 remote_server.py --results-dir /custom/path
```

### 📋 服務器啟動信息

當服務器成功啟動時，會顯示：

```
╔═══════════════════════════════════════════════════════════╗
║         遠端設備掃描測試服務                              ║
║         Remote Device Scanner Service                    ║
╚═══════════════════════════════════════════════════════════╝

📍 服務運行信息:
   URL: http://localhost:3388
   API: http://localhost:3388/api
   結果存儲目錄: /path/to/results

🔌 API 端點: [列出所有端點]
⌨️  快捷命令: [列出常用命令]
```

### 🌐 訪問 Web UI

在瀏覽器中打開：`http://localhost:3388`

Web UI 提供：
- 🔍 一鍵掃描按鈕
- 📊 結果列表查看
- 📈 統計信息查看
- 📜 API 文檔
- ⌨️ 快速命令示例
#### 📋 結果列表操作

在 Web UI 的結果列表中，每個結果都有三個操作按鈕：

| 按鈕 | 功能 | 說明 |
|------|------|------|
| **👁️ 查看** | 查看結果詳情 | 在新頁面中查看完整的掃描結果，包括系統信息、CPU、內存、存儲、網絡等詳細數據 |
| **⬇️ 下載** | 下載結果文件 | 以 JSON 格式下載測試結果，可用於離線分析或存檔 |
| **🗑️ 刪除** | 刪除結果 | 永久刪除該測試結果（需確認） |

#### 📄 結果詳情頁面

點擊「查看」按鈕進入結果詳情頁面，可以看到：

- **系統信息**
  - 操作系統平台
  - 處理器架構
  - Python 版本
  - 主機名等

- **CPU 信息**
  - 物理核心數
  - 邏輯核心數
  - CPU 頻率
  - 當前使用率

- **內存信息**
  - 總內存大小
  - 已用內存
  - 可用內存
  - 使用百分比

- **存儲信息**
  - 磁盤設備列表
  - 掛載點
  - 文件系統類型
  - 容量和使用情況

- **網絡接口**
  - 接口名稱
  - IP 地址
  - 子網掩碼
  - 地址族

- **系統運行時間**
  - 開機時間
  - 運行時長

#### 🔄 完整 JSON 數據查看

在詳情頁面點擊「查看完整 JSON」按鈕可以切換到 JSON 數據視圖，顯示所有原始測試數據。
---

## 遠端客戶端

### 💻 客戶端命令

```bash
# 檢查服務器健康狀態
python3 remote_client.py --health

# 執行遠端掃描
python3 remote_client.py --scan

# 列出所有結果
python3 remote_client.py --list

# 查看結果摘要
python3 remote_client.py --summary <test_id>

# 查看完整結果
python3 remote_client.py --get <test_id>

# 保存結果到本地
python3 remote_client.py --save <test_id> --output ~/my_result.json

# 獲取統計信息
python3 remote_client.py --statistics

# 連接到遠端服務器
python3 remote_client.py --host 192.168.1.100 --port 3388 --health
```

### 📊 客戶端功能表

| 命令 | 功能 | 例子 |
|------|------|------|
| `--health` | 檢查服務器狀態 | `python3 remote_client.py --health` |
| `--scan` | 執行掃描 | `python3 remote_client.py --scan` |
| `--list` | 列出結果 | `python3 remote_client.py --list --limit 10` |
| `--get` | 獲取特定結果 | `python3 remote_client.py --get abc123` |
| `--summary` | 結果摘要 | `python3 remote_client.py --summary abc123` |
| `--save` | 保存結果 | `python3 remote_client.py --save abc123 --output result.json` |
| `--delete` | 刪除結果 | `python3 remote_client.py --delete abc123` |
| `--apis` | 列出 API | `python3 remote_client.py --apis` |
| `--statistics` | 統計信息 | `python3 remote_client.py --statistics` |

---

## API 文檔

### 🔌 REST API 端點

#### 1. 執行掃描
```
POST /api/scan

請求體：
{
    "test_name": "device_scan",      // 可選：測試名稱
    "scan_type": "full"               // 可選：掃描類型
}

響應：
{
    "status": "success",
    "test_id": "abc-123-def",
    "filename": "device_scan_20260210_123456_abc12345.json"
}
```

#### 2. 獲取掃描結果（JSON API）
```
GET /api/scan/<test_id>

響應：
{
    "test_id": "abc-123-def",
    "test_name": "device_scan",
    "timestamp": "2026-02-10T13:31:24.123456",
    "scan_data": {
        "system": {...},
        "cpu": {...},
        "memory": {...},
        ...
    }
}
```

#### 3. 查看結果詳情頁面（HTML）
```
GET /results/<test_id>

返回：
HTML 格式的結果詳情頁面，包含：
- 系統信息卡片
- CPU 信息卡片
- 內存信息卡片
- 存儲信息表格
- 網絡接口表格
- 系統運行時間信息
- 查看完整 JSON 按鈕
- 下載結果按鈕
```

#### 4. 下載結果文件
```
GET /api/download/<test_id>

返回：
JSON 格式的結果文件下載
檔案名：{test_name}_{timestamp}_{test_id_prefix}.json
```

#### 5. 列出所有結果
```
GET /api/results?limit=10

響應：
{
    "status": "success",
    "count": 10,
    "results": [
        {
            "test_id": "abc-123-def",
            "test_name": "device_scan",
            "timestamp": "2026-02-10T13:31:24...",
            "filename": "device_scan_..."
        }
    ]
}
```

#### 6. 獲取結果摘要
```
GET /api/results/summary/<test_id>

響應：
{
    "test_id": "abc-123-def",
    "summary": {
        "system": {...},
        "cpu": {
            "physical_cores": 4,
            "logical_cores": 8,
            "cpu_percent": 15.2
        },
        "memory": {
            "total_gb": 16.0,
            "used_gb": 8.5,
            "percent": 53.1
        }
    }
}
```

#### 7. 刪除結果
```
DELETE /api/results/<test_id>

響應：
{
    "status": "success",
    "message": "結果已刪除"
}
```

#### 8. 獲取統計信息
```
GET /api/statistics

響應：
{
    "status": "success",
    "total_results": 42,
    "total_size_mb": 12.3,
    "results_directory": "/path/to/results"
}
```

#### 9. 列出可用 API
```
GET /api/apis

響應：
{
    "status": "success",
    "apis": {
        "get_cpu_info": {
            "description": "...",
            "returns": "...",
            "category": "CPU"
        },
        ...
    }
}
```

#### 10. 健康檢查
```
GET /api/health

響應：
{
    "status": "healthy",
    "timestamp": "2026-02-10T13:31:24...",
    "port": 3388
}
```

---

## 使用示例

### 📌 使用場景 1: 本地設備掃描

**目標**: 掃描本機設備信息並生成報告

```bash
# 1. 執行完整掃描
python3 main.py --scan-all

# 2. 生成 Markdown 報告
python3 main.py --markdown device_report.md

# 3. 導出 JSON 數據
python3 main.py --json device_data.json

# 4. 查看報告
cat device_report.md
```

### 📌 使用場景 2: 遠端服務掃描

**目標**: 在一台服務器上啟動遠端測試服務，從另一台機器操控

**服務器端**:
```bash
# 服務器機器 (IP: 192.168.1.100)
python3 remote_server.py --port 3388
```

**客戶端**:
```bash
# 客戶端機器
# 1. 檢查服務器
python3 remote_client.py --host 192.168.1.100 --port 3388 --health

# 2. 執行遠端掃描
python3 remote_client.py --host 192.168.1.100 --scan

# 3. 查看結果
python3 remote_client.py --host 192.168.1.100 --list

# 4. 獲取詳細結果
python3 remote_client.py --host 192.168.1.100 --get abc123def

# 5. 保存到本地
python3 remote_client.py --host 192.168.1.100 --save abc123def --output result.json
```

### 📌 使用場景 3: 使用 curl 命令測試 API

```bash
# 1. 檢查服務健康狀態
curl http://localhost:3388/api/health

# 2. 執行掃描
curl -X POST http://localhost:3388/api/scan

# 3. 獲取自定義名稱的掃描
curl -X POST http://localhost:3388/api/scan \
  -H "Content-Type: application/json" \
  -d '{"test_name":"my_test","scan_type":"full"}'

# 4. 列出所有結果
curl http://localhost:3388/api/results

# 5. 獲取特定結果
curl http://localhost:3388/api/scan/abc123def

# 6. 獲取統計信息
curl http://localhost:3388/api/statistics

# 7. 查看可用 API
curl http://localhost:3388/api/apis
```

### 📌 使用場景 4: Python 腳本調用

```python
#!/usr/bin/env python3
"""遠端測試 Python 腳本示例"""

from device_scanner.remote_client import create_remote_client

# 創建客戶端
client = create_remote_client(host="localhost", port=3388)

# 檢查服務器健康
health = client.check_health()
print(f"服務器狀態: {health['status']}")

# 執行掃描
result = client.scan_device(test_name="my_scan", scan_type="full")
test_id = result['test_id']
print(f"掃描已開始，ID: {test_id}")

# 獲取結果摘要
summary = client.get_result_summary(test_id)
print(f"CPU 核心數: {summary['summary']['cpu']['logical_cores']}")
print(f"內存大小: {summary['summary']['memory']['total_gb']} GB")

# 列出所有結果
results = client.list_results(limit=10)
print(f"共有 {results['count']} 個結果")

# 保存結果到本地
client.save_result_locally(test_id, "my_result.json")
```

---

## 結果管理

### 📁 結果存儲結構

```
results/
├── device_scan_20260210_123456_abc12345.json
├── device_scan_20260210_130100_def67890.json
├── device_scan_20260210_131500_ghi11111.json
└── device_scan_20260210_132000_jkl22222.json
```

### 📊 結果文件格式

每個結果文件都是 JSON 格式，包含：

```json
{
  "test_id": "abc12345-def6-7890-ghi1-1111jkl22222",
  "test_name": "device_scan",
  "timestamp": "2026-02-10T13:31:24.123456",
  "scan_data": {
    "system": {
      "platform": "Linux",
      "processor": "x86_64",
      ...
    },
    "cpu": {
      "physical_cores": 4,
      "logical_cores": 8,
      ...
    },
    "memory": {
      "total_gb": 16.0,
      "used_gb": 8.5,
      ...
    },
    ...
  },
  "filename": "device_scan_20260210_123456_abc12345.json"
}
```

### 🔍 查詢結果

```python
from device_scanner.result_manager import ResultManager

manager = ResultManager(results_dir="results")

# 列出所有結果
all_results = manager.list_results()
print(f"共有 {all_results['count']} 個結果")

# 加載特定結果
result = manager.load_result("abc12345-def6-7890")
print(result['scan_data'])

# 獲取結果摘要
summary = manager.get_result_summary("abc12345-def6-7890")
print(summary['summary']['cpu'])

# 獲取統計信息
stats = manager.get_statistics()
print(f"總大小: {stats['total_size_mb']} MB")
```

---

## 程式說明

### 📚 模塊架構

#### 1. `device_info.py` - 設備信息收集模塊

**用途**: 收集系統設備信息

**主要類**: `DeviceInfo`

**核心方法**:

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `get_system_info()` | 獲取系統信息 | dict |
| `get_cpu_info()` | 獲取 CPU 信息 | dict |
| `get_memory_info()` | 獲取內存信息 | dict |
| `get_gpu_info()` | 獲取 GPU 信息 | dict |
| `get_disk_info()` | 獲取磁盤信息 | dict |
| `get_network_info()` | 獲取網絡信息 | dict |
| `get_process_info()` | 獲取進程信息 | dict |
| `get_uptime()` | 獲取運行時間 | dict |
| `scan_all()` | 執行完整掃描 | dict |
| `to_dict()` | 轉換為字典 | dict |
| `to_json()` | 轉換為 JSON | str |

**使用示例**:
```python
from device_scanner import DeviceInfo

device = DeviceInfo()
device.scan_all()

cpu_info = device.get_cpu_info()
print(f"邏輯核心數: {cpu_info['logical_cores']}")
```

#### 2. `scanner.py` - 掃描器編排模塊

**用途**: 統一的掃描界面和 API 管理

**主要類**: `DeviceScanner`

**核心方法**:

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `scan()` | 執行完整掃描 | dict |
| `get_specific_info()` | 獲取特定信息 | dict |
| `list_available_apis()` | 列出 API | dict |
| `get_device_json()` | JSON 格式 | str |
| `get_device_dict()` | 字典格式 | dict |

**使用示例**:
```python
from device_scanner import DeviceScanner

scanner = DeviceScanner()
scanner.scan()

apis = scanner.list_available_apis()
cpu = scanner.get_specific_info("cpu")
```

#### 3. `result_manager.py` - 結果管理模塊

**用途**: 管理和存儲測試結果

**主要類**: `ResultManager`

**核心方法**:

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `save_result()` | 保存結果到文件 | dict |
| `load_result()` | 加載結果 | dict |
| `list_results()` | 列出所有結果 | dict |
| `delete_result()` | 刪除結果 | dict |
| `get_result_summary()` | 獲取摘要 | dict |
| `get_statistics()` | 獲取統計 | dict |

**使用示例**:
```python
from device_scanner.result_manager import ResultManager

manager = ResultManager(results_dir="results")
scan_data = {...}  # 掃描數據
result = manager.save_result(scan_data, "my_test")
test_id = result['test_id']

loaded = manager.load_result(test_id)
summary = manager.get_result_summary(test_id)
```

#### 4. `markdown_generator.py` - Markdown 生成模塊

**用途**: 生成美化的 Markdown 報告

**主要類**: `MarkdownGenerator`

**核心方法**:

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `generate_full_markdown()` | 生成完整報告 | str |
| `generate_system_info_section()` | 系統信息段落 | str |
| `generate_cpu_section()` | CPU 信息段落 | str |
| `generate_memory_section()` | 內存信息段落 | str |
| `generate_api_reference_section()` | API 參考段落 | str |
| `save_to_file()` | 保存到文件 | bool |

#### 5. `remote_server.py` - 遠端服務器模塊

**用途**: 提供 Web 和 REST API 遠端服務

**主要類**: `RemoteServer`

**Flask 路由**:

| 路由 | 方法 | 功能 |
|------|------|------|
| `/` | GET | Web UI 主頁 |
| `/api/scan` | POST | 執行掃描 |
| `/api/scan/<id>` | GET | 獲取結果 |
| `/api/results` | GET | 列出結果 |
| `/api/results/<id>` | DELETE | 刪除結果 |
| `/api/statistics` | GET | 統計信息 |
| `/api/health` | GET | 健康檢查 |

**使用示例**:
```python
from device_scanner.remote_server import create_remote_server

server = create_remote_server(port=3388, results_dir="results")
server.run(debug=False)
```

#### 6. `remote_client.py` - 遠端客戶端模塊

**用途**: 連接和控制遠端服務

**主要類**: `RemoteClient`

**核心方法**:

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `check_health()` | 健康檢查 | dict |
| `scan_device()` | 執行掃描 | dict |
| `get_scan_result()` | 獲取結果 | dict |
| `list_results()` | 列出結果 | dict |
| `save_result_locally()` | 保存到本地 | bool |
| `print_result_summary()` | 打印摘要 | None |

**使用示例**:
```python
from device_scanner.remote_client import create_remote_client

client = create_remote_client(host="localhost", port=3388)
client.check_health()
result = client.scan_device()
client.print_result_summary(result['test_id'])
```

---

## 常見問題

### Q1: 將遠端服務綁定到所有網卡？

**A**: 默認已綁定到 `0.0.0.0`，即所有 IP 地址都可訪問

### Q2: 如何修改端口號？

**A**: 
```bash
# 服務器
python3 remote_server.py --port 3389

# 客戶端
python3 remote_client.py --port 3389
```

### Q3: 結果文件如何備份？

**A**: 
```bash
# 複製整個 results 目錄
cp -r results results.backup
```

### Q4: 如何刪除所有舊結果？

**A**: 
```bash
# 使用客戶端逐個刪除
python3 remote_client.py --list | grep test_id

# 或直接刪除文件夾再重建
rm -rf results
mkdir results
```

### Q5: GPU 信息無法顯示？

**A**: 
- 確保已安裝 GPU 駕動程序
- 更新 GPUtil: `pip install --upgrade GPUtil`
- 某些系統可能不支持

---

## 許可證

此項目作為教育和測試用途提供。

---

## 技術支持

如有問題，請檢查：
1. 依賴包是否已正確安裝
2. 防火牆是否允許 3388 端口
3. Python 版本是否為 3.7 或更高

---

**最後更新**: 2026-02-10  
**版本**: 1.0.0  
**語言**: 繁體中文
