# SlowZone 減速地帶功能設計

## 功能說明

當任何坦克（玩家或敵人）駛入 `slow-speed.jpg` 圖像的格子時，移動速度降至原速度的 50%；離開後自動恢復。

## 架構

### 方案：Map 管理元素，Game 應用效果

符合現有架構：地圖元素由 `Map` 管理，跨元素效果由 `Game` 協調。

---

## 變更清單

### `src/map.py`

1. 新增 `SlowZone` 精靈類
   - 使用 `assets/slow-speed.jpg` 圖像（40×40 px）
   - 可穿越（不加入 `obstacles`），繪製在底層
2. `Map.__init__`
   - 載入 `slow-speed.jpg` 為 `Map.slow_zone_image`
   - 新增 `self.slow_zones = pygame.sprite.Group()`
   - 呼叫 `_generate_slow_zones()`
3. `_generate_slow_zones()`
   - 隨機生成 2-3 個 SlowZone
   - 排除玩家起始安全區域與已有障礙物位置
4. `get_slow_zone_rects() -> List[pygame.Rect]`
   - 回傳所有 SlowZone 的 rect 列表
5. `Map.draw(surface)`
   - 在障礙物後、草叢前繪製 slow_zones

### `src/enemy.py`（EnemyTank）

1. `ENEMY_CONFIGS` 各 type 新增 `base_speed` key（與 `speed` 相同）
2. `__init__` 初始化 `self.base_speed = config["base_speed"]`

### `src/game.py`（Game）

1. `update()` 末尾呼叫 `_apply_slow_zone_effects()`
2. 新增 `_apply_slow_zone_effects()`
   - 取得 `slow_zone_rects = self.map.get_slow_zone_rects()`
   - 玩家：若 rect 與任一 slow_zone 碰撞 → `speed = TANK_SPEED * 0.5`，否則 `speed = TANK_SPEED`
   - 各敵人：若 rect 與任一 slow_zone 碰撞 → `speed = base_speed * 0.5`，否則 `speed = base_speed`

---

## 速度還原基準

| 坦克 | 基準屬性 |
|------|---------|
| PlayerTank | `PlayerTank.TANK_SPEED`（類別常數） |
| EnemyTank | `enemy.base_speed`（實例屬性，依類型而異） |

## 不涉及變更

- `src/tank.py` 的 `PlayerTank` 無需新增 `base_speed` 實例屬性，直接參照類別常數 `TANK_SPEED`
- 子彈速度、射擊冷卻不受影響
