#!/usr/bin/env python3
"""
Network Scanner Pro - Advanced Network Scanning Tool
Author: Security Researcher
Version: 1.0
License: MIT
"""

import socket
import sys
import subprocess
import argparse
from datetime import datetime
import ipaddress
import threading
from queue import Queue
import time
import json

class NetworkScanner:
    def __init__(self):
        self.author = "Security Researcher"
        self.version = "1.0"
        self.open_ports = []
        self.lock = threading.Lock()
        
    def print_banner(self):
        """Display tool banner with author information"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                   Network Scanner Pro                     ║
║                         Author: DURGESH GAIKWAD                      ║
║                  Advanced Network Scanning Tool                    ║
║                    For Kali Linux & Security Testing               ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def ping_sweep(self, network):
        """Perform ping sweep to discover live hosts"""
        print(f"\n[*] Starting ping sweep on {network}")
        live_hosts = []
        
        try:
            network = ipaddress.ip_network(network, strict=False)
            
            for ip in network.hosts():
                ip_str = str(ip)
                response = subprocess.run(
                    ['ping', '-c', '1', '-W', '1', ip_str],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                if response.returncode == 0:
                    live_hosts.append(ip_str)
                    print(f"[+] Host {ip_str} is alive")
                    
        except Exception as e:
            print(f"[-] Error in ping sweep: {e}")
            
        return live_hosts
    
    def port_scan(self, target, port):
        """Scan a single port on target"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                    
                with self.lock:
                    self.open_ports.append(port)
                    print(f"[+] Port {port}/tcp open - {service}")
                    
            sock.close()
            
        except:
            pass
    
    def scan_ports(self, target, start_port=1, end_port=1024):
        """Scan multiple ports on target using threading"""
        print(f"\n[*] Scanning ports on {target} (ports {start_port}-{end_port})")
        self.open_ports = []
        
        queue = Queue()
        
        for port in range(start_port, end_port + 1):
            queue.put(port)
            
        def worker():
            while not queue.empty():
                port = queue.get()
                self.port_scan(target, port)
                queue.task_done()
        
        # Create thread pool
        threads = []
        for _ in range(50):  # 50 concurrent threads
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)
            
        queue.join()
        
        for t in threads:
            t.join()
            
        return self.open_ports
    
    def os_detection(self, target):
        """Basic OS detection using TTL"""
        try:
            response = subprocess.run(
                ['ping', '-c', '1', target],
                capture_output=True,
                text=True
            )
            
            if "ttl=" in response.stdout.lower():
                ttl_line = response.stdout.lower().split("ttl=")[1].split()[0]
                ttl = int(ttl_line)
                
                if ttl <= 64:
                    os_type = "Linux/Unix"
                elif ttl <= 128:
                    os_type = "Windows"
                else:
                    os_type = "Unknown/Cisco"
                    
                print(f"[*] Detected OS: {os_type} (TTL: {ttl})")
                return os_type
                
        except:
            pass
            
        return "Unknown"
    
    def service_version(self, target, port):
        """Simple service version detection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((target, port))
            
            # Send probe for common services
            if port == 80:  # HTTP
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            elif port == 21:  # FTP
                sock.send(b"HELP\r\n")
            elif port == 22:  # SSH
                pass  # SSH banner is usually immediate
                
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner[:100] if banner else "No banner"
            
        except:
            return "Unknown"
    
    def comprehensive_scan(self, target):
        """Perform comprehensive scan on target"""
        print(f"\n{'='*60}")
        print(f"Starting comprehensive scan on {target}")
        print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # OS Detection
        os_type = self.os_detection(target)
        
        # Port scanning
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 
                       445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        print(f"\n[*] Scanning common ports...")
        open_ports = []
        
        for port in common_ports:
            if self.port_scan_simple(target, port):
                open_ports.append(port)
                service = socket.getservbyport(port, 'tcp') if port <= 1024 else "unknown"
                version = self.service_version(target, port)
                print(f"[+] Port {port}/tcp - {service} - Version: {version}")
        
        return {
            'target': target,
            'os': os_type,
            'open_ports': open_ports,
            'timestamp': str(datetime.now())
        }
    
    def port_scan_simple(self, target, port):
        """Simple port scan (returns True if open)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def save_results(self, results, filename):
        """Save scan results to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=4)
            print(f"\n[+] Results saved to {filename}")
        except Exception as e:
            print(f"[-] Error saving results: {e}")

def main():
    scanner = NetworkScanner()
    scanner.print_banner()
    
    parser = argparse.ArgumentParser(description='Network Scanner Pro - Advanced Network Scanning Tool')
    parser.add_argument('-t', '--target', help='Target IP address or hostname')
    parser.add_argument('-n', '--network', help='Network range (e.g., 192.168.1.0/24)')
    parser.add_argument('-p', '--ports', help='Port range (e.g., 1-1000)', default='1-1024')
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('-s', '--scan-type', choices=['quick', 'full', 'ping'], 
                       default='quick', help='Scan type')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    # Parse port range
    try:
        if args.ports:
            start_port, end_port = map(int, args.ports.split('-'))
    except:
        print("[-] Invalid port range. Using default 1-1024")
        start_port, end_port = 1, 1024
    
    results = {}
    
    if args.network:
        # Network discovery mode
        print(f"\n[*] Scanning network: {args.network}")
        live_hosts = scanner.ping_sweep(args.network)
        
        if live_hosts:
            results['live_hosts'] = live_hosts
            
            for host in live_hosts:
                host_results = scanner.comprehensive_scan(host)
                results[host] = host_results
        else:
            print("[-] No live hosts found")
            
    elif args.target:
        # Single target mode
        if args.scan_type == 'ping':
            # Just ping sweep
            host_alive = subprocess.run(
                ['ping', '-c', '2', args.target],
                capture_output=True
            ).returncode == 0
            
            if host_alive:
                print(f"[+] Host {args.target} is alive")
                results['target'] = args.target
                results['status'] = 'alive'
            else:
                print(f"[-] Host {args.target} is not responding")
                results['status'] = 'dead'
                
        elif args.scan_type == 'quick':
            # Quick port scan
            results = scanner.comprehensive_scan(args.target)
            
        elif args.scan_type == 'full':
            # Full port scan
            print(f"\n[*] Full port scan on {args.target}")
            open_ports = scanner.scan_ports(args.target, start_port, end_port)
            results['target'] = args.target
            results['open_ports'] = open_ports
            results['os'] = scanner.os_detection(args.target)
    
    # Save results if output file specified
    if args.output and results:
        scanner.save_results(results, args.output)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)
