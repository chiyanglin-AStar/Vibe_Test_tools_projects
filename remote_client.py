#!/usr/bin/env python3
"""
遠端客戶端測試腳本

此腳本用於連接到遠端測試服務並執行各種操作

使用方式：
    python3 remote_client.py --help              # 查看幫助
    python3 remote_client.py --scan              # 執行掃描
    python3 remote_client.py --list              # 列出結果
    python3 remote_client.py --get <test_id>     # 獲取結果
    python3 remote_client.py --summary <test_id> # 查看摘要

API 端點配置：
    默認: http://localhost:3388
    可通過 --host 和 --port 指定
"""

import sys
import argparse
import json
from device_scanner.remote_client import create_remote_client


def print_banner():
    """打印應用橫幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║       遠端設備掃描客戶端                                 ║
║       Device Scanner Remote Client                       ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_json(data: dict, indent: int = 2):
    """打印 JSON 格式的數據"""
    print(json.dumps(data, indent=indent, default=str, ensure_ascii=False))


def main():
    """主函數"""
    print_banner()

    parser = argparse.ArgumentParser(
        description="遠端設備掃描客戶端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 檢查服務器健康狀態
  python3 remote_client.py --health

  # 執行掃描
  python3 remote_client.py --scan

  # 自定義測試名稱的掃描
  python3 remote_client.py --scan --name my_test

  # 只掃描 CPU 信息
  python3 remote_client.py --scan --type cpu

  # 列出最近 10 個結果
  python3 remote_client.py --list --limit 10

  # 查看特定結果的摘要
  python3 remote_client.py --summary <test_id>

  # 查看完整結果
  python3 remote_client.py --get <test_id>

  # 保存結果到本地
  python3 remote_client.py --save <test_id> --output result.json

  # 列出可用的 API
  python3 remote_client.py --apis

  # 獲取統計信息
  python3 remote_client.py --statistics

  # 連接到遠端服務器
  python3 remote_client.py --host 192.168.1.100 --port 3388 --health
        """
    )

    # 連接選項
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="遠端服務器主機（默認: localhost）",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3388,
        help="遠端服務器端口（默認: 3388）",
    )

    # 功能選項
    parser.add_argument(
        "--health",
        action="store_true",
        help="檢查服務器健康狀態",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="執行遠端掃描",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="device_scan",
        help="掃描的測試名稱（默認: device_scan）",
    )
    parser.add_argument(
        "--type",
        type=str,
        default="full",
        help="掃描類型 (full/cpu/memory/disk/network/gpu)（默認: full）",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出遠端測試結果",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="結果列表的限制數量",
    )
    parser.add_argument(
        "--get",
        type=str,
        metavar="TEST_ID",
        help="獲取特定測試結果",
    )
    parser.add_argument(
        "--summary",
        type=str,
        metavar="TEST_ID",
        help="獲取測試結果摘要",
    )
    parser.add_argument(
        "--save",
        type=str,
        metavar="TEST_ID",
        help="保存結果到本地文件",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="result.json",
        help="輸出文件路徑（默認: result.json）",
    )
    parser.add_argument(
        "--delete",
        type=str,
        metavar="TEST_ID",
        help="刪除特定測試結果",
    )
    parser.add_argument(
        "--apis",
        action="store_true",
        help="列出服務器上可用的 API",
    )
    parser.add_argument(
        "--statistics",
        action="store_true",
        help="獲取服務器統計信息",
    )

    args = parser.parse_args()

    # 創建客戶端
    client = create_remote_client(host=args.host, port=args.port)

    # 檢查健康狀態
    if args.health:
        print("🏥 檢查服務器健康狀態...\n")
        result = client.check_health()
        print_json(result)
        return 0

    # 執行掃描
    if args.scan:
        print(f"🔍 正在執行遠端掃描...\n")
        result = client.scan_device(test_name=args.name, scan_type=args.type)
        print_json(result)

        if result.get("status") == "success":
            test_id = result.get("test_id")
            print(f"\n✅ 掃描成功！測試 ID: {test_id}")
        return 0

    # 列出結果
    if args.list:
        print("📋 獲取結果列表...\n")
        result = client.list_results(limit=args.limit)
        if result.get("status") == "success":
            print(f"共 {result.get('count')} 個結果：\n")
            for item in result.get("results", []):
                print(f"  ID: {item['test_id'][:8]}...")
                print(f"  名稱: {item['test_name']}")
                print(f"  時間: {item['timestamp']}")
                print()
        else:
            print(f"❌ 錯誤: {result.get('message')}")
        return 0

    # 獲取特定結果
    if args.get:
        print(f"📥 獲取結果: {args.get}\n")
        result = client.get_scan_result(args.get)
        if result.get("status") == "error":
            print(f"❌ 錯誤: {result.get('message')}")
        else:
            print_json(result)
        return 0

    # 獲取結果摘要
    if args.summary:
        print(f"📄 獲取結果摘要: {args.summary}\n")
        client.print_result_summary(args.summary)
        return 0

    # 保存結果
    if args.save:
        print(f"💾 保存結果到: {args.output}\n")
        if client.save_result_locally(args.save, args.output):
            print(f"✅ 結果已保存")
        else:
            print(f"❌ 保存失敗")
        return 0

    # 刪除結果
    if args.delete:
        print(f"🗑️  刪除結果: {args.delete}\n")
        result = client.delete_result(args.delete)
        print_json(result)
        return 0

    # 列出 API
    if args.apis:
        print("📚 遠端服務器可用的 API:\n")
        result = client.list_available_apis()
        if result.get("status") == "success":
            apis = result.get("apis", {})
            for api_name, details in sorted(apis.items()):
                print(f"  • {api_name}()")
                print(f"    描述: {details.get('description')}")
                print(f"    返回: {details.get('returns')}")
                print()
        return 0

    # 獲取統計信息
    if args.statistics:
        print("📈 服務器統計信息:\n")
        result = client.get_statistics()
        print_json(result)
        return 0

    # 如果沒有指定任何選項，顯示幫助
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
