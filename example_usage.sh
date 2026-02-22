#!/bin/bash
# Network Scanner Pro - Usage Examples
# Author: Security Researcher

echo "Network Scanner Pro - Usage Examples"
echo "======================================"
echo ""

# Example 1: Basic scan
echo "Example 1: Basic scan of localhost"
echo "Command: netscan-pro -t 127.0.0.1"
echo ""
netscan-pro -t 127.0.0.1
echo ""

# Example 2: Scan with output file
echo "Example 2: Scan with output file"
echo "Command: netscan-pro -t 127.0.0.1 -o scan_results.json"
echo ""
netscan-pro -t 127.0.0.1 -o scan_results.json
echo ""

# Example 3: Show help
echo "Example 3: Show help menu"
echo "Command: netscan-pro -h"
echo ""
netscan-pro -h

echo ""
echo "For more examples, check the README file:"
echo "cat /usr/share/netscan-pro/README.md"
