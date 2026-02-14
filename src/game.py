"""
遊戲管理器模組
管理遊戲狀態、碰撞檢測、計分系統
"""

import pygame
import random
from pathlib import Path
from typing import List, Optional, Literal

from src.tank import PlayerTank
from src.enemy import EnemyTank
from src.bullet import Bullet
from src.map import Map


class Game:
    """遊戲管理器類別"""

    # 資源目錄
    ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
    MUSIC_DIR = ASSETS_DIR / "music"

    def __init__(self):
        """初始化遊戲"""
        # 載入音效
        self.game_start_sound = self._load_sound("game_start.wav")
        self.shoot_sound = self._load_sound("shoot.mp3")
        self.game_win_sound = self._load_sound("game_win.mp3")
        self.game_over_sound = self._load_sound("game_over.mp3")

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

        # 播放遊戲開始音效
        if self.game_start_sound:
            self.game_start_sound.play()

    def _spawn_initial_enemies(self):
        """生成初始敵人"""
        enemy_count = random.randint(3, 5)
        for _ in range(enemy_count):
            self.spawn_enemy()

    def _is_spawn_position_clear(self, rect: pygame.Rect) -> bool:
        """
        檢查出生位置是否可以放置敵人

        參數：
            rect: pygame.Rect - 敵人坦克的矩形區域

        返回：
            bool - True 表示可放置，False 表示與物件重疊
        """
        if self.player.rect is None:
            return False
        if rect.colliderect(self.player.rect):
            return False

        for obstacle in self.map.obstacles:
            if obstacle.rect is None:
                continue
            if rect.colliderect(obstacle.rect):
                return False

        for enemy in self.enemies:
            if enemy.rect is None:
                continue
            if rect.colliderect(enemy.rect):
                return False

        return True

    def _collect_spawn_positions(self, grid_y_range: range) -> list[tuple[int, int]]:
        """
        收集可用的敵人出生位置

        參數：
            grid_y_range: range - y 方向的格子範圍

        返回：
            list[tuple[int, int]] - 可用的 (x, y) 位置列表
        """
        positions: list[tuple[int, int]] = []
        grid_size = self.map.GRID_SIZE
        for grid_y in grid_y_range:
            if grid_y < 0 or grid_y >= self.map.MAP_HEIGHT:
                continue
            for grid_x in range(self.map.MAP_WIDTH):
                x = grid_x * grid_size + grid_size // 2
                y = grid_y * grid_size + grid_size // 2
                rect = pygame.Rect(0, 0, EnemyTank.TANK_SIZE, EnemyTank.TANK_SIZE)
                rect.center = (x, y)
                if self._is_spawn_position_clear(rect):
                    positions.append((x, y))
        return positions

    def spawn_enemy(self):
        """生成一個敵人"""
        # 隨機敵人類型
        enemy_types: list[Literal["basic", "fast", "heavy"]] = [
            "basic",
            "fast",
            "heavy",
        ]
        weights = [0.5, 0.3, 0.2]  # basic 更多，heavy 更少
        enemy_type = random.choices(enemy_types, weights=weights, k=1)[0]

        # 優先在頂部區域尋找可用位置
        top_positions = self._collect_spawn_positions(range(1, 4))
        if top_positions:
            x, y = random.choice(top_positions)
        else:
            # 如果頂部區域沒有位置，改用整張地圖
            all_positions = self._collect_spawn_positions(range(self.map.MAP_HEIGHT))
            if not all_positions:
                return
            x, y = random.choice(all_positions)

        enemy = EnemyTank(x, y, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def update(self, keys):
        """更新遊戲狀態"""
        obstacle_rects = self.map.get_obstacles_rects()

        # 更新玩家
        self.player.handle_input(keys)
        self.player.move(obstacle_rects)
        self.player.update()

        # 更新敵人
        for enemy in self.enemies:
            enemy.update(obstacle_rects)
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
            # 播放遊戲失敗音效
            if self.game_over_sound:
                self.game_over_sound.play()
        elif len(self.enemies) == 0:
            self.game_won = True
            # 播放遊戲勝利音效
            if self.game_win_sound:
                self.game_win_sound.play()

    def player_shoot(self):
        """玩家射擊"""
        bullet = self.player.shoot()
        if bullet:
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            # 播放射擊音效
            if self.shoot_sound:
                self.shoot_sound.play()

    def _load_sound(self, filename: str) -> Optional[pygame.mixer.Sound]:
        """
        載入音效檔案

        參數：
            filename: 音效檔案名稱

        返回：
            pygame.mixer.Sound - 載入的音效（成功時），None（失敗時）
        """
        try:
            sound_path = self.MUSIC_DIR / filename
            sound = pygame.mixer.Sound(str(sound_path))
            return sound
        except (FileNotFoundError, pygame.error):
            return None

    def reset(self):
        """
        重置遊戲狀態

        重置所有遊戲元素，包括：
        - 分數歸零
        - 重新生成地圖（障礙物和草叢位置隨機）
        - 重置玩家位置和生命值
        - 清除並重新生成敵人（位置和類型隨機）
        - 清除所有子彈
        """
        # 重置遊戲狀態
        self.score = 0
        self.game_over = False
        self.game_won = False

        # 清除所有精靈
        self.enemies.empty()
        self.bullets.empty()
        self.all_sprites.empty()

        # 重新生成地圖（新的障礙物和草叢位置）
        self.map = Map()

        # 重置玩家坦克（位置和生命值）
        self.player = PlayerTank(400, 550)
        self.all_sprites.add(self.player)

        # 生成新的敵人（位置和類型隨機）
        self._spawn_initial_enemies()

        # 播放遊戲開始音效
        if self.game_start_sound:
            self.game_start_sound.play()

    def _load_heart_image(self) -> Optional[pygame.Surface]:
        """
        載入愛心圖像

        返回：
            pygame.Surface - 載入的圖像（成功時），None（失敗時）
        """
        try:
            image_path = self.ASSETS_DIR / "life-heart.png"
            image = pygame.image.load(str(image_path))
            return image
        except (FileNotFoundError, pygame.error):
            return None

    def draw(self, screen):
        """繪製所有遊戲元素"""
        # 繪製地圖障礙物（磚塊和鋼塊）
        self.map.draw(screen)

        # 繪製所有精靈（坦克、子彈等）
        for sprite in self.all_sprites:
            sprite.draw(screen)

        # 繪製草叢（在最上層，遮擋坦克）
        self.map.bushes.draw(screen)

        # 繪製分數
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # 繪製生命值（使用愛心圖示）
        heart_image = self._load_heart_image()
        if heart_image:
            # 縮小愛心圖示
            heart_size = 30
            heart_image = pygame.transform.scale(heart_image, (heart_size, heart_size))
            # 根據生命值數量繪製愛心
            for i in range(self.player.lives):
                screen.blit(heart_image, (10 + i * 35, 50))
        else:
            # 回退到文字顯示
            lives_text = font.render(
                f"Lives: {self.player.lives}", True, (255, 255, 255)
            )
            screen.blit(lives_text, (10, 50))
