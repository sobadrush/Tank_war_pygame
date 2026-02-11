"""
坦克大戰遊戲主程式

使用 pygame 開發的經典街機遊戲實現。
視窗尺寸：800x600 像素
"""

import sys

try:
    import pygame
except ImportError:
    print("錯誤：未找到 pygame 套件。")
    print("請運行以下命令安裝依賴：")
    print("  uv sync")
    print("或")
    print("  pip install pygame-ce>=2.5.0")
    sys.exit(1)

from src.game import Game


def main() -> None:
    """
    遊戲主程式進入點。

    初始化 pygame 並啟動遊戲主循環。
    視窗尺寸為 800x600 像素。
    """
    # 初始化 pygame
    pygame.init()

    # 設定遊戲視窗
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = "坦克大戰"
    FPS = 60

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # 建立時鐘物件用於控制幀率
    clock = pygame.time.Clock()

    # 顏色常數（RGB 格式）
    BLACK = (0, 0, 0)

    # 創建遊戲實例
    game = Game()

    # 遊戲運行標誌
    running = True

    # 主遊戲循環
    while running:
        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # ESC 鍵退出遊戲
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Q 鍵也可以退出
                elif event.key == pygame.K_q:
                    running = False
                # 空格鍵射擊
                elif event.key == pygame.K_SPACE:
                    game.player_shoot()

        # 檢查遊戲結束條件
        if game.game_over:
            # 顯示遊戲結束畫面
            screen.fill(BLACK)
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 36)
            score_text = font_small.render(f"Final Score: {game.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            screen.blit(score_text, score_rect)
            
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            continue

        if game.game_won:
            # 顯示勝利畫面
            screen.fill(BLACK)
            font = pygame.font.Font(None, 74)
            text = font.render("VICTORY!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 36)
            score_text = font_small.render(f"Final Score: {game.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            screen.blit(score_text, score_rect)
            
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            continue

        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()

        # 更新遊戲狀態
        game.update(keys)

        # 清除螢幕（用黑色填充）
        screen.fill(BLACK)

        # 繪製遊戲元素
        game.draw(screen)

        # 更新顯示
        pygame.display.flip()

        # 控制幀率
        clock.tick(FPS)

    # 清理資源並結束
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
