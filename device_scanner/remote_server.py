"""
遠端服務器模塊 - Flask 遠端測試服務

此模塊提供以下功能：
- 在 port 3388 啟動 Flask 遠端服務
- 提供遠端掃描設備的 API 端點
- 存儲和管理測試結果
- 查詢測試結果和統計信息
- 提供 Web UI 查看結果

API 端點列表：
- POST /api/scan - 執行設備掃描
- GET /api/scan/<test_id> - 獲取掃描結果
- GET /api/results - 列出所有結果
- GET /api/results/summary/<test_id> - 獲取結果摘要
- GET /api/statistics - 獲取統計信息
- DELETE /api/results/<test_id> - 刪除結果
- GET /api/apis - 列出所有可用 API
- GET / - Web UI 主頁
"""

from flask import Flask, request, jsonify, render_template_string, send_file
from device_scanner import DeviceScanner
from .result_manager import ResultManager
import os
import json
from datetime import datetime
from typing import Dict, Any
from io import BytesIO


class RemoteServer:
    """遠端測試服務器類"""

    def __init__(self, port: int = 3388, results_dir: str = "results"):
        """
        初始化遠端服務器

        Args:
            port: 服務運行的端口，默認 3388
            results_dir: 結果存儲目錄
        """
        self.port = port
        self.results_dir = results_dir
        self.app = Flask(__name__)
        self.scanner = DeviceScanner()
        self.result_manager = ResultManager(results_dir)
        self._setup_routes()

    def _setup_routes(self):
        """設置 Flask 路由"""

        @self.app.route('/', methods=['GET'])
        def home():
            """Web UI 主頁"""
            return self._render_home_page()

        @self.app.route('/api/scan', methods=['POST'])
        def scan():
            """
            執行設備掃描 API 端點

            JSON 請求體（可選）:
            {
                "test_name": "自定義測試名稱",
                "scan_type": "full"  # 'full' 或特定類型
            }

            Returns:
                JSON: 掃描結果和測試 ID
            """
            try:
                data = request.get_json() or {}
                test_name = data.get("test_name", "device_scan")
                scan_type = data.get("scan_type", "full")

                # 執行掃描
                if scan_type == "full":
                    scan_data = self.scanner.scan()
                else:
                    scan_data = {scan_type: self.scanner.get_specific_info(scan_type)}

                # 保存結果
                result = self.result_manager.save_result(scan_data, test_name)

                return jsonify({
                    "status": "success",
                    "message": "掃描完成",
                    "test_id": result.get("test_id"),
                    "filename": result.get("filename"),
                }), 200

            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": str(e),
                }), 500

        @self.app.route('/api/scan/<test_id>', methods=['GET'])
        def get_scan_result(test_id):
            """
            獲取掃描結果 API 端點

            Args:
                test_id: 測試結果 ID

            Returns:
                JSON: 掃描結果詳細信息
            """
            result = self.result_manager.load_result(test_id)
            if result.get("status") == "error":
                return jsonify(result), 404
            return jsonify(result), 200

        @self.app.route('/api/results', methods=['GET'])
        def list_results():
            """
            列出所有測試結果 API 端點

            Query Parameters:
                limit: 限制返回的數量（可選）

            Returns:
                JSON: 結果列表
            """
            limit = request.args.get('limit', type=int)
            results = self.result_manager.list_results(limit=limit)
            return jsonify(results), 200

        @self.app.route('/api/results/summary/<test_id>', methods=['GET'])
        def get_result_summary(test_id):
            """
            獲取結果摘要 API 端點（不含完整掃描數據）

            Args:
                test_id: 測試結果 ID

            Returns:
                JSON: 結果摘要
            """
            summary = self.result_manager.get_result_summary(test_id)
            return jsonify(summary), 200

        @self.app.route('/api/results/<test_id>', methods=['DELETE'])
        def delete_result(test_id):
            """
            刪除測試結果 API 端點

            Args:
                test_id: 測試結果 ID

            Returns:
                JSON: 刪除結果
            """
            result = self.result_manager.delete_result(test_id)
            status_code = 200 if result.get("status") == "success" else 404
            return jsonify(result), status_code

        @self.app.route('/api/statistics', methods=['GET'])
        def get_statistics():
            """
            獲取統計信息 API 端點

            Returns:
                JSON: 統計信息
            """
            stats = self.result_manager.get_statistics()
            return jsonify(stats), 200

        @self.app.route('/api/apis', methods=['GET'])
        def list_apis():
            """
            列出所有可用 API 端點

            Returns:
                JSON: API 列表和描述
            """
            apis = self.scanner.list_available_apis()
            return jsonify({
                "status": "success",
                "apis": apis,
            }), 200

        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """
            健康檢查 API 端點

            Returns:
                JSON: 服務狀態
            """
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "port": self.port,
            }), 200

        @self.app.route('/results/<test_id>', methods=['GET'])
        def view_result(test_id):
            """
            查看測試結果詳情頁面

            Args:
                test_id: 測試結果 ID

            Returns:
                HTML: 結果詳情頁面
            """
            result = self.result_manager.load_result(test_id)
            if result.get("status") == "error":
                return f"<h1>❌ 錯誤</h1><p>{result.get('message')}</p>", 404

            return self._render_result_detail_page(result)

        @self.app.route('/api/download/<test_id>', methods=['GET'])
        def download_result(test_id):
            """
            下載測試結果文件

            Args:
                test_id: 測試結果 ID

            Returns:
                File: JSON 格式的結果文件下載
            """
            result = self.result_manager.load_result(test_id)
            if result.get("status") == "error":
                return jsonify(result), 404

            try:
                test_name = result.get("test_name", "device_scan")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{test_name}_{timestamp}_{test_id[:8]}.json"

                json_data = json.dumps(result, indent=2, default=str)
                data = BytesIO(json_data.encode('utf-8'))

                return send_file(
                    data,
                    mimetype='application/json',
                    as_attachment=True,
                    download_name=filename
                )
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500

    def _render_result_detail_page(self, result: Dict[str, Any]) -> str:
        """
        渲染測試結果詳情頁面

        Args:
            result: 測試結果數據

        Returns:
            HTML 字符串
        """
        test_id = result.get("test_id", "Unknown")
        test_name = result.get("test_name", "Unknown")
        timestamp = result.get("timestamp", "Unknown")
        scan_data = result.get("scan_data", {})

        html_template = """
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>測試結果詳情 - """ + test_name + """</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Microsoft YaHei', '微軟正黑體', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                
                .container {
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    overflow: hidden;
                }
                
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px 20px;
                }
                
                .header-content {
                    max-width: 1400px;
                    margin: 0 auto;
                }
                
                .header h1 {
                    font-size: 2em;
                    margin-bottom: 20px;
                }
                
                .header-info {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    font-size: 0.95em;
                }
                
                .header-info-item {
                    background: rgba(255,255,255,0.1);
                    padding: 15px;
                    border-radius: 5px;
                }
                
                .header-info-item strong {
                    display: block;
                    margin-bottom: 5px;
                    opacity: 0.9;
                }
                
                .header-info-item code {
                    font-family: 'Courier New', monospace;
                    background: rgba(0,0,0,0.2);
                    padding: 5px 10px;
                    border-radius: 3px;
                    word-break: break-all;
                }
                
                .content {
                    padding: 30px;
                }
                
                .button-group {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 30px;
                    flex-wrap: wrap;
                }
                
                button, a.button {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1em;
                    transition: all 0.3s;
                    text-decoration: none;
                    display: inline-block;
                }
                
                button:hover, a.button:hover {
                    background: #764ba2;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                
                .button.secondary {
                    background: #6c757d;
                }
                
                .button.secondary:hover {
                    background: #5a6268;
                }
                
                .section {
                    margin-bottom: 30px;
                }
                
                .section h2 {
                    color: #333;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                    font-size: 1.5em;
                }
                
                .info-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 15px;
                }
                
                .info-card {
                    background: #f5f5f5;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #667eea;
                }
                
                .info-card strong {
                    display: block;
                    color: #333;
                    margin-bottom: 5px;
                    font-size: 0.9em;
                }
                
                .info-card span {
                    font-size: 1.3em;
                    color: #667eea;
                    font-weight: bold;
                }
                
                .info-card.unit {
                    font-size: 0.85em;
                    color: #666;
                    margin-top: -5px;
                    border-left-color: transparent;
                    background: transparent;
                    padding-left: 0;
                }
                
                .json-viewer {
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                    line-height: 1.4;
                    max-height: 500px;
                    overflow-y: auto;
                }
                
                .json-viewer pre {
                    margin: 0;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }
                
                th, td {
                    text-align: left;
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }
                
                th {
                    background: #667eea;
                    color: white;
                }
                
                tr:hover {
                    background: #f9f9f9;
                }
                
                .back-link {
                    color: #667eea;
                    text-decoration: none;
                    display: inline-block;
                    margin-bottom: 20px;
                }
                
                .back-link:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="header-content">
                        <a href="/" class="back-link">← 返回主頁</a>
                        <h1>📋 測試結果詳情</h1>
                        <div class="header-info">
                            <div class="header-info-item">
                                <strong>測試名稱</strong>
                                <code>""" + test_name + """</code>
                            </div>
                            <div class="header-info-item">
                                <strong>測試 ID</strong>
                                <code>""" + test_id + """</code>
                            </div>
                            <div class="header-info-item">
                                <strong>掃描時間</strong>
                                <code>""" + timestamp + """</code>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="content">
                    <div class="button-group">
                        <button onclick="window.location.href='/'">🏠 返回列表</button>
                        <button onclick="downloadResult()">⬇️ 下載結果</button>
                        <button class="secondary" onclick="toggleJsonView()">👁️ 查看完整 JSON</button>
                    </div>
                    
                    <div id="summary-section">
                        <!-- 系統信息 -->
                        <div class="section">
                            <h2>🖥️ 系統信息</h2>
                            <div class="info-grid">
        """

        # 增加系統信息卡片
        system = scan_data.get("system", {})
        for key, value in system.items():
            display_key = key.replace("_", " ").title()
            html_template += f"""
                                <div class="info-card">
                                    <strong>{display_key}</strong>
                                    <span>{str(value)[:50]}</span>
                                </div>
            """

        html_template += f"""
                            </div>
                        </div>
                        
                        <!-- CPU 信息 -->
                        <div class="section">
                            <h2>⚙️ CPU 信息</h2>
                            <div class="info-grid">
        """

        cpu = scan_data.get("cpu", {})
        if "error" not in cpu:
            html_template += f"""
                                <div class="info-card">
                                    <strong>物理核心數</strong>
                                    <span>{cpu.get('physical_cores', 'N/A')}</span>
                                </div>
                                <div class="info-card">
                                    <strong>邏輯核心數</strong>
                                    <span>{cpu.get('logical_cores', 'N/A')}</span>
                                </div>
                                <div class="info-card">
                                    <strong>CPU 頻率</strong>
                                    <span>{cpu.get('cpu_freq_mhz', 'N/A')}</span>
                                    <div class="info-card unit">MHz</div>
                                </div>
                                <div class="info-card">
                                    <strong>當前使用率</strong>
                                    <span>{cpu.get('cpu_percent', 'N/A')}%</span>
                                </div>
            """
        else:
            html_template += f"<p>❌ 錯誤: {cpu.get('error')}</p>"

        html_template += f"""
                            </div>
                        </div>
                        
                        <!-- 內存信息 -->
                        <div class="section">
                            <h2>💾 內存信息</h2>
                            <div class="info-grid">
        """

        memory = scan_data.get("memory", {})
        if "error" not in memory:
            html_template += f"""
                                <div class="info-card">
                                    <strong>總內存</strong>
                                    <span>{memory.get('total_gb', 'N/A')}</span>
                                    <div class="info-card unit">GB</div>
                                </div>
                                <div class="info-card">
                                    <strong>已用內存</strong>
                                    <span>{memory.get('used_gb', 'N/A')}</span>
                                    <div class="info-card unit">GB</div>
                                </div>
                                <div class="info-card">
                                    <strong>可用內存</strong>
                                    <span>{memory.get('available_gb', 'N/A')}</span>
                                    <div class="info-card unit">GB</div>
                                </div>
                                <div class="info-card">
                                    <strong>使用百分比</strong>
                                    <span>{memory.get('percent', 'N/A')}%</span>
                                </div>
            """
        else:
            html_template += f"<p>❌ 錯誤: {memory.get('error')}</p>"

        html_template += """
                            </div>
                        </div>
                        
                        <!-- 存儲信息 -->
                        <div class="section">
                            <h2>💿 存儲信息</h2>
        """

        disk = scan_data.get("disk", {})
        if disk and "error" not in disk:
            html_template += """
                            <table>
                                <tr>
                                    <th>設備</th>
                                    <th>掛載點</th>
                                    <th>文件系統</th>
                                    <th>總大小</th>
                                    <th>已用</th>
                                    <th>空閒</th>
                                    <th>使用率</th>
                                </tr>
            """
            for device, info in disk.items():
                html_template += f"""
                                <tr>
                                    <td><code>{device}</code></td>
                                    <td>{info.get('mountpoint', 'N/A')}</td>
                                    <td>{info.get('fstype', 'N/A')}</td>
                                    <td>{info.get('total_gb', 'N/A')} GB</td>
                                    <td>{info.get('used_gb', 'N/A')} GB</td>
                                    <td>{info.get('free_gb', 'N/A')} GB</td>
                                    <td>{info.get('percent', 'N/A')}%</td>
                                </tr>
                """
            html_template += """
                            </table>
            """
        else:
            html_template += "<p>❌ 無可用的存儲信息</p>"

        html_template += f"""
                        </div>
                        
                        <!-- 網絡信息 -->
                        <div class="section">
                            <h2>🌐 網絡接口</h2>
        """

        network = scan_data.get("network", {})
        if network and "error" not in network:
            html_template += """
                            <table>
                                <tr>
                                    <th>接口名稱</th>
                                    <th>地址族</th>
                                    <th>IP 地址</th>
                                    <th>子網掩碼</th>
                                </tr>
            """
            for interface, addrs in network.items():
                for addr in addrs:
                    html_template += f"""
                                <tr>
                                    <td><code>{interface}</code></td>
                                    <td>{addr.get('family', 'N/A')}</td>
                                    <td>{addr.get('address', 'N/A')}</td>
                                    <td>{addr.get('netmask', 'N/A')}</td>
                                </tr>
                    """
            html_template += """
                            </table>
            """
        else:
            html_template += "<p>❌ 無可用的網絡信息</p>"

        html_template += f"""
                        </div>
                        
                        <!-- 系統運行時間 -->
                        <div class="section">
                            <h2>📅 系統運行時間</h2>
                            <div class="info-grid">
        """

        uptime = scan_data.get("uptime", {})
        if "error" not in uptime:
            html_template += f"""
                                <div class="info-card">
                                    <strong>運行時長</strong>
                                    <span>{uptime.get('uptime_days', 0)} 天 {uptime.get('uptime_hours', 0)} 小時 {uptime.get('uptime_minutes', 0)} 分鐘</span>
                                </div>
                                <div class="info-card">
                                    <strong>總秒數</strong>
                                    <span>{uptime.get('uptime_seconds', 'N/A')}</span>
                                </div>
            """

        html_template += """
                            </div>
                        </div>
                    </div>
                    
                    <!-- 完整 JSON 視圖 -->
                    <div class="section" id="json-section" style="display: none;">
                        <h2>📝 完整 JSON 數據</h2>
                        <div class="json-viewer">
                            <pre id="json-content"></pre>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                const testId = '""" + test_id[:8] + """';
                const testName = '""" + test_name + """';
                const fullTestId = '""" + test_id + """';
                
                function downloadResult() {
                    const url = `/api/download/${fullTestId}`;
                    const a = document.createElement('a');
                    a.href = url;
                    a.click();
                }
                
                function toggleJsonView() {
                    const summary = document.getElementById('summary-section');
                    const json = document.getElementById('json-section');
                    const jsonContent = document.getElementById('json-content');
                    
                    if (json.style.display === 'none') {
                        // 載入完整 JSON
                        fetch(`/api/scan/${fullTestId}`)
                            .then(response => response.json())
                            .then(data => {
                                jsonContent.textContent = JSON.stringify(data, null, 2);
                                summary.style.display = 'none';
                                json.style.display = 'block';
                            })
                            .catch(error => {
                                jsonContent.textContent = '❌ 無法載入 JSON: ' + error.message;
                                json.style.display = 'block';
                            });
                    } else {
                        summary.style.display = 'block';
                        json.style.display = 'none';
                    }
                }
            </script>
        </body>
        </html>
        """
        return html_template

    def _render_home_page(self) -> str:
        """
        渲染 Web UI 主頁

        Returns:
            HTML 字符串
        """
        html_template = """
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>設備掃描遠端測試工具</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Microsoft YaHei', '微軟正黑體', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    overflow: hidden;
                }
                
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                }
                
                .header h1 {
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }
                
                .header p {
                    font-size: 1.1em;
                    opacity: 0.9;
                }
                
                .content {
                    padding: 40px;
                }
                
                .section {
                    margin-bottom: 40px;
                }
                
                .section h2 {
                    color: #333;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }
                
                .button-group {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }
                
                button {
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1em;
                    transition: all 0.3s;
                }
                
                button:hover {
                    background: #764ba2;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                
                .result-box {
                    background: #f5f5f5;
                    padding: 20px;
                    border-radius: 5px;
                    margin-top: 20px;
                    border-left: 4px solid #667eea;
                }
                
                .result-box h3 {
                    color: #333;
                    margin-bottom: 10px;
                }
                
                .result-box p {
                    color: #666;
                    margin: 5px 0;
                    font-family: 'Courier New', monospace;
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                
                th, td {
                    text-align: left;
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }
                
                th {
                    background: #667eea;
                    color: white;
                }
                
                tr:hover {
                    background: #f5f5f5;
                }
                
                .result-row {
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .result-row:hover {
                    background: #e8f0ff;
                    transform: scale(1.01);
                    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
                }
                
                .action-buttons {
                    display: flex;
                    gap: 5px;
                }
                
                .action-buttons a, .action-buttons button {
                    padding: 6px 12px;
                    font-size: 0.85em;
                    border-radius: 3px;
                    text-decoration: none;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                
                .view-btn {
                    background: #667eea;
                    color: white;
                }
                
                .view-btn:hover {
                    background: #764ba2;
                }
                
                .download-btn {
                    background: #28a745;
                    color: white;
                }
                
                .download-btn:hover {
                    background: #218838;
                }
                
                .delete-btn {
                    background: #dc3545;
                    color: white;
                }
                
                .delete-btn:hover {
                    background: #c82333;
                }
                
                .status-badge {
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 0.9em;
                }
                
                .status-success {
                    background: #d4edda;
                    color: #155724;
                }
                
                .status-error {
                    background: #f8d7da;
                    color: #721c24;
                }
                
                .loader {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 20px 0;
                    display: none;
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .loader.active {
                    display: block;
                }
                
                input[type="text"] {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    width: 300px;
                    max-width: 100%;
                    font-size: 1em;
                }
                
                .api-example {
                    background: #f9f9f9;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                    font-family: 'Courier New', monospace;
                    overflow-x: auto;
                }
                
                .command {
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                    overflow-x: auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🖥️ 設備掃描遠端測試工具</h1>
                    <p>Device Remote Scanner - Port """ + str(self.port) + """</p>
                </div>
                
                <div class="content">
                    <!-- 快速操作區域 -->
                    <div class="section">
                        <h2>⚡ 快速操作</h2>
                        <div class="button-group">
                            <button onclick="scanDevice()">🔍 開始掃描</button>
                            <button onclick="loadResults()">📊 查看結果</button>
                            <button onclick="getStatistics()">📈 統計信息</button>
                            <button onclick="checkHealth()">✅ 健康檢查</button>
                        </div>
                    </div>
                    
                    <!-- 掃描區域 -->
                    <div class="section">
                        <h2>🔍 執行掃描</h2>
                        <div>
                            <p style="margin-bottom: 10px;">測試名稱：</p>
                            <input type="text" id="testName" placeholder="輸入測試名稱（可選）" value="device_scan">
                            <button onclick="scanDevice()" style="margin-left: 10px;">執行掃描</button>
                        </div>
                        <div class="loader" id="scanLoader"></div>
                        <div class="result-box" id="scanResult" style="display: none;"></div>
                    </div>
                    
                    <!-- 結果列表區域 -->
                    <div class="section">
                        <h2>📋 最近的掃描結果</h2>
                        <button onclick="loadResults()">重新整理</button>
                        <div class="loader" id="resultsLoader"></div>
                        <div id="resultsList"></div>
                    </div>
                    
                    <!-- API 文檔區域 -->
                    <div class="section">
                        <h2>📚 API 文檔</h2>
                        <h3>可用的 API 端點：</h3>
                        <div class="api-example">
                            POST /api/scan<br>
                            GET /api/scan/&lt;test_id&gt;<br>
                            GET /api/results<br>
                            GET /api/results/summary/&lt;test_id&gt;<br>
                            DELETE /api/results/&lt;test_id&gt;<br>
                            GET /api/statistics<br>
                            GET /api/apis<br>
                            GET /api/health</br>
                        </div>
                        
                        <h3>使用示例：</h3>
                        <p>1. 開始掃描：</p>
                        <div class="command">curl -X POST http://localhost:""" + str(self.port) + """/api/scan</div>
                        
                        <p>2. 查看結果：</p>
                        <div class="command">curl http://localhost:""" + str(self.port) + """/api/scan/&lt;test_id&gt;</div>
                        
                        <p>3. 列出所有結果：</p>
                        <div class="command">curl http://localhost:""" + str(self.port) + """/api/results</div>
                    </div>
                </div>
            </div>
            
            <script>
                // 開始掃描
                function scanDevice() {
                    const testName = document.getElementById('testName').value || 'device_scan';
                    const loader = document.getElementById('scanLoader');
                    const result = document.getElementById('scanResult');
                    
                    loader.classList.add('active');
                    result.style.display = 'none';
                    
                    fetch('/api/scan', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ test_name: testName })
                    })
                    .then(response => response.json())
                    .then(data => {
                        loader.classList.remove('active');
                        result.style.display = 'block';
                        
                        if (data.status === 'success') {
                            result.innerHTML = `
                                <h3>✅ 掃描成功</h3>
                                <p><strong>測試 ID:</strong> ${data.test_id}</p>
                                <p><strong>檔案名稱:</strong> ${data.filename}</p>
                                <p><strong>訊息:</strong> ${data.message}</p>
                            `;
                            setTimeout(() => loadResults(), 1000);
                        } else {
                            result.classList.add('status-error');
                            result.innerHTML = `<h3>❌ 掃描失敗</h3><p>${data.message}</p>`;
                        }
                    })
                    .catch(error => {
                        loader.classList.remove('active');
                        result.style.display = 'block';
                        result.classList.add('status-error');
                        result.innerHTML = `<h3>❌ 錯誤</h3><p>${error.message}</p>`;
                    });
                }
                
                // 載入結果列表
                function loadResults() {
                    const loader = document.getElementById('resultsLoader');
                    const list = document.getElementById('resultsList');
                    
                    loader.style.display = 'block';
                    list.innerHTML = '';
                    
                    fetch('/api/results?limit=20')
                    .then(response => response.json())
                    .then(data => {
                        loader.style.display = 'none';
                        
                        if (data.status === 'success' && data.results.length > 0) {
                            let html = '<table>';
                            html += '<tr><th>測試名稱</th><th>測試 ID</th><th>掃描時間</th><th>操作</th></tr>';
                            
                            data.results.forEach(result => {
                                const testId = result.test_id;
                                const shortId = testId.substring(0, 8);
                                const timestamp = new Date(result.timestamp).toLocaleString('zh-TW');
                                
                                html += `<tr class="result-row">
                                    <td><strong>${result.test_name}</strong></td>
                                    <td><code title="${testId}">${shortId}...</code></td>
                                    <td>${timestamp}</td>
                                    <td>
                                        <div class="action-buttons">
                                            <a href="/results/${testId}" class="view-btn" onclick="event.stopPropagation()">👁️ 查看</a>
                                            <button class="download-btn" onclick="downloadResult('${testId}'); event.stopPropagation();">⬇️ 下載</button>
                                            <button class="delete-btn" onclick="deleteResult('${testId}'); event.stopPropagation();">🗑️ 刪除</button>
                                        </div>
                                    </td>
                                </tr>`;
                            });
                            
                            html += '</table>';
                            list.innerHTML = html;
                        } else {
                            list.innerHTML = '<p>沒有找到結果</p>';
                        }
                    })
                    .catch(error => {
                        loader.style.display = 'none';
                        list.innerHTML = `<p style="color: red;">錯誤: ${error.message}</p>`;
                    });
                }
                
                // 獲取統計信息
                function getStatistics() {
                    fetch('/api/statistics')
                    .then(response => response.json())
                    .then(data => {
                        alert(`總結果數: ${data.total_results}\\n總大小: ${data.total_size_mb} MB\\n目錄: ${data.results_directory}`);
                    })
                    .catch(error => alert('錯誤: ' + error.message));
                }
                
                // 健康檢查
                function checkHealth() {
                    fetch('/api/health')
                    .then(response => response.json())
                    .then(data => {
                        const timestamp = new Date(data.timestamp).toLocaleString('zh-TW');
                        alert(`狀態: ${data.status}\n時間: ${timestamp}\n端口: ${data.port}`);
                    })
                    .catch(error => alert('錯誤: ' + error.message));
                }
                
                // 下載結果
                function downloadResult(testId) {
                    const url = `/api/download/${testId}`;
                    const a = document.createElement('a');
                    a.href = url;
                    a.click();
                }
                
                // 刪除結果
                function deleteResult(testId) {
                    if (!confirm('確定要刪除這個測試結果嗎？')) {
                        return;
                    }
                    
                    fetch(`/api/results/${testId}`, {
                        method: 'DELETE'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('✅ 結果已刪除');
                            loadResults();
                        } else {
                            alert('❌ 刪除失敗: ' + data.message);
                        }
                    })
                    .catch(error => alert('❌ 錯誤: ' + error.message));
                }
                
                // 頁面加載時獲取結果
                window.addEventListener('load', () => {
                    loadResults();
                });
            </script>
        </body>
        </html>
        """
        return render_template_string(html_template)

    def run(self, debug: bool = False):
        """
        運行遠端服務器

        Args:
            debug: 是否以調試模式運行
        """
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║         遠端設備掃描測試服務                              ║
║         Remote Device Scanner Service                    ║
╚═══════════════════════════════════════════════════════════╝

