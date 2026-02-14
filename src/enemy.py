"""
敵人坦克類別實現

敵人坦克是玩家需要消滅的對象，有不同類型（基礎型、快速型、重裝型）。
每種類型有不同的顏色、速度和生命值。
"""

import random
import time
from pathlib import Path
from typing import Literal, Optional, Tuple

import pygame

from src.bullet import Bullet


class EnemyTank(pygame.sprite.Sprite):
    """
    敵人坦克精靈類別

    表示遊戲中玩家需要消滅的敵人坦克，包含位置、方向、生命值、類型等屬性。
    敵人坦克有三種類型：基礎型、快速型和重裝型，各有不同的特性。

     屬性：
            rect: pygame.Rect - 坦克的矩形碰撞區域
            x: float - 水平位置（像素）
            y: float - 垂直位置（像素）
            direction: Literal["up", "down", "left", "right"] - 坦克朝向
            speed: float - 移動速度（像素/幀）
            lives: int - 剩餘生命數
            enemy_type: Literal["basic", "fast", "heavy"] - 敵人類型
            color: tuple - 坦克顏色 (RGB)
            move_interval: int - 改變方向的時間間隔（毫秒，範圍 1000-2000）
            last_direction_change: int - 最後一次改變方向的時間戳
            last_shot_time: float - 最後射擊的時間戳（秒）
            shoot_interval: float - 射擊冷卻時間間隔（秒）
    """

    TANK_SIZE = 40
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

    ENEMY_CONFIGS = {
        "basic": {
            "speed": 2,
            "lives": 1,
            "color": (255, 0, 0),
        },
        "fast": {
            "speed": 4,
            "lives": 1,
            "color": (0, 255, 0),
        },
        "heavy": {
            "speed": 2,
            "lives": 2,
            "color": (128, 128, 128),
        },
    }

    def __init__(
        self,
        x: int,
        y: int,
        enemy_type: Literal["basic", "fast", "heavy"] = "basic",
    ) -> None:
        """
        初始化敵人坦克

        參數：
                x: 初始水平位置（像素）
                y: 初始垂直位置（像素）
                enemy_type: 敵人類型（'basic', 'fast', 'heavy'），預設為 'basic'

        異常：
                ValueError: 如果 enemy_type 不是有效的類型
        """
        super().__init__()

        if enemy_type not in self.ENEMY_CONFIGS:
            raise ValueError(
                f"無效的敵人類型: {enemy_type}。有效類型: {list(self.ENEMY_CONFIGS.keys())}"
            )

        self.x = float(x)
        self.y = float(y)

        self.enemy_type = enemy_type
        config = self.ENEMY_CONFIGS[enemy_type]
        self.speed = config["speed"]
        self.lives = config["lives"]
        self.color = config["color"]

        self.direction: Literal["up", "down", "left", "right"] = "down"

        self.move_interval = random.randint(1000, 2000)
        self.last_direction_change = pygame.time.get_ticks()

        # 射擊相關屬性（根據敵人類型設定射擊間隔）
        self.last_shot_time = 0.0
        self.shoot_interval = (
            random.uniform(1.5, 2.5)
            if enemy_type == "basic"
            else (
                random.uniform(1.0, 1.8)
                if enemy_type == "fast"
                else random.uniform(2.0, 3.0)
            )
        )

        # 載入坦克圖像
        self.image = self._load_tank_image()
        if self.image is None:
            # 如果圖片載入失敗，回退到程序生成
            self.image = pygame.Surface(
                (self.TANK_SIZE, self.TANK_SIZE), pygame.SRCALPHA
            )
            self._draw_tank_image()

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def _load_tank_image(self) -> Optional[pygame.Surface]:
        """
        載入敵人坦克圖像

        根據當前方向載入對應的 PNG 圖像。
        如果載入失敗，返回 None 並觸發回退到程序生成。

        返回：
            pygame.Surface - 載入的圖像（成功時），None（失敗時）
        """
        try:
            # 建立圖像檔案名稱（使用小寫）
            direction_file = {
                "up": "tank_enemy_up.png",
                "down": "tank_enemy_down.png",
                "left": "tank_enemy_left.png",
                "right": "tank_enemy_right.png",
            }[self.direction]

            # 載入圖像
            image_path = self.ASSETS_DIR / direction_file
            loaded_image = pygame.image.load(str(image_path))

            # 調整圖像大小以符合坦克尺寸（保持寬高比）
            return pygame.transform.scale(
                loaded_image, (self.TANK_SIZE, self.TANK_SIZE)
            )
        except (FileNotFoundError, pygame.error):
            # 載入失敗，返回 None
            return None

    def _draw_tank_image(self) -> None:
        """
        程序生成敵人坦克圖像

        清空當前圖像並繪製新坦克圖像。圖像為簡單的正方形，顏色取決於敵人類型。
        """
        self.image.fill((0, 0, 0, 0))

        pygame.draw.rect(
            self.image,
            self.color,
            (
                0,
                0,
                self.TANK_SIZE,
                self.TANK_SIZE,
            ),
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        繪製敵人坦克到指定的表面

        參數：
                surface: pygame.Surface - 目標繪製表面（通常是遊戲螢幕）
        """
        surface.blit(self.image, self.rect)

    def get_cannon_position(self) -> Tuple[float, float]:
        """
        計算砲管位置（子彈生成點）

        根據坦克朝向計算砲管位置，距離坦克中心約 30 像素。

        返回：
            Tuple[float, float] - (x, y) 砲管位置座標
        """
        cannon_offset = 30
        direction_offsets = {
            "up": (0, -cannon_offset),
            "down": (0, cannon_offset),
            "left": (-cannon_offset, 0),
            "right": (cannon_offset, 0),
        }
        offset_x, offset_y = direction_offsets[self.direction]
        return (self.x + offset_x, self.y + offset_y)

    def try_shoot(self) -> Optional[Bullet]:
        """
        嘗試發射子彈

        檢查是否足夠時間已經過去，若滿足冷卻時間則創建並返回子彈。
        否則返回 None。

        返回：
            Optional[Bullet] - 如果發射成功則返回 Bullet 實例，否則返回 None
        """
        # 獲取當前時間（秒）
        current_time = time.time()

        # 檢查冷卻時間是否已經過
        if current_time - self.last_shot_time < self.shoot_interval:
            return None

        # 更新射擊時間戳
        self.last_shot_time = current_time

        # 將方向字符串轉換為方向向量
        direction_vectors = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        direction_vector = direction_vectors[self.direction]

        # 獲取砲管位置
        cannon_x, cannon_y = self.get_cannon_position()

        # 創建子彈
        bullet = Bullet(cannon_x, cannon_y, direction_vector, owner="enemy")

        return bullet

    def can_move(self, new_rect: pygame.Rect, obstacles: list[pygame.Rect]) -> bool:
        """
        檢查是否可以移動到新位置

        檢查邊界碰撞和障礙物碰撞。

        參數：
                new_rect: pygame.Rect - 新位置的矩形
                obstacles: list[pygame.Rect] - 障礙物列表

        回傳：
                bool - True 可以移動，False 發生碰撞
        """
        if (
            new_rect.left < 0
            or new_rect.right > self.WINDOW_WIDTH
            or new_rect.top < 0
            or new_rect.bottom > self.WINDOW_HEIGHT
        ):
            return False

        for obstacle in obstacles:
            if new_rect.colliderect(obstacle):
                return False

        return True

    def update(self, obstacles: list[pygame.Rect]) -> None:
        """
        更新敵人坦克的位置和方向

        根據計時器定期改變方向，嘗試按當前方向移動。
        如果碰撞則嘗試找到一個可移動的方向。

        參數：
                obstacles: list[pygame.Rect] - 障礙物列表
        """
        current_time = pygame.time.get_ticks()

        # 定期改變方向
        if current_time - self.last_direction_change >= self.move_interval:
            self._choose_random_direction()
            self.last_direction_change = current_time

        # 嘗試移動
        new_x, new_y = self.x, self.y
        if self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed
        elif self.direction == "left":
            new_x -= self.speed
        elif self.direction == "right":
            new_x += self.speed

        new_rect = self.image.get_rect(center=(int(new_x), int(new_y)))

        if self.can_move(new_rect, obstacles):
            # 可以移動，更新位置
            self.x = new_x
            self.y = new_y
            self.rect.center = (int(self.x), int(self.y))
        else:
            # 碰撞，嘗試找到一個可移動的方向
            if not self._try_find_valid_direction(obstacles):
                # 如果沒有可移動的方向，隨機選擇一個方向（避免死鎖）
                self._choose_random_direction()
            self.last_direction_change = current_time

    def _choose_random_direction(self) -> None:
        """隨機選擇一個方向並更新坦克圖像"""
        self.direction = random.choice(["up", "down", "left", "right"])
        loaded = self._load_tank_image()
        if loaded is not None:
            self.image = loaded
        else:
            self._draw_tank_image()

    def _try_find_valid_direction(self, obstacles: list[pygame.Rect]) -> bool:
        """
        嘗試找到一個可以移動的方向

        遍歷所有方向，找到第一個可以移動的方向。
        如果找不到任何可移動的方向，返回 False。

        參數：
                obstacles: list[pygame.Rect] - 障礙物列表

        返回：
                bool - True 找到可移動的方向，False 沒有找到
        """
        # 保存原始方向
        original_direction = self.direction

        # 遍歷所有方向
        for direction in ["up", "down", "left", "right"]:
            self.direction = direction

            # 計算新位置
            new_x, new_y = self.x, self.y
            if direction == "up":
                new_y -= self.speed
            elif direction == "down":
                new_y += self.speed
            elif direction == "left":
                new_x -= self.speed
            elif direction == "right":
                new_x += self.speed

            new_rect = self.image.get_rect(center=(int(new_x), int(new_y)))

            # 檢查是否可以移動
            if self.can_move(new_rect, obstacles):
                # 找到可移動的方向，更新圖像並返回 True
                loaded = self._load_tank_image()
                if loaded is not None:
                    self.image = loaded
                else:
                    self._draw_tank_image()
                return True

        # 如果找不到可移動的方向，恢復原始方向
        self.direction = original_direction
        return False
