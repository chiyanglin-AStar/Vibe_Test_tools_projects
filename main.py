#!/usr/bin/env python3
"""
Device Scanner Test Tool - Main Entry Point

This tool scans system devices and generates comprehensive device information
and API documentation in markdown format.
"""

import sys
import json
import argparse
from pathlib import Path
from device_scanner import DeviceScanner
from device_scanner.markdown_generator import MarkdownGenerator


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║           Device Scanner Test Tool v1.0.0               ║
║     Comprehensive System Device Information Scanner     ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Device Scanner - Comprehensive system device information tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --scan-all                    # Full device scan
  python main.py --info cpu                    # CPU information only
  python main.py --markdown device_info.md     # Generate markdown report
  python main.py --json device_info.json       # Export as JSON
  python main.py --list-apis                   # List available APIs
        """
    )
    
    parser.add_argument(
        "--scan-all",
        action="store_true",
        help="Perform complete device scan and display results"
    )
    parser.add_argument(
        "--info",
        choices=["system", "cpu", "memory", "gpu", "disk", "network", "process", "uptime"],
        help="Get specific device information type"
    )
    parser.add_argument(
        "--markdown",
        type=str,
        metavar="FILE",
        help="Generate markdown report and save to FILE"
    )
    parser.add_argument(
        "--json",
        type=str,
        metavar="FILE",
        help="Export device information as JSON to FILE"
    )
    parser.add_argument(
        "--list-apis",
        action="store_true",
        help="List all available API methods"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Pretty print JSON output (default: True)"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Create scanner instance
    scanner = DeviceScanner()
    
    # Handle different commands
    if args.list_apis:
        print("📚 Available APIs:\n")
        apis = scanner.list_available_apis()
        for api_name, details in sorted(apis.items()):
            print(f"  • {api_name}()")
            print(f"    └─ {details['description']}")
        print()
        return 0
    
    if args.info:
        print(f"🔍 Scanning {args.info.upper()} information...\n")
        info = scanner.get_specific_info(args.info)
        if args.pretty:
            print(json.dumps(info, indent=2, default=str))
        else:
            print(info)
        print()
        return 0
    
    if args.scan_all or (not args.markdown and not args.json and not args.list_apis and not args.info):
        print("🔍 Performing complete device scan...\n")
        device_info = scanner.scan()
        if args.pretty:
            print(json.dumps(device_info, indent=2, default=str))
        else:
            print(device_info)
        print()
    else:
        # Ensure we have scanned
        scanner.scan()
    
    # Generate markdown if requested
    if args.markdown:
        print(f"📝 Generating markdown report: {args.markdown}")
        device_info = scanner.get_device_dict()
        apis = scanner.list_available_apis()
        generator = MarkdownGenerator(device_info, apis)
        
        if generator.save_to_file(args.markdown):
            print(f"✅ Markdown report saved to: {args.markdown}")
        else:
            print(f"❌ Failed to save markdown report")
            return 1
        print()
    
    # Export JSON if requested
    if args.json:
        print(f"📊 Exporting device information: {args.json}")
        json_data = scanner.get_device_json(indent=2)
        
        try:
            with open(args.json, 'w', encoding='utf-8') as f:
                f.write(json_data)
            print(f"✅ JSON data exported to: {args.json}")
        except Exception as e:
            print(f"❌ Failed to export JSON: {e}")
            return 1
        print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
