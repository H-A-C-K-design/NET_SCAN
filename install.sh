#!/bin/bash
# Network Scanner Pro Installation Script
# Author: Security Researcher
# Date: 2024

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         Network Scanner Pro - Installation Script            ║"
echo "║                    Author: Security Researcher               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "[-] This script must be run as root (use sudo)" 
   exit 1
fi

echo "[*] Installing Network Scanner Pro..."

# Install Python dependencies
echo "[*] Installing Python dependencies..."
apt-get update
apt-get install -y python3 python3-pip nmap masscan

# Install Python packages
pip3 install ipaddress argparse

# Create directory structure
echo "[*] Creating directory structure..."
mkdir -p /usr/share/netscan-pro
mkdir -p /usr/share/netscan-pro/results
mkdir -p /usr/share/netscan-pro/logs

# Copy main script
echo "[*] Installing main scanner script..."
cp netscan-pro.py /usr/share/netscan-pro/
chmod +x /usr/share/netscan-pro/netscan-pro.py

# Create symlink
echo "[*] Creating symlink..."
ln -sf /usr/share/netscan-pro/netscan-pro.py /usr/local/bin/netscan-pro

# Create configuration file
echo "[*] Creating configuration file..."
cat > /usr/share/netscan-pro/config.json << EOF
{
    "author": "Security Researcher",
    "version": "1.0",
    "default_scan_range": "1-1024",
    "thread_count": 50,
    "timeout": 1,
    "results_dir": "/usr/share/netscan-pro/results",
    "logs_dir": "/usr/share/netscan-pro/logs"
}
EOF

# Create README file
echo "[*] Creating documentation..."
cat > /usr/share/netscan-pro/README.md << EOF
# Network Scanner Pro

**Author:** Security Researcher  
**Version:** 1.0  
**License:** MIT  

## Description
Advanced network scanning tool for Kali Linux with multiple scanning capabilities.

## Features
- Ping sweep for host discovery
- Port scanning with threading
- OS detection
- Service version detection
- Multiple scan types (quick, full, ping)
- JSON output support

## Installation
Run the install.sh script as root:
\`\`\`
sudo ./install.sh
\`\`\`

## Usage Examples

1. Scan a single host:
\`\`\`
netscan-pro -t 192.168.1.1
\`\`\`

2. Quick scan with output file:
\`\`\`
netscan-pro -t 192.168.1.1 -o results.json
\`\`\`

3. Scan network range:
\`\`\`
netscan-pro -n 192.168.1.0/24
\`\`\`

4. Full port scan:
\`\`\`
netscan-pro -t 192.168.1.1 -s full -p 1-65535
\`\`\`

5. Ping sweep only:
\`\`\`
netscan-pro -t 192.168.1.1 -s ping
\`\`\`

## Legal Disclaimer
This tool is for educational and authorized testing purposes only.
Unauthorized scanning of networks may be illegal.
EOF

# Set permissions
echo "[*] Setting permissions..."
chmod -R 755 /usr/share/netscan-pro
chown -R root:root /usr/share/netscan-pro

echo ""
echo "[+] Installation complete!"
echo "[+] You can now run 'netscan-pro' from anywhere"
echo "[+] Documentation available at /usr/share/netscan-pro/README.md"
echo ""
echo "Usage examples:"
echo "  netscan-pro -t 192.168.1.1"
echo "  netscan-pro -n 192.168.1.0/24"
echo "  netscan-pro -t 192.168.1.1 -o scan_results.json"