📍 服務運行信息:
   URL: http://localhost:{self.port}
   API: http://localhost:{self.port}/api
   結果存儲目錄: {os.path.abspath(self.results_dir)}

🔌 API 端點:
   POST   /api/scan                    - 執行掃描
   GET    /api/scan/<test_id>          - 獲取掃描結果
   GET    /api/results                 - 列出所有結果
   GET    /api/results/summary/<id>    - 獲取結果摘要
   GET    /api/statistics              - 統計信息
   DELETE /api/results/<test_id>       - 刪除結果
   GET    /api/apis                    - 列出 API
   GET    /api/health                  - 健康檢查
   GET    /                             - Web UI 主頁

⌨️  快捷命令:
   # 開始掃描
   curl -X POST http://localhost:{self.port}/api/scan

   # 查看結果列表
   curl http://localhost:{self.port}/api/results

   # 獲取掃描摘要
   curl http://localhost:{self.port}/api/results/summary/<test_id>

⚙️  設置:
   調試模式: {debug}

按 Ctrl+C 停止服務...
""")
        self.app.run(host='0.0.0.0', port=self.port, debug=debug)


def create_remote_server(port: int = 3388, results_dir: str = "results") -> RemoteServer:
    """
    創建遠端服務器實例

    Args:
        port: 服務端口，默認 3388
        results_dir: 結果存儲目錄，默認 'results'

    Returns:
        RemoteServer 實例
    """
    return RemoteServer(port=port, results_dir=results_dir)
