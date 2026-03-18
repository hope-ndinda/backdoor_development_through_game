#!/usr/bin/env python3
"""
Cyber Runner Build Script
Creates standalone executables for different platforms
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class CyberRunnerBuilder:
    def __init__(self):
        self.system = platform.system()
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        
    def log(self, message):
        print(f"[BUILDER] {message}")
        
    def clean_build(self):
        """Clean previous build artifacts"""
        self.log("Cleaning previous builds...")
        
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            
        # Remove .spec files
        for spec_file in self.project_dir.glob("*.spec"):
            spec_file.unlink()
            
        self.log("Build cleanup complete")
        
    def install_pyinstaller(self):
        """Install PyInstaller if not available"""
        try:
            import PyInstaller
            self.log("PyInstaller already installed")
        except ImportError:
            self.log("Installing PyInstaller...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            
    def build_game(self):
        """Build the main game executable"""
        self.log("Building Cyber Runner game...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",  # No console window for the game
            "--name", "CyberRunner",
            "--add-data", "README.md:.",
            "main.py"
        ]
        
        if self.system == "Windows":
            # Windows-specific options
            cmd[2] = "--windowed"  # Keep windowed for Windows
            cmd[3:3] = ["--icon", "icon.ico"] if Path("icon.ico").exists() else []
            
        subprocess.run(cmd, check=True)
        self.log("Game build complete")
        
    def build_cleaner(self):
        """Build the cleanup utility"""
        self.log("Building Cyber Runner Cleaner...")
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--console",  # Show console for cleaner
            "--name", "CyberRunnerCleaner",
            "cleanup.py"
        ]
        
        subprocess.run(cmd, check=True)
        self.log("Cleaner build complete")
        
    def create_release_package(self):
        """Create a release package with executables and documentation"""
        self.log("Creating release package...")
        
        release_dir = self.project_dir / "release"
        if release_dir.exists():
            shutil.rmtree(release_dir)
        release_dir.mkdir()
        
        # Copy executables
        for exe_file in self.dist_dir.glob("*"):
            shutil.copy2(exe_file, release_dir)
            
        # Copy documentation
        shutil.copy2(self.project_dir / "README.md", release_dir)
        
        # Create usage instructions
        instructions = f"""# Cyber Runner - Executable Package

## Files Included:
- CyberRunner{'.exe' if self.system == 'Windows' else ''} - Main game executable
- CyberRunnerCleaner{'.exe' if self.system == 'Windows' else ''} - Cleanup utility
- README.md - Complete documentation

## Quick Start:
1. Run CyberRunner{'.exe' if self.system == 'Windows' else ''}
2. Follow the on-screen instructions
3. Use CyberRunnerCleaner when done

## System Requirements:
- {self.system} operating system
- No additional dependencies required

## For Educational Use Only!
Run only in controlled virtual machine environments.

Built on: {platform.system()} {platform.release()}
"""
        
        with open(release_dir / "USAGE.txt", "w") as f:
            f.write(instructions)
            
        self.log(f"Release package created in: {release_dir}")
        
    def build_all(self):
        """Build all executables"""
        self.log(f"Starting build for {self.system}...")
        
        try:
            self.clean_build()
            self.install_pyinstaller()
            self.build_game()
            self.build_cleaner()
            self.create_release_package()
            
            self.log("Build completed successfully!")
            self.log(f"Executables available in: {self.dist_dir}")
            self.log(f"Release package in: {self.project_dir / 'release'}")
            
        except subprocess.CalledProcessError as e:
            self.log(f"Build failed: {e}")
            sys.exit(1)
        except Exception as e:
            self.log(f"Unexpected error: {e}")
            sys.exit(1)

def main():
    builder = CyberRunnerBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "clean":
            builder.clean_build()
        elif command == "game":
            builder.build_game()
        elif command == "cleaner":
            builder.build_cleaner()
        elif command == "package":
            builder.create_release_package()
        else:
            print("Usage: python build.py [clean|game|cleaner|package]")
            sys.exit(1)
    else:
        builder.build_all()

if __name__ == "__main__":
    main()
