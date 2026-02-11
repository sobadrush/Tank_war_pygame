"""
遊戲管理器模組
管理遊戲狀態、碰撞檢測、計分系統
"""

import pygame
import random
from typing import List, Optional

from src.tank import PlayerTank
from src.enemy import EnemyTank
from src.bullet import Bullet
from src.map import Map


class Game:
    """遊戲管理器類別"""

    def __init__(self):
        """初始化遊戲"""
        # 創建地圖
        self.map = Map()

        # 創建玩家坦克（底部中央）
        self.player = PlayerTank(400, 550)

        # 創建精靈組
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # 添加玩家到精靈組
        self.all_sprites.add(self.player)

        # 初始化遊戲狀態
        self.score = 0
        self.game_over = False
        self.game_won = False

        # 生成初始敵人（3-5個）
        self._spawn_initial_enemies()

    def _spawn_initial_enemies(self):
        """生成初始敵人"""
        enemy_count = random.randint(3, 5)
        for _ in range(enemy_count):
            self.spawn_enemy()

    def spawn_enemy(self):
        """生成一個敵人"""
        # 隨機敵人類型
        enemy_types = ["basic", "fast", "heavy"]
        weights = [0.5, 0.3, 0.2]  # basic 更多，heavy 更少
        enemy_type = random.choices(enemy_types, weights=weights)[0]

        # 隨機位置（頂部區域）
        x = random.randint(50, 750)
        y = random.randint(50, 150)

        # 確保不離玩家太近
        while abs(x - 400) < 100 and abs(y - 550) < 200:
            x = random.randint(50, 750)
            y = random.randint(50, 150)

        enemy = EnemyTank(x, y, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def update(self, keys):
        """更新遊戲狀態"""
        # 更新玩家
        self.player.handle_input(keys)
        self.player.move(self.map.obstacles)
        self.player.update()

        # 更新敵人
        for enemy in self.enemies:
            enemy.update(self.map.obstacles)
            # 敵人嘗試射擊
            bullet = enemy.try_shoot()
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

        # 更新子彈
        self.bullets.update()

        # 檢查碰撞
        self._check_collisions()

        # 檢查遊戲結束條件
        self._check_game_over()

    def _check_collisions(self):
        """檢查所有碰撞"""
        # 玩家子彈擊中敵人
        for bullet in self.bullets:
            if bullet.owner == "player":
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
                if hit_enemies:
                    bullet.kill()
                    for enemy in hit_enemies:
                        enemy.lives -= 1
                        if enemy.lives <= 0:
                            enemy.kill()
                            self.score += 100

        # 敵人子彈擊中玩家
        for bullet in self.bullets:
            if bullet.owner == "enemy":
                if bullet.rect.colliderect(self.player.rect):
                    if not self.player.invincible:
                        bullet.kill()
                        self.player.hit()

        # 玩家與敵人坦克碰撞
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hit_enemies and not self.player.invincible:
            for enemy in hit_enemies:
                enemy.kill()
                self.player.hit()
                self.score += 50

        # 子彈擊中地圖障礙物
        for bullet in self.bullets:
            hit_obstacles = pygame.sprite.spritecollide(
                bullet, self.map.obstacles, False
            )
            if hit_obstacles:
                bullet.kill()
                for obstacle in hit_obstacles:
                    if obstacle in self.map.bricks:
                        self.map.destroy_brick(obstacle)

    def _check_game_over(self):
        """檢查遊戲結束條件"""
        if self.player.lives <= 0:
            self.game_over = True
        elif len(self.enemies) == 0:
            self.game_won = True

    def player_shoot(self):
        """玩家射擊"""
        bullet = self.player.shoot()
        if bullet:
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)

    def draw(self, screen):
        """繪製所有遊戲元素"""
        # 繪製地圖
        self.map.draw(screen)

        # 繪製所有精靈
        for sprite in self.all_sprites:
            sprite.draw(screen)

        # 繪製分數和生命值
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
