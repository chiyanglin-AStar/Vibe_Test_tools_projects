#!/usr/bin/env python3
"""
遠端服務器啟動腳本

此腳本啟動遠端設備掃描測試服務

使用方式：
    python3 remote_server.py                 # 運行在默認端口 3388
    python3 remote_server.py --port 3389     # 指定端口
    python3 remote_server.py --debug         # 調試模式

結果存儲位置：
    ./results/ 目錄中的 JSON 文件

Web UI 訪問：
    http://localhost:3388
"""

import sys
import argparse
from device_scanner.remote_server import create_remote_server


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="遠端設備掃描測試服務",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 使用默認配置啟動（端口 3388）
  python3 remote_server.py

  # 指定端口
  python3 remote_server.py --port 3389

  # 調試模式運行
  python3 remote_server.py --debug

  # 指定結果目錄
  python3 remote_server.py --results-dir /path/to/results

服務啟動後，訪問 http://localhost:3388 查看 Web UI
        """
    )

    parser.add_argument(
        "--port",
        type=int,
        default=3388,
        help="服務運行的端口（默認: 3388）",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results",
        help="測試結果存儲目錄（默認: results）",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="以調試模式運行",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="服務綁定的主機地址（默認: 0.0.0.0）",
    )

    args = parser.parse_args()

    try:
        # 創建並運行服務器
        server = create_remote_server(
            port=args.port,
            results_dir=args.results_dir,
        )
        server.run(debug=args.debug)
    except KeyboardInterrupt:
        print("\n\n⏹️  服務已停止")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
