"""
地圖類別實現

地圖系統管理遊戲場景，包含磚塊和鋼塊障礙物。
磚塊可被破壞，鋼塊不可破壞。遊戲開始時隨機生成 30-50 個障礙物。
"""

import random
from typing import List

import pygame


class Brick(pygame.sprite.Sprite):
    """
    磚塊精靈類別

    可破壞的障礙物，棕色，玩家子彈可以摧毀。

    屬性：
        rect: pygame.Rect - 磚塊的矩形碰撞區域
        image: pygame.Surface - 磚塊的可視化圖像
    """

    # 磚塊常數設定
    SIZE = 40  # 格子大小（像素）
    COLOR = (139, 69, 19)  # 棕色 (RGB)

    def __init__(self, grid_x: int, grid_y: int) -> None:
        """
        初始化磚塊

        參數：
            grid_x: 格子X座標（0-19）
            grid_y: 格子Y座標（0-14）
        """
        super().__init__()

        # 計算像素座標
        self.x = grid_x * self.SIZE
        self.y = grid_y * self.SIZE

        # 建立磚塊圖像
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(self.COLOR)

        # 設定碰撞矩形位置
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def destroy(self) -> None:
        """
        摧毀磚塊，將其從遊戲中移除
        """
        self.kill()

    def draw(self, surface: pygame.Surface) -> None:
        """
        繪製磚塊到指定的表面

        參數：
            surface: pygame.Surface - 目標繪製表面（通常是遊戲螢幕）
        """
        surface.blit(self.image, self.rect)


class Steel(pygame.sprite.Sprite):
    """
    鋼塊精靈類別

    不可破壞的障礙物，灰色，玩家子彈無法摧毀。

    屬性：
        rect: pygame.Rect - 鋼塊的矩形碰撞區域
        image: pygame.Surface - 鋼塊的可視化圖像
    """

    # 鋼塊常數設定
    SIZE = 40  # 格子大小（像素）
    COLOR = (128, 128, 128)  # 灰色 (RGB)

    def __init__(self, grid_x: int, grid_y: int) -> None:
        """
        初始化鋼塊

        參數：
            grid_x: 格子X座標（0-19）
            grid_y: 格子Y座標（0-14）
        """
        super().__init__()

        # 計算像素座標
        self.x = grid_x * self.SIZE
        self.y = grid_y * self.SIZE

        # 建立鋼塊圖像
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(self.COLOR)

        # 設定碰撞矩形位置
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface: pygame.Surface) -> None:
        """
        繪製鋼塊到指定的表面

        參數：
            surface: pygame.Surface - 目標繪製表面（通常是遊戲螢幕）
        """
        surface.blit(self.image, self.rect)


class Map:
    """
    遊戲地圖類別

    管理遊戲場景中的所有障礙物（磚塊和鋼塊）。
    支持隨機生成地圖，繪製障礙物，以及管理磚塊的破壞。

    屬性：
        GRID_SIZE: int - 格子大小（40 像素）
        MAP_WIDTH: int - 地圖寬度（20 格 = 800 像素）
        MAP_HEIGHT: int - 地圖高度（15 格 = 600 像素）
        PLAYER_SPAWN_SAFE_ZONE: tuple - 玩家起始安全區域
        OBSTACLE_MIN: int - 最小障礙物數量
        OBSTACLE_MAX: int - 最大障礙物數量
        obstacles: pygame.sprite.Group - 所有障礙物精靈組
        bricks: pygame.sprite.Group - 所有磚塊精靈組
        steels: pygame.sprite.Group - 所有鋼塊精靈組
    """

    # 地圖常數設定
    GRID_SIZE = 40  # 格子大小（像素）
    MAP_WIDTH = 20  # 地圖寬度（格子數）
    MAP_HEIGHT = 15  # 地圖高度（格子數）
    PLAYER_SPAWN_X_MIN = 360  # 玩家起始區域X最小（像素）
    PLAYER_SPAWN_X_MAX = 440  # 玩家起始區域X最大（像素）
    PLAYER_SPAWN_Y_MIN = 520  # 玩家起始區域Y最小（像素）
    PLAYER_SPAWN_Y_MAX = 600  # 玩家起始區域Y最大（像素）
    OBSTACLE_MIN = 30  # 最小障礙物數量
    OBSTACLE_MAX = 50  # 最大障礙物數量

    def __init__(self) -> None:
        """
        初始化遊戲地圖，隨機生成障礙物
        """
        # 初始化精靈組
        self.obstacles = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.steels = pygame.sprite.Group()

        # 隨機生成障礙物
        self._generate_random_obstacles()

    def _generate_random_obstacles(self) -> None:
        """
        隨機生成地圖上的障礙物

        - 隨機選擇 OBSTACLE_MIN 到 OBSTACLE_MAX 個格子
        - 避免在玩家起始區域放置障礙物
        - 隨機決定每個障礙物是磚塊還是鋼塊
        """
        # 計算玩家安全區域的格子範圍
        safe_zone_grid_x_min = self.PLAYER_SPAWN_X_MIN // self.GRID_SIZE
        safe_zone_grid_x_max = (self.PLAYER_SPAWN_X_MAX // self.GRID_SIZE) + 1
        safe_zone_grid_y_min = self.PLAYER_SPAWN_Y_MIN // self.GRID_SIZE
        safe_zone_grid_y_max = (self.PLAYER_SPAWN_Y_MAX // self.GRID_SIZE) + 1

        # 生成有效位置列表（排除玩家安全區域）
        available_positions = []
        for grid_y in range(self.MAP_HEIGHT):
            for grid_x in range(self.MAP_WIDTH):
                # 檢查是否在玩家安全區域內
                if not (
                    safe_zone_grid_x_min <= grid_x <= safe_zone_grid_x_max
                    and safe_zone_grid_y_min <= grid_y <= safe_zone_grid_y_max
                ):
                    available_positions.append((grid_x, grid_y))

        # 隨機選擇障礙物數量
        num_obstacles = random.randint(self.OBSTACLE_MIN, self.OBSTACLE_MAX)

        # 從可用位置中隨機選擇
        selected_positions = random.sample(available_positions, num_obstacles)

        # 建立障礙物
        for grid_x, grid_y in selected_positions:
            # 隨機決定是磚塊還是鋼塊（60% 磚塊，40% 鋼塊）
            if random.random() < 0.6:
                obstacle = Brick(grid_x, grid_y)
                self.bricks.add(obstacle)
            else:
                obstacle = Steel(grid_x, grid_y)
                self.steels.add(obstacle)

            self.obstacles.add(obstacle)

    def draw(self, surface: pygame.Surface) -> None:
        """
        繪製地圖上的所有障礙物

        參數：
            surface: pygame.Surface - 目標繪製表面（通常是遊戲螢幕）
        """
        self.obstacles.draw(surface)

    def get_obstacles_rects(self) -> List[pygame.Rect]:
        """
        取得所有障礙物的碰撞矩形

        返回：
            List[pygame.Rect] - 所有障礙物的矩形列表
        """
        return [obstacle.rect for obstacle in self.obstacles]

    def destroy_brick(self, brick: Brick) -> None:
        """
        摧毀指定的磚塊

        參數：
            brick: Brick - 要摧毀的磚塊物件
        """
        if brick in self.bricks:
            brick.destroy()
            self.obstacles.remove(brick)
