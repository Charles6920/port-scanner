#!/usr/bin/env python3
import socket

class PortScanner:
    def __init__(self, target_host):
        # Resolve target hostname (like 'google.com') to an IP address
        self.target_host = target_host
        try:
            self.target_ip = socket.gethostbyname(target_host)
        except socket.gaierror:
            print(f"\n[!] Error: Could not resolve hostname {target_host}")
            self.target_ip = None

    def scan_port(self, port):
        """Attempts to connect to a specific port and grab its banner."""
        if not self.target_ip:
            return
        
        # Create a TCP socket
        # AF_INET = IPv4, SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout so the script doesn't freeze forever on closed ports
        s.settimeout(1.0)
        
        try:
            # Connect to target IP and port
            result = s.connect_ex((self.target_ip, port))
            
            # connect_ex returns 0 if the connection was successful
            if result == 0:
                print(f"[+] Port {port} is OPEN!")
                
                # Attempt banner grabbing
                try:
                    # Send a basic probe nudge
                    s.send(b'Hello\r\n')
                    # Read up to 1024 bytes of the response
                    banner = s.recv(1024).decode().strip()
                    if banner:
                        print(f"    --> Banner: {banner}")
                except Exception:
                    # Some services stay silent unless sent a specific protocol payload
                    print("    --> Banner: Clear connection established (No explicit banner visible)")
                    
        except Exception as e:
            pass
        finally:
            # Always close the socket connection
            s.close()

# Terminal Execution Setup
if __name__ == "__main__":
    print("\n=== RECONNAISSANCE PORT SCANNER ===\n")
    target = input("Enter target URL or IP address (e.g., scanme.nmap.org): ")
    
    scanner = PortScanner(target)
    
    if scanner.target_ip:
        print(f"\n[*] Scanning target: {scanner.target_host} ({scanner.target_ip})")
        print("[*] Testing ports 21, 22, 80, 443...\n")
        
        # Test a small list of classic target ports
        for test_port in [21, 22, 80, 443]:
            scanner.scan_port(test_port)
            
        print("\n[*] Scan complete.")