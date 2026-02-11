"""
子彈類別實現

子彈是遊戲中的可射擊物體，由玩家或敵人發射。
子彈以直線移動，飛出邊界時被自動移除。
"""

from typing import Literal, Tuple

import pygame


class Bullet(pygame.sprite.Sprite):
    """
    子彈精靈類別

    表示遊戲中的子彈，包含位置、速度、方向等屬性。
    子彈會自動在邊界外時標記為移除。

    屬性：
        rect: pygame.Rect - 子彈的矩形碰撞區域
        x: float - 水平位置（像素）
        y: float - 垂直位置（像素）
        direction: Tuple[int, int] - 移動方向向量 (-1, 0, 1)
        speed: float - 移動速度（像素/幀）
        damage: int - 子彈傷害值
        owner: str - 所有者（'player' 或 'enemy'）
    """

    # 子彈常數設定
    BULLET_RADIUS = 4  # 子彈半徑（8-10 像素直徑）
    BULLET_SPEED = 8  # 子彈速度（像素/幀）
    BULLET_COLOR = (255, 255, 0)  # 黃色 (RGB)
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    def __init__(
        self,
        x: float,
        y: float,
        direction: Tuple[int, int],
        owner: Literal["player", "enemy"] = "player",
        damage: int = 1,
    ) -> None:
        """
        初始化子彈

        參數：
            x: 初始水平位置（像素）
            y: 初始垂直位置（像素）
            direction: 移動方向向量，例如 (1, 0) 表示向右，(0, -1) 表示向上
            owner: 所有者，'player' 或 'enemy'
            damage: 傷害值，預設 1
        """
        super().__init__()

        # 位置屬性
        self.x = float(x)
        self.y = float(y)

        # 方向和速度
        self.direction = direction
        self.speed = self.BULLET_SPEED

        # 子彈屬性
        self.damage = damage
        self.owner = owner

        # 建立子彈圖像（黃色圓形）
        self.image = pygame.Surface(
            (self.BULLET_RADIUS * 2, self.BULLET_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image,
            self.BULLET_COLOR,
            (self.BULLET_RADIUS, self.BULLET_RADIUS),
            self.BULLET_RADIUS,
        )

        # 建立碰撞矩形
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self) -> None:
        """
        更新子彈位置並檢查邊界

        每幀調用一次，移動子彈並移除超出邊界的子彈。
        """
        # 計算新位置
        # 移動方向的向量乘以速度
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # 更新矩形位置
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # 邊界檢測：如果子彈飛出邊界，標記為移除
        if not self._is_in_bounds():
            self.kill()

    def _is_in_bounds(self) -> bool:
        """
        檢查子彈是否在遊戲邊界內

        返回：
            bool - 子彈在邊界內返回 True，否則返回 False
        """
        return (
            -self.BULLET_RADIUS <= self.x <= self.WINDOW_WIDTH + self.BULLET_RADIUS
            and -self.BULLET_RADIUS <= self.y <= self.WINDOW_HEIGHT + self.BULLET_RADIUS
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        繪製子彈到指定的表面

        參數：
            surface: pygame.Surface - 目標繪製表面（通常是遊戲螢幕）
        """
        surface.blit(self.image, self.rect)

    def get_position(self) -> Tuple[float, float]:
        """
        取得子彈當前位置

        返回：
            Tuple[float, float] - (x, y) 座標
        """
        return (self.x, self.y)

    def get_owner(self) -> Literal["player", "enemy"]:
        """
        取得子彈所有者

        返回：
            str - 'player' 或 'enemy'
        """
        return self.owner

    def get_damage(self) -> int:
        """
        取得子彈傷害值

        返回：
            int - 傷害值
        """
        return self.damage
