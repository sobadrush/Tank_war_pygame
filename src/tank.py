"""
玩家坦克類別實現

玩家坦克是玩家控制的主要遊戲角色，具有移動、射擊、生命值管理等功能。
坦克會檢查地圖邊界和障礙物碰撞，受傷後有短暫無敵時間。
"""

from typing import List, Literal, Optional, Tuple

import pygame

from src.bullet import Bullet


class PlayerTank(pygame.sprite.Sprite):
    """
    玩家坦克精靈類別

    表示遊戲中玩家控制的坦克，包含位置、速度、方向、生命值、無敵狀態等屬性。
    坦克可以移動、射擊、受傷和重生。

    屬性：
        rect: pygame.Rect - 坦克的矩形碰撞區域
        x: float - 水平位置（像素）
        y: float - 垂直位置（像素）
        direction: Literal["up", "down", "left", "right"] - 坦克朝向
        speed: float - 移動速度（像素/幀）
        lives: int - 剩餘生命數
        invincible: bool - 是否處於無敵狀態
        invincible_time: int - 無敵時間計時器（毫秒）
        last_shoot_time: int - 上次射擊時間
    """

    # 坦克常數設定
    TANK_SIZE = 40  # 坦克大小（像素）
    TANK_COLOR = (255, 255, 0)  # 黃色 (RGB) - 車身
    TURRET_COLOR = (204, 204, 0)  # 深黃色 (RGB) - 砲管
    TANK_SPEED = 4  # 移動速度（像素/幀）
    STARTING_LIVES = 3  # 初始生命數
    SHOOT_COOLDOWN = 400  # 射擊冷卻時間（毫秒）
    INVINCIBILITY_TIME = 2000  # 無敵時間（毫秒）
    CANNON_LENGTH = 20  # 砲管長度（像素）
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    STARTING_X = 400  # 初始 X 座標（視窗寬度中心）
    STARTING_Y = 550  # 初始 Y 座標（靠近底部）

    def __init__(self, x: int = STARTING_X, y: int = STARTING_Y) -> None:
        """
        初始化玩家坦克

        參數：
            x: 初始水平位置（像素），預設為視窗中心
            y: 初始垂直位置（像素），預設為靠近底部
        """
        super().__init__()

        # 位置屬性
        self.x = float(x)
        self.y = float(y)

        # 方向和速度
        self.direction: Literal["up", "down", "left", "right"] = "up"
        self.speed = self.TANK_SPEED

        # 生命和狀態
        self.lives = self.STARTING_LIVES
        self.invincible = False
        self.invincible_time = 0  # 無敵時間計時器

        # 射擊冷卻
        self.last_shoot_time = 0

        # 建立坦克圖像（程序生成）
        self.image = pygame.Surface((self.TANK_SIZE, self.TANK_SIZE), pygame.SRCALPHA)
        self._draw_tank_image()

        # 建立碰撞矩形
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def _draw_tank_image(self) -> None:
        """
        程序生成坦克圖像（黃色車身 + 砲管）

        清空當前圖像並繪製新坦克圖像。
        """
        # 清空圖像
        self.image.fill((0, 0, 0, 0))

        # 繪製坦克車身（正方形）
        pygame.draw.rect(
            self.image,
            self.TANK_COLOR,
            (
                0,
                0,
                self.TANK_SIZE,
                self.TANK_SIZE,
            ),
        )

        # 根據方向繪製砲管
        center_x = self.TANK_SIZE // 2
        center_y = self.TANK_SIZE // 2

        if self.direction == "up":
            # 向上的砲管
            start_pos = (center_x, center_y - self.TANK_SIZE // 4)
            end_pos = (center_x, center_y - self.TANK_SIZE // 4 - self.CANNON_LENGTH)
        elif self.direction == "down":
            # 向下的砲管
            start_pos = (center_x, center_y + self.TANK_SIZE // 4)
            end_pos = (center_x, center_y + self.TANK_SIZE // 4 + self.CANNON_LENGTH)
        elif self.direction == "left":
            # 向左的砲管
            start_pos = (center_x - self.TANK_SIZE // 4, center_y)
            end_pos = (
                center_x - self.TANK_SIZE // 4 - self.CANNON_LENGTH,
                center_y,
            )
        else:  # right
            # 向右的砲管
            start_pos = (center_x + self.TANK_SIZE // 4, center_y)
            end_pos = (
                center_x + self.TANK_SIZE // 4 + self.CANNON_LENGTH,
                center_y,
            )

        # 繪製砲管（深黃色線條）
        pygame.draw.line(
            self.image,
            self.TURRET_COLOR,
            start_pos,
            end_pos,
            width=4,
        )

    def move(self, obstacles: Optional[List[pygame.Rect]] = None) -> None:
        """
        移動坦克到指定方向

        根據當前方向移動坦克，並檢查邊界和障礙物碰撞。
        如果無法移動，坦克位置不變。

        參數：
            obstacles: 障礙物矩形列表，若為 None 則不檢查碰撞
        """
        # 計算新位置
        new_x = self.x
        new_y = self.y

        if self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed
        elif self.direction == "left":
            new_x -= self.speed
        elif self.direction == "right":
            new_x += self.speed

        # 檢查邊界
        if (
            new_x - self.TANK_SIZE // 2 < 0
            or new_x + self.TANK_SIZE // 2 > self.WINDOW_WIDTH
            or new_y - self.TANK_SIZE // 2 < 0
            or new_y + self.TANK_SIZE // 2 > self.WINDOW_HEIGHT
        ):
            # 超出邊界，不移動
            return

        # 檢查障礙物碰撞
        if obstacles:
            # 創建新位置的碰撞矩形
            new_rect = self.image.get_rect(center=(int(new_x), int(new_y)))

            # 檢查與任何障礙物的碰撞
            for obstacle_rect in obstacles:
                if new_rect.colliderect(obstacle_rect):
                    # 碰撞到障礙物，不移動
                    return

        # 更新位置
        self.x = new_x
        self.y = new_y
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def shoot(self) -> Optional[Bullet]:
        """
        射擊子彈

        檢查射擊冷卻，如果可以射擊則創建子彈。
        子彈從坦克砲管位置發射。

        返回：
            Bullet 實例（如果發射成功），否則返回 None
        """
        # 檢查射擊冷卻
        current_time = pygame.time.get_ticks()
        if (
            self.last_shoot_time > 0
            and current_time - self.last_shoot_time < self.SHOOT_COOLDOWN
        ):
            # 冷卻時間未到
            return None

        # 更新上次射擊時間
        self.last_shoot_time = current_time

        # 計算子彈發射位置（砲管頂端）
        bullet_x = self.x
        bullet_y = self.y

        # 根據方向調整發射位置
        offset = self.TANK_SIZE // 2 + 5
        if self.direction == "up":
            bullet_y -= offset
            direction_vector: Tuple[int, int] = (0, -1)
        elif self.direction == "down":
            bullet_y += offset
            direction_vector = (0, 1)
        elif self.direction == "left":
            bullet_x -= offset
            direction_vector = (-1, 0)
        else:  # right
            bullet_x += offset
            direction_vector = (1, 0)

        # 創建子彈
        bullet = Bullet(
            x=bullet_x,
            y=bullet_y,
            direction=direction_vector,
            owner="player",
            damage=1,
        )

        return bullet

    def hit(self) -> None:
        """
        坦克受傷

        減少生命值並進入短暫無敵狀態。
        """
        # 減少生命值
        self.lives -= 1

        # 進入無敵狀態
        self.invincible = True
        self.invincible_time = self.INVINCIBILITY_TIME

    def respawn(self, x: int = STARTING_X, y: int = STARTING_Y) -> None:
        """
        坦克重生

        重置坦克位置、方向並進入短暫無敵狀態。

        參數：
            x: 重生位置 X 座標，預設為初始位置
            y: 重生位置 Y 座標，預設為初始位置
        """
        # 重置位置
        self.x = float(x)
        self.y = float(y)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # 重置方向
        self.direction = "up"

        # 進入無敵狀態
        self.invincible = True
        self.invincible_time = self.INVINCIBILITY_TIME

    def update(self) -> None:
        """
        更新坦克狀態

        每幀調用一次，用於更新無敵時間計時器和其他時間相關的狀態。
        """
        # 更新無敵時間
        if self.invincible:
            self.invincible_time -= pygame.time.get_ticks()
            # 注意：這裡需要在外部追蹤時間，所以使用幀時間更新
            # 正確的實現應由 Game 類控制時間流逝
            if self.invincible_time <= 0:
                self.invincible = False
                self.invincible_time = 0

    def set_direction(self, direction: Literal["up", "down", "left", "right"]) -> None:
        """
        設定坦克方向

        更改坦克朝向並重繪坦克圖像。

        參數：
            direction: 新方向 ("up", "down", "left", "right")
        """
        if direction in ("up", "down", "left", "right"):
            if self.direction != direction:
                self.direction = direction
                self._draw_tank_image()

    def get_position(self) -> Tuple[float, float]:
        """
        取得坦克當前位置

        返回：
            Tuple[float, float] - (x, y) 座標
        """
        return (self.x, self.y)

    def get_lives(self) -> int:
        """
        取得坦克剩餘生命數

        返回：
            int - 生命數
        """
        return self.lives

    def draw(self, surface: pygame.Surface) -> None:
        """
        繪製坦克到指定的表面

        參數：
            surface: pygame.Surface - 目標繪製表面（通常是遊戲螢幕）
        """
        surface.blit(self.image, self.rect)

    def handle_input(self, keys) -> None:
        """處理鍵盤輸入
        
        根據按下的方向鍵設置坦克方向。
        
        參數：
            keys: pygame.key.get_pressed() 返回的按鍵狀態
        """
        if keys[pygame.K_UP]:
            self.set_direction("up")
        elif keys[pygame.K_DOWN]:
            self.set_direction("down")
        elif keys[pygame.K_LEFT]:
            self.set_direction("left")
        elif keys[pygame.K_RIGHT]:
            self.set_direction("right")
