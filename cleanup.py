#!/usr/bin/env python3
"""
Cyber Runner Cleanup Tool
Removes all traces of the educational backdoor
For educational purposes only - Rwanda Coding Academy Assignment
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import json

class CyberRunnerCleaner:
    def __init__(self):
        self.system = platform.system()
        self.home_dir = Path.home()
        self.config_dir = self.home_dir / ".cyber_runner"
        self.config_file = self.config_dir / "config.json"
        
    def log_cleanup(self, message):
        """Log cleanup activities"""
        print(f"[CLEANUP] {message}")
        
    def remove_linux_persistence(self):
        """Remove Linux persistence (crontab)"""
        try:
            # Get current crontab
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Remove lines containing cyber_runner
                new_lines = [line for line in lines if 'cyber_runner' not in line and line.strip()]
                
                # Update crontab
                if new_lines:
                    new_cron = '\n'.join(new_lines) + '\n'
                else:
                    new_cron = ""
                    
                process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
                process.communicate(input=new_cron.encode())
                
                self.log_cleanup("Removed crontab persistence")
            else:
                self.log_cleanup("No crontab entries found")
                
        except Exception as e:
            self.log_cleanup(f"Failed to remove Linux persistence: {str(e)}")
            
    def remove_windows_persistence(self):
        """Remove Windows persistence (registry)"""
        try:
            import winreg
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            
            try:
                winreg.DeleteValue(key, "CyberRunner")
                self.log_cleanup("Removed registry persistence")
            except FileNotFoundError:
                self.log_cleanup("No registry entry found")
                
            winreg.CloseKey(key)
            
        except Exception as e:
            self.log_cleanup(f"Failed to remove Windows persistence: {str(e)}")
            
    def remove_macos_persistence(self):
        """Remove macOS persistence (launch agent)"""
        try:
            launch_agent_dir = self.home_dir / "Library" / "LaunchAgents"
            plist_file = launch_agent_dir / "com.cyberrunner.agent.plist"
            
            if plist_file.exists():
                plist_file.unlink()
                self.log_cleanup("Removed launch agent")
                
                # Unload the agent
                subprocess.run(['launchctl', 'unload', str(plist_file)], 
                             capture_output=True)
                
            else:
                self.log_cleanup("No launch agent found")
                
        except Exception as e:
            self.log_cleanup(f"Failed to remove macOS persistence: {str(e)}")
            
    def remove_config_files(self):
        """Remove configuration and log files"""
        try:
            if self.config_dir.exists():
                shutil.rmtree(self.config_dir)
                self.log_cleanup("Removed configuration directory")
            else:
                self.log_cleanup("No configuration directory found")
                
        except Exception as e:
            self.log_cleanup(f"Failed to remove config files: {str(e)}")
            
    def stop_processes(self):
        """Stop any running Cyber Runner processes"""
        try:
            if self.system == "Linux":
                # Find and kill python processes running our scripts
                result = subprocess.run(['pgrep', '-f', 'cyber_runner'], 
                                      capture_output=True, text=True)
                
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        subprocess.run(['kill', pid])
                        self.log_cleanup(f"Killed process {pid}")
                else:
                    self.log_cleanup("No running processes found")
                    
        except Exception as e:
            self.log_cleanup(f"Failed to stop processes: {str(e)}")
            
    def scan_for_artifacts(self):
        """Scan for any remaining artifacts"""
        artifacts = []
        
        # Check common locations
        common_paths = [
            self.home_dir / ".cyber_runner",
            self.home_dir / "cyber_runner",
            Path("/tmp/cyber_runner"),
            Path("/var/tmp/cyber_runner")
        ]
        
        for path in common_paths:
            if path.exists():
                artifacts.append(str(path))
                
        # Check for processes
        try:
            if self.system == "Linux":
                result = subprocess.run(['pgrep', '-f', 'cyber_runner'], 
                                      capture_output=True, text=True)
                if result.stdout.strip():
                    artifacts.append("Running processes detected")
        except:
            pass
            
        return artifacts
        
    def run_cleanup(self):
        """Run complete cleanup process"""
        print("=== Cyber Runner Cleanup Tool ===")
        print("Educational Backdoor Removal Utility")
        print()
        
        self.log_cleanup("Starting cleanup process...")
        
        # Stop processes
        self.stop_processes()
        
        # Remove persistence based on OS
        if self.system == "Linux":
            self.remove_linux_persistence()
        elif self.system == "Windows":
            self.remove_windows_persistence()
        elif self.system == "Darwin":
            self.remove_macos_persistence()
            
        # Remove config files
        self.remove_config_files()
        
        # Final scan
        print("\n=== Final Scan ===")
        artifacts = self.scan_for_artifacts()
        
        if artifacts:
            print("Remaining artifacts found:")
            for artifact in artifacts:
                print(f"  - {artifact}")
        else:
            print("✓ No artifacts found - cleanup complete!")
            
        print("\n=== Cleanup Complete ===")
        print("All traces of Cyber Runner have been removed")

def main():
    cleaner = CyberRunnerCleaner()
    
    # Safety confirmation
    print("This tool will remove all traces of Cyber Runner.")
    response = input("Do you want to continue? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        cleaner.run_cleanup()
    else:
        print("Cleanup cancelled.")

if __name__ == "__main__":
    main()
