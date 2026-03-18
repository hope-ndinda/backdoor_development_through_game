# Cyber Runner - Educational Backdoor Game

**Rwanda Coding Academy - Cybersecurity Course Assignment**

## Overview

Cyber Runner is an educational Temple Run-style endless runner game that demonstrates cybersecurity concepts through practical implementation. This project is designed **exclusively for educational purposes** to help students understand:

- Backdoor mechanisms and persistence techniques
- System security vulnerabilities
- Network programming and shell access
- Malware analysis and removal

**⚠️ IMPORTANT:** This tool should only be used in controlled virtual machine environments for educational training.

## Game Features

### Gameplay
- **Temple Run-style endless runner** with increasing difficulty
- **Jump mechanics** (SPACE key) to avoid high obstacles
- **Slide mechanics** (DOWN arrow) to duck under low obstacles
- Progressive speed increase for challenge
- Score tracking system

### Educational Components
1. **Dependency Management** - Automatically checks and installs required applications
2. **Persistence Mechanisms** - Survives system restarts across different OS platforms
3. **Shell Access** - Provides remote shell access for educational demonstrations
4. **Interruption Prevention** - Maintains operation during gameplay
5. **Comprehensive Logging** - Tracks all activities for analysis

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Virtual Machine (strongly recommended)
- Administrative privileges (for persistence features)

### Installation Steps

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd cyber-runner
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## Usage Instructions

### Starting the Game
1. Run `python main.py`
2. Read the educational disclaimer carefully
3. Press SPACE to continue or ESC to exit

### Game Controls
- **SPACE**: Jump over high obstacles (red)
- **DOWN ARROW**: Slide under low obstacles (yellow)
- **R**: Restart when game over
- **ESC**: Exit game

### Shell Access
The backdoor automatically starts a shell listener on `127.0.0.1:4444`. Connect using:
```bash
nc 127.0.0.1 4444
```

Available shell commands:
- `help` - Show available commands
- `info` - Display system information
- `status` - Show backdoor status
- `exit` - Disconnect from shell

## Technical Implementation

### File Structure
```
cyber-runner/
├── main.py              # Main game application
├── backdoor_utils.py    # Backdoor functionality
├── cleanup.py          # Removal utility
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

### Core Components

#### 1. Game Engine (`main.py`)
- Pygame-based 2D endless runner
- Player physics and collision detection
- Obstacle generation and management
- Score and difficulty progression

#### 2. Backdoor Manager (`backdoor_utils.py`)
- **Dependency Checker**: Verifies required system applications
- **Persistence Manager**: OS-specific startup mechanisms
- **Shell Listener**: Remote access implementation
- **Activity Logger**: Comprehensive activity tracking

#### 3. Cleanup Utility (`cleanup.py`)
- Removes all persistence mechanisms
- Deletes configuration files
- Terminates running processes
- Scans for remaining artifacts

### Persistence Mechanisms by OS

#### Linux
- Uses user crontab with `@reboot` directive
- Survives system restarts
- Executes silently in background

#### Windows
- Registry entry in `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Auto-starts with user login
- Runs as background process

#### macOS
- Launch Agent in `~/Library/LaunchAgents/`
- Standard macOS persistence technique
- Loads automatically at login

## Educational Learning Objectives

After completing this assignment, students will understand:

1. **Malware Persistence**
   - How malware maintains presence across reboots
   - OS-specific persistence mechanisms
   - Registry and startup folder manipulation

2. **Remote Access Techniques**
   - Socket programming for backdoor communication
   - Command execution and response handling
   - Network security principles

3. **System Security**
   - Privilege escalation concepts
   - Process hiding and interruption prevention
   - File system manipulation

4. **Defense and Removal**
   - Malware detection techniques
   - Complete artifact removal
   - System security hardening

## Security Considerations

### For Educational Use Only
- **Never deploy on production systems**
- **Always use in isolated VM environments**
- **Ensure proper network isolation**
- **Document all activities for learning**

### Detection Methods
This tool demonstrates common detection signatures:
- Unusual network connections (port 4444)
- Modified startup configurations
- Unexpected background processes
- Configuration files in user directories

## Troubleshooting

### Common Issues

1. **Game won't start**
   - Check Python version (3.7+ required)
   - Install missing dependencies: `pip install -r requirements.txt`
   - Verify Pygame installation

2. **Shell access not working**
   - Check if port 4444 is available
   - Verify firewall settings
   - Ensure backdoor initialization completed

3. **Persistence not working**
   - Check system permissions
   - Verify administrative privileges
   - Check OS-specific requirements

### Debug Mode
Run with verbose logging:
```bash
python backdoor_utils.py --help
```

## Cleanup Procedure

### Automated Cleanup
Use the provided cleanup utility:
```bash
python cleanup.py
```

### Manual Cleanup Steps
1. Stop all running processes
2. Remove startup entries (crontab/registry/launch agents)
3. Delete configuration directory: `~/.cyber_runner`
4. Remove project files


## Ethical Usage Statement

This project is developed exclusively for cybersecurity education at Rwanda Coding Academy. The techniques demonstrated are for learning purposes only and should never be used for malicious activities. Students are expected to:

- Use only in controlled environments
- Document all testing activities
- Follow ethical hacking guidelines
- Contribute positively to cybersecurity knowledge

