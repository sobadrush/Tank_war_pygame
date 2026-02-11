# 經典坦克大戰遊戲

## TL;DR

> **Quick Summary**: 使用 Python3 + pygame + uv 構建經典坦克大戰遊戲，程序生成圖形，支援單人任務模式，視窗大小 800x600。
>
> **Deliverables**:
> - Python 遊戲專案（完整可玩）
> - uv 項目配置（pyproject.toml）
> - 程序生成的圖形資源
> - 遊戲循環與所有核心機制
>
> **Estimated Effort**: Medium
> **Parallel Execution**: NO - sequential (有依賴關係)
> **Critical Path**: 設定環境 → 遊戲架構 → 玩家坦克 → 敵人AI → 地圖系統 → 遊戲循環整合 → QA 驗證

---

## Context

### Original Request
請設計規劃一個經典的坦克大戰遊戲，環境：python3, pygame, 使用 uv 進行套件及虛擬環境管理

### Interview Summary

**Key Discussions**:
- **功能範圍**: 基礎版本（玩家坦克移動/射擊、簡單敵人、基礎地圖）
- **圖片資源**: 程序生成（pygame 繪圖 API）- 不需要外部圖片
- **預期用途**: 完整作品（可玩的遊戲體驗）
- **視窗大小**: 800x600
- **遊戲模式**: 任務模式（消滅所有敵人即可獲勝）
- **地圖佈局**: 隨機生成型（隨機生成障礙物）
- **敵人數量**: 3-5 台同時出現
- **測試策略**: 無自動化測試，使用 Agent-Executed QA 驗證

**Research Findings**:
- pygame 2.6.0 (2024 年 6 月發布) 是最新版本
- uv 是由 Astral 打造的極速 Python 套件管理工具（比 pip 快 10-100 倍）
- pygame sprite 模組適合管理遊戲物件
- pygame.Rect 用於碰撞檢測和位置管理
- 程序生成圖形使用 pygame.draw 模組

### Metis Review

**Identified Gaps** (addressed):
- **地圖尺寸參數**: 設定為網格系統（例如 20x15，每格 40x40 像素）
- **碰撞檢測**: 需要實現坦克之間、坦克與子彈、坦克與障礙物的碰撞
- **遊戲狀態管理**: 需要實現開始、遊戲中、勝利、失敗等狀態

---

## Work Objectives

### Core Objective
構建一個完整的、可玩的 Python 坦克大戰遊戲，使用程序生成圖形，支援單人任務模式，消滅所有敵人即可獲勝。

### Concrete Deliverables
- `pyproject.toml`: uv 專案配置檔
- `main.py`: 遊戲主程式
- `src/tank.py`: 玩家坦克類別
- `src/enemy.py`: 敵人坦克類別
- `src/bullet.py`: 子彈類別
- `src/map.py`: 地圖類別
- `src/game.py`: 遊戲管理器類別
- `README.md`: 專案說明文件

### Definition of Done
- [x] 遊戲可啟動（`uv run python main.py`）
- [x] 玩家可用方向鍵移動、空格鍵射擊
- [x] 敵人自動移動和射擊
- [x] 地圖隨機生成障礙物
- [x] 碰撞檢測正常運作
- [x] 勝利/失敗邏輯正確
- [x] 計分系統運作

### Must Have
- 玩家坦克（移動：上下左右；射擊：空格鍵）
- 簡單敵人（自動移動和射擊）
- 基礎地圖系統（磚塊：可破壞；鋼塊：不可破壞）
- 生命值系統（玩家 3 顆生命）
- 計分系統（消滅敵人得分）
- 勝利條件（消滅所有敵人）
- 失敗條件（玩家生命歸零）

### Must NOT Have (Guardrails)
- 道具系統（星星、時鐘等加強道具）- 控制範圍
- 關卡進度系統（單一關卡即可）- 控制範圍
- 音效（不在範圍內）- 控制範圍
- 多人模式（單人遊戲）- 控制範圍
- 外部圖片資源（程序生成）- 技術限制

---

## Verification Strategy (MANDATORY)

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
>
> ALL tasks in this plan MUST be verifiable WITHOUT any human action.
> This is NOT conditional — it applies to EVERY task, regardless of test strategy.
>
> **FORBIDDEN** — acceptance criteria that require:
> - "User manually tests..." / "使用者手動測試..."
> - "User visually confirms..." / "使用者視覺確認..."
> - "User interacts with..." / "使用者互動..."
> - "Ask user to verify..." / "請使用者驗證..."
> - ANY step where a human must perform an action
>
> **ALL verification is executed by the agent** using tools (Playwright, interactive_bash, curl, etc.). No exceptions.

### Test Decision
- **Infrastructure exists**: NO
- **Automated tests**: None
- **Framework**: None

### If TDD Enabled

不適用（使用者選擇無自動化測試）

### Agent-Executed QA Scenarios (MANDATORY — ALL tasks)

> Whether TDD is enabled or not, EVERY task MUST include Agent-Executed QA Scenarios.
> - **With TDD**: QA scenarios complement unit tests at integration/E2E level
> - **Without TDD**: QA scenarios are the PRIMARY verification method
>
> These describe how the executing agent DIRECTLY verifies the deliverable
> by running it — opening browsers, executing commands, sending API requests.
> The agent performs what a human tester would do, but automated via tools.

**Verification Tool by Deliverable Type:**

| Type | Tool | How Agent Verifies |
|------|------|-------------------|
| **CLI/Application** | interactive_bash (tmux) | Run command, send keystrokes, validate output, capture screenshots |
| **Library/Module** | Bash (uv/python REPL) | Import, call functions, compare output |

**Each Scenario MUST Follow This Format:**

```
Scenario: [Descriptive name — what user action/flow is being verified]
  Tool: [interactive_bash / Bash]
  Preconditions: [What must be true before this scenario runs]
  Steps:
    1. [Exact action with specific command/keystroke]
    2. [Next action with expected intermediate state]
    3. [Assertion with exact expected value]
  Expected Result: [Concrete, observable outcome]
  Failure Indicators: [What would indicate failure]
  Evidence: [Screenshot path / output capture / log file path]
```

**Scenario Detail Requirements:**
- **Commands**: Specific commands with arguments (`uv run python main.py`, not "run the game")
- **Keystrokes**: Concrete keystrokes (`ArrowUp`, not "press up")
- **Assertions**: Exact values (`Score: 100`, not "verify score updates")
- **Timing**: Include wait conditions where relevant
- **Negative Scenarios**: At least ONE failure/error scenario per feature
- **Evidence Paths**: Specific file paths (`.sisyphus/evidence/task-N-scenario-name.{png,txt}`)

**Anti-patterns (NEVER write scenarios like this):**
- ❌ "Verify the game works correctly"
- ❌ "Check that the player can move"
- ❌ "Test the collision detection"
- ❌ "User runs the game and confirms..."

**Write scenarios like this instead:**
- ✅ `Run "uv run python main.py" → Wait for game window → Send ArrowUp → Wait 1s → Send ArrowRight → Wait 1s → Screenshot .sisyphus/evidence/task-1-player-movement.png → Assert tank moved from initial position`
- ✅ `Run "uv run python main.py" → Wait for game window → Send Space → Wait 0.5s → Check bullet exists on screen → Screenshot .sisyphus/evidence/task-2-shooting.png`
- ✅ `Run "uv run python main.py" → Wait for game window → Wait for enemy to spawn → Send ArrowUp repeatedly to move player → Wait for enemy bullet → Check if collision detection works`

**Evidence Requirements:**
- Screenshots: `.sisyphus/evidence/` for all game state verifications
- Terminal output: Captured for CLI verifications
- All evidence referenced by specific file path in acceptance criteria

---

## Execution Strategy

### Parallel Execution Waves

> Maximize throughput by grouping independent tasks into parallel waves.
> Each wave completes before the next begins.

```
Wave 1 (Start Immediately):
├── Task 1: 建立專案結構和 uv 配置
└── Task 2: 安裝依賴（pygame）

Wave 2 (After Wave 1):
├── Task 3: 實現子彈類別
├── Task 4: 實現地圖類別
└── Task 5: 實現玩家坦克類別

Wave 3 (After Wave 2):
└── Task 6: 實現敵人坦克類別

Wave 4 (After Wave 3):
└── Task 7: 實現遊戲管理器類別

Wave 5 (After Wave 4):
├── Task 8: 實現遊戲主循環
└── Task 9: 整合所有元件

Wave 6 (After Wave 5):
└── Task 10: 完整 QA 驗證

Critical Path: Task 1 → Task 5 → Task 6 → Task 7 → Task 8 → Task 9 → Task 10
Parallel Speedup: ~30% faster than sequential
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2 | - |
| 2 | 1 | 3,4,5 | - |
| 3 | 2 | 7 | 4,5 |
| 4 | 2 | 7 | 3,5 |
| 5 | 2 | 6 | 3,4 |
| 6 | 5 | 7 | - |
| 7 | 3,4,6 | 8 | - |
| 8 | 7 | 9 | - |
| 9 | 8 | 10 | - |
| 10 | 9 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1, 2 | task(category="quick", load_skills=["python-expert"], run_in_background=false) |
| 2 | 3, 4, 5 | dispatch parallel after Wave 1 completes |
| 3 | 6 | task(category="quick", load_skills=["python-expert"], run_in_background=false) |
| 4 | 7 | task(category="unspecified-high", load_skills=["python-expert"], run_in_background=false) |
| 5 | 8, 9 | task(category="unspecified-high", load_skills=["python-expert"], run_in_background=false) |
| 6 | 10 | task(category="unspecified-high", load_skills=["python-expert"], run_in_background=false) |

---

## TODOs

> Implementation + Test = ONE Task. Never separate.
> EVERY task MUST have: Recommended Agent Profile + Parallelization info.

- [x] 1. 建立專案結構和 uv 配置

  **What to do**:
  - [x] 建立專案目錄結構：`src/`, `.sisyphus/evidence/`
  - [x] 創建 `pyproject.toml` 配置文件
  - [x] 設定專案名稱、Python 版本要求（>=3.9）
  - [x] 添加 pygame 依賴
  - [x] 創建 `README.md` 說明文件
  - [x] 創建 `main.py` 主程式骨架

  **Must NOT do**:
  - 不要安裝其他不必要的套件
  - 不要創建複雜的目錄結構

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: 專案設定是明確、標準化的任務，可以快速完成
  - **Skills**: [`python-expert`]
    - `python-expert`: 精通 Python 與 uv 環境管理，確保專案配置正確
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (起始任務)
  - **Blocks**: Task 2
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - (無現有代碼可參考)

  **API/Type References** (contracts to implement against):
  - uv 官方文檔: https://docs.astral.sh/uv/configuration/ - pyproject.toml 結構
  - Python 版本要求: PEP 440 - 版本指定格式

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - uv pyproject.toml 文檔 - 專案配置結構

  **External References** (libraries and frameworks):
  - uv 官方文檔: https://docs.astral.sh/uv/
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - uv 官方文檔: 提供 pyproject.toml 的正確結構和依賴聲明方式
  - Python 版本要求: 確保專案在正確的 Python 版本上運行
  - pygame 官方文檔: 了解 pygame 的基本結構和最佳實踐

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 專案結構和配置文件正確創建**
    Tool: Bash
    Preconditions: None
    Steps:
      1. `ls -la` → Assert output contains `pyproject.toml`, `main.py`, `README.md`, `src/`
      2. `cat pyproject.toml` → Assert contains `[project]`, `name = "tank-war"`, `dependencies = ["pygame"]`
      3. `uv python --version` → Assert Python version >= 3.9
      4. `uv sync --dry-run` → Assert command succeeds without errors
    Expected Result: 專案結構正確，配置文件有效
    Evidence: Terminal output captured in .sisyphus/evidence/task-1-project-structure.txt

  **Scenario: README.md 包含基本說明**
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. `cat README.md` → Assert contains "坦克大戰", "Python", "pygame", "uv"
      2. `grep -q "運行方式" README.md` → Assert exit code 0 (找到運行說明)
      3. `grep -q "uv run python main.py" README.md` → Assert exit code 0 (找到運行命令)
    Expected Result: README 包含完整的使用說明
    Evidence: README.md content in .sisyphus/evidence/task-1-readme.txt

  **Evidence to Capture**:
  - [x] 專案結構輸出：.sisyphus/evidence/task-1-project-structure.txt
  - [x] README.md 內容：.sisyphus/evidence/task-1-readme.txt
  - [x] pyproject.toml 內容：.sisyphus/evidence/task-1-pyproject.txt

  **Commit**: YES
  - Message: `feat: 建立專案結構和 uv 配置`
  - Files: `pyproject.toml`, `README.md`, `main.py`
  - Pre-commit: `uv sync --dry-run`

---

- [x] 2. 安裝依賴（pygame）

  **What to do**:
  - [x] 使用 `uv sync` 安裝所有依賴
  - [x] 驗證 pygame 安裝成功
  - [x] 創建簡單的 pygame 測試程式來驗證環境

  **Must NOT do**:
  - 不要安裝其他不必要的套件

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: 依賴安裝是標準化任務，可以快速完成
  - **Skills**: [`python-expert`]
    - `python-expert`: 精通 uv 環境管理和套件安裝
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (依賴 Task 1)
  - **Blocks**: Task 3, 4, 5
  - **Blocked By**: Task 1

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - (無現有代碼可參考)

  **API/Type References** (contracts to implement against):
  - uv sync 命令: https://docs.astral.sh/uv/cli/sync/ - 同步依賴
  - pygame 安裝驗證: https://www.pygame.org/wiki/GettingStarted - 測試 pygame 環境

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - uv sync 文檔: 確保正確使用 uv 安裝依賴
  - pygame GettingStarted: 驗證 pygame 安裝成功的方法

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: pygame 依賴安裝成功**
    Tool: Bash
    Preconditions: pyproject.toml exists with pygame dependency
    Steps:
      1. `uv sync` → Assert command completes without errors
      2. `uv pip list` → Assert output contains "pygame"
      3. `uv run python -c "import pygame; print(pygame.version.ver)"` → Assert prints pygame version (e.g., "2.6.0")
    Expected Result: pygame 成功安裝並可匯入
    Evidence: Terminal output captured in .sisyphus/evidence/task-2-install-output.txt

  **Scenario: pygame 基本功能測試**
    Tool: Bash
    Preconditions: pygame installed
    Steps:
      1. Create test script:
         ```python
         import pygame
         pygame.init()
         print("pygame initialized successfully")
         pygame.quit()
         ```
      2. `uv run python test_pygame.py` → Assert output contains "pygame initialized successfully"
      3. Assert exit code is 0
    Expected Result: pygame 可以正常初始化和關閉
    Evidence: Test output in .sisyphus/evidence/task-2-pygame-test.txt

  **Evidence to Capture**:
  - [x] 安裝輸出：.sisyphus/evidence/task-2-install-output.txt
  - [x] pygame 測試輸出：.sisyphus/evidence/task-2-pygame-test.txt

  **Commit**: YES
  - Message: `chore: 安裝 pygame 依賴`
  - Files: `uv.lock` (generated)
  - Pre-commit: `uv run python -c "import pygame"`

---

- [x] 3. 實現子彈類別

  **What to do**:
  - [x] 創建 `src/bullet.py` 文件
  - [x] 實現 Bullet 類別（繼承 pygame.sprite.Sprite）
  - [x] 實現子彈屬性：位置、速度、方向、傷害值
  - [x] 實現 update() 方法（移動子彈）
  - [x] 實現 draw() 方法（程序生成子彈圖形）
  - [x] 實現碰撞檢測方法
  - [x] 添加子彈飛出邊界的處理邏輯

  **Must NOT do**:
  - 不要使用外部圖片資源
  - 不要實現複雜的子彈物理效果（保持直線移動）

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: 子彈類別相對簡單，邏輯清晰
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 2

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - (無現有代碼可參考)

  **API/Type References** (contracts to implement against):
  - pygame.sprite.Sprite: https://www.pygame.org/docs/ref/sprite.html - 精靈基類
  - pygame.draw.circle: https://www.pygame.org/docs/ref/draw.html - 繪製圓形（程序生成子彈）
  - pygame.Rect: https://www.pygame.org/docs/ref/rect.html - 矩形碰撞檢測

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame sprite 文檔: https://www.pygame.org/docs/ref/sprite.html

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - pygame.sprite.Sprite: Bullet 類別需要繼承這個基類以獲得精靈功能
  - pygame.draw.circle: 使用程序生成繪製子彈（圓形）
  - pygame.Rect: 用於子彈的碰撞檢測

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 子彈可以正確建立和初始化**
    Tool: Bash
    Preconditions: Bullet class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from bullet import Bullet
         import pygame
         pygame.init()
         bullet = Bullet(x=100, y=100, direction=(1, 0), owner='player')
         print(f"Bullet created at ({bullet.rect.x}, {bullet.rect.y})")
         print(f"Bullet speed: {bullet.speed}")
         pygame.quit()
         ```
      2. `uv run python test_bullet_init.py` → Assert output contains "Bullet created"
      3. Assert no errors or exceptions
    Expected Result: 子彈物件正確初始化，屬性設定正確
    Evidence: Test output in .sisyphus/evidence/task-3-bullet-init.txt

  **Scenario: 子彈可以正確移動**
    Tool: Bash
    Preconditions: Bullet class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from bullet import Bullet
         import pygame
         pygame.init()
         bullet = Bullet(x=100, y=100, direction=(1, 0), owner='player')
         initial_x = bullet.rect.x
         bullet.update()
         final_x = bullet.rect.x
         print(f"Initial X: {initial_x}, Final X: {final_x}, Moved: {final_x > initial_x}")
         pygame.quit()
         ```
      2. `uv run python test_bullet_move.py` → Assert output contains "Moved: True"
      3. Assert final_x > initial_x (子彈向右移動)
    Expected Result: 子彈在調用 update() 後正確移動
    Evidence: Test output in .sisyphus/evidence/task-3-bullet-move.txt

  **Scenario: 子彈飛出邊界時被標記為刪除**
    Tool: Bash
    Preconditions: Bullet class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from bullet import Bullet
         import pygame
         pygame.init()
         bullet = Bullet(x=790, y=100, direction=(1, 0), owner='player')  # 接近右邊界
         print(f"Before update: {bullet.rect.right}")
         bullet.update()
         print(f"After update: {bullet.rect.right}, alive: {bullet.alive()}")
         pygame.quit()
         ```
      2. `uv run python test_bullet_boundary.py` → Assert output contains "alive: False"
    Expected Result: 子彈飛出邊界時被標記為刪除
    Evidence: Test output in .sisyphus/evidence/task-3-bullet-boundary.txt

  **Evidence to Capture**:
  - [x] 子彈初始化測試：.sisyphus/evidence/task-3-bullet-init.txt
  - [x] 子彈移動測試：.sisyphus/evidence/task-3-bullet-move.txt
  - [x] 子彈邊界測試：.sisyphus/evidence/task-3-bullet-boundary.txt

  **Commit**: YES
  - Message: `feat: 實現子彈類別`
  - Files: `src/bullet.py`
  - Pre-commit: `uv run python -c "from src.bullet import Bullet; print('OK')"`

---

- [x] 4. 實現地圖類別

  **What to do**:
  - [x] 創建 `src/map.py` 文件
  - [x] 定義地圖格子大小（例如 40x40 像素）
  - [x] 定義地圖尺寸（例如 20x15 格子，800x600 像素）
  - [x] 實現地圖元素類別：磚塊（可破壞）、鋼塊（不可破壞）
  - [x] 實現隨機生成地圖邏輯（隨機散佈障礙物）
  - [x] 實現 draw() 方法（程序生成磚塊和鋼塊圖形）
  - [x] 實現獲取地圖元素的碰撞矩形方法
  - [x] 實現破壞磚塊的方法

  **Must NOT do**:
  - 不要使用外部圖片資源
  - 不要實現過於複雜的地圖生成算法（隨機散佈即可）

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: 地圖類別相對簡單，使用隨機生成
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 2

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - (無現有代碼可參考)

  **API/Type References** (contracts to implement against):
  - pygame.sprite.Sprite: https://www.pygame.org/docs/ref/sprite.html - 精靈基類
  - pygame.draw.rect: https://www.pygame.org/docs/ref/draw.html - 繪製矩形（程序生成磚塊）
  - pygame.Rect: https://www.pygame.org/docs/ref/rect.html - 矩形碰撞檢測

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame sprite 文檔: https://www.pygame.org/docs/ref/sprite.html

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - pygame.sprite.Sprite: 地圖元素類別需要繼承這個基類
  - pygame.draw.rect: 使用程序生成繪製磚塊和鋼塊（矩形）
  - pygame.Rect: 用於地圖元素的碰撞檢測

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 地圖可以正確建立並隨機生成障礙物**
    Tool: Bash
    Preconditions: Map class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from map import Map
         import pygame
         pygame.init()
         game_map = Map()
         print(f"Map size: {game_map.width}x{game_map.height}")
         print(f"Obstacles count: {len(game_map.obstacles)}")
         print(f"Bricks: {len([o for o in game_map.obstacles if o.type == 'brick'])}")
         print(f"Steels: {len([o for o in game_map.obstacles if o.type == 'steel'])}")
         pygame.quit()
         ```
      2. `uv run python test_map_init.py` → Assert output contains "Obstacles count:"
      3. Assert obstacles count > 0 (有生成障礙物)
    Expected Result: 地圖正確建立，隨機生成障礙物
    Evidence: Test output in .sisyphus/evidence/task-4-map-init.txt

  **Scenario: 地圖可以正確繪製**
    Tool: interactive_bash (tmux)
    Preconditions: Map class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from map import Map
         import pygame
         pygame.init()
         screen = pygame.display.set_mode((800, 600))
         game_map = Map()
         screen.fill((0, 0, 0))
         game_map.draw(screen)
         pygame.image.save(screen, '.sisyphus/evidence/task-4-map-draw.png')
         print("Map drawn and saved")
         pygame.quit()
         ```
      2. `uv run python test_map_draw.py` → Assert output contains "Map drawn and saved"
      3. Check if `.sisyphus/evidence/task-4-map-draw.png` exists
    Expected Result: 地圖正確繪製到螢幕並保存截圖
    Evidence: Map screenshot .sisyphus/evidence/task-4-map-draw.png

  **Scenario: 地圖磚塊可以被破壞**
    Tool: Bash
    Preconditions: Map class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from map import Map
         import pygame
         pygame.init()
         game_map = Map()
         brick = [o for o in game_map.obstacles if o.type == 'brick'][0]
         print(f"Before destroy: bricks={len([o for o in game_map.obstacles if o.type == 'brick'])}")
         brick.destroy()
         game_map.obstacles.remove(brick)
         print(f"After destroy: bricks={len([o for o in game_map.obstacles if o.type == 'brick'])}")
         pygame.quit()
         ```
      2. `uv run python test_map_destroy.py` → Assert "After destroy" count is less than "Before destroy"
    Expected Result: 磚塊可以被破壞並從地圖中移除
    Evidence: Test output in .sisyphus/evidence/task-4-map-destroy.txt

  **Evidence to Capture**:
  - [x] 地圖初始化測試：.sisyphus/evidence/task-4-map-init.txt
  - [x] 地圖繪製截圖：.sisyphus/evidence/task-4-map-draw.png
  - [x] 地圖破壞測試：.sisyphus/evidence/task-4-map-destroy.txt

  **Commit**: YES
  - Message: `feat: 實現地圖類別`
  - Files: `src/map.py`
  - Pre-commit: `uv run python -c "from src.map import Map; print('OK')"`

---

- [x] 5. 實現玩家坦克類別

  **What to do**:
  - [x] 創建 `src/tank.py` 文件
  - [x] 實現 PlayerTank 類別（繼承 pygame.sprite.Sprite）
  - [x] 實現玩家坦克屬性：位置、速度、方向、生命值
  - [x] 實現繪製方法（程序生成坦克圖形）
  - [x] 實現移動方法（上下左右鍵控制）
  - [x] 實現射擊方法（空格鍵發射子彈）
  - [x] 實現碰撞檢測（與地圖障礙物、敵人子彈）
  - [x] 實現生命值減少和死亡邏輯
  - [x] 實現重生邏輯（生命用盡後遊戲結束）

  **Must NOT do**:
  - 不要使用外部圖片資源
  - 不要實現複雜的坦克物理效果

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: 玩家坦克類別邏輯相對清晰
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4)
  - **Blocks**: Task 6
  - **Blocked By**: Task 2

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - `src/bullet.py`: 子彈類別實現（玩家坦克需要使用）

  **API/Type References** (contracts to implement against):
  - pygame.sprite.Sprite: https://www.pygame.org/docs/ref/sprite.html - 精靈基類
  - pygame.draw: https://www.pygame.org/docs/ref/draw.html - 繪製幾何圖形
  - pygame.Rect: https://www.pygame.org/docs/ref/rect.html - 矩形碰撞檢測
  - pygame.KEYDOWN: https://www.pygame.org/docs/ref/event.html - 鍵盤事件處理

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame event 文檔: https://www.pygame.org/docs/ref/event.html

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - pygame.sprite.Sprite: PlayerTank 類別需要繼承這個基類
  - pygame.draw: 使用程序生成繪製坦克（矩形、線條等）
  - pygame.Rect: 用於坦克的碰撞檢測
  - pygame.KEYDOWN: 處理玩家輸入（方向鍵、空格鍵）

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 玩家坦克可以正確建立和初始化**
    Tool: Bash
    Preconditions: PlayerTank class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from tank import PlayerTank
         import pygame
         pygame.init()
         tank = PlayerTank(x=100, y=100)
         print(f"Tank created at ({tank.rect.x}, {tank.rect.y})")
         print(f"Lives: {tank.lives}, Speed: {tank.speed}")
         pygame.quit()
         ```
      2. `uv run python test_tank_init.py` → Assert output contains "Tank created"
      3. Assert no errors or exceptions
    Expected Result: 玩家坦克物件正確初始化，屬性設定正確
    Evidence: Test output in .sisyphus/evidence/task-5-tank-init.txt

  **Scenario: 玩家坦克可以正確移動**
    Tool: interactive_bash (tmux)
    Preconditions: PlayerTank class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from tank import PlayerTank
         import pygame
         pygame.init()
         screen = pygame.display.set_mode((800, 600))
         tank = PlayerTank(x=400, y=300)
         initial_pos = (tank.rect.x, tank.rect.y)
         print(f"Initial position: {initial_pos}")
         # Simulate moving up
         tank.direction = 'up'
         for _ in range(10):
             tank.update()
         final_pos = (tank.rect.x, tank.rect.y)
         print(f"Final position: {final_pos}")
         print(f"Moved up: {final_pos[1] < initial_pos[1]}")
         screen.fill((0, 0, 0))
         tank.draw(screen)
         pygame.image.save(screen, '.sisyphus/evidence/task-5-tank-move.png')
         pygame.quit()
         ```
      2. `uv run python test_tank_move.py` → Assert output contains "Moved up: True"
      3. Check if `.sisyphus/evidence/task-5-tank-move.png` exists
    Expected Result: 玩家坦克可以向上移動
    Evidence: Tank movement screenshot .sisyphus/evidence/task-5-tank-move.png

  **Scenario: 玩家坦克可以發射子彈**
    Tool: Bash
    Preconditions: PlayerTank class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from tank import PlayerTank
         from bullet import Bullet
         import pygame
         pygame.init()
         tank = PlayerTank(x=400, y=300)
         tank.direction = 'right'
         bullet = tank.shoot()
         print(f"Bullet created: {bullet is not None}")
         if bullet:
             print(f"Bullet direction: {bullet.direction}")
         pygame.quit()
         ```
      2. `uv run python test_tank_shoot.py` → Assert output contains "Bullet created: True"
      3. Assert bullet direction matches tank direction
    Expected Result: 玩家坦克可以發射子彈
    Evidence: Test output in .sisyphus/evidence/task-5-tank-shoot.txt

  **Evidence to Capture**:
  - [x] 坦克初始化測試：.sisyphus/evidence/task-5-tank-init.txt
  - [x] 坦克移動截圖：.sisyphus/evidence/task-5-tank-move.png
  - [x] 坦克射擊測試：.sisyphus/evidence/task-5-tank-shoot.txt

  **Commit**: YES
  - Message: `feat: 實現玩家坦克類別`
  - Files: `src/tank.py`
  - Pre-commit: `uv run python -c "from src.tank import PlayerTank; print('OK')"`

---

- [x] 6. 實現敵人坦克類別

  **What to do**:
  - [x] 創建 `src/enemy.py` 文件
  - [x] 實現 EnemyTank 類別（繼承 pygame.sprite.Sprite）
  - [x] 實現敵人坦克屬性：位置、速度、方向、生命值
  - [x] 實現繪製方法（程序生成敵人坦克圖形，不同顏色區分）
  - [x] 實現 AI 移動邏輯（隨機移動或簡單的尋路）
  - [x] 實現射擊方法（定時發射子彈）
  - [x] 實現碰撞檢測（與地圖障礙物、玩家子彈、玩家坦克）
  - [x] 實現死亡邏輯（被擊中後消失）

  **Must NOT do**:
  - 不要使用外部圖片資源
  - 不要實現過於複雜的 AI（隨機移動或簡單模式即可）

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `quick`
    - Reason: 敵人坦克類別邏輯相對清晰
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (依賴 Task 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 5

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - `src/tank.py`: 玩家坦克類別實現（敵人坦克可參考）
  - `src/bullet.py`: 子彈類別實現（敵人坦克需要使用）

  **API/Type References** (contracts to implement against):
  - pygame.sprite.Sprite: https://www.pygame.org/docs/ref/sprite.html - 精靈基類
  - pygame.draw: https://www.pygame.org/docs/ref/draw.html - 繪製幾何圖形
  - pygame.Rect: https://www.pygame.org/docs/ref/rect.html - 矩形碰撞檢測
  - random module: https://docs.python.org/3/library/random.html - 隨機 AI 移動

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame sprite 文檔: https://www.pygame.org/docs/ref/sprite.html
  - Python random 文檔: https://docs.python.org/3/library/random.html

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - pygame.sprite.Sprite: EnemyTank 類別需要繼承這個基類
  - pygame.draw: 使用程序生成繪製敵人坦克（不同顏色）
  - pygame.Rect: 用於敵人坦克的碰撞檢測
  - random module: 實現簡單的 AI 移動邏輯

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 敵人坦克可以正確建立和初始化**
    Tool: Bash
    Preconditions: EnemyTank class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from enemy import EnemyTank
         import pygame
         pygame.init()
         enemy = EnemyTank(x=100, y=100)
         print(f"Enemy created at ({enemy.rect.x}, {enemy.rect.y})")
         print(f"Type: {enemy.type}, Speed: {enemy.speed}")
         pygame.quit()
         ```
      2. `uv run python test_enemy_init.py` → Assert output contains "Enemy created"
      3. Assert no errors or exceptions
    Expected Result: 敵人坦克物件正確初始化，屬性設定正確
    Evidence: Test output in .sisyphus/evidence/task-6-enemy-init.txt

  **Scenario: 敵人坦克可以自動移動**
    Tool: Bash
    Preconditions: EnemyTank class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from enemy import EnemyTank
         import pygame
         pygame.init()
         enemy = EnemyTank(x=100, y=100)
         initial_pos = (enemy.rect.x, enemy.rect.y)
         print(f"Initial position: {initial_pos}")
         for _ in range(10):
             enemy.update()
         final_pos = (enemy.rect.x, enemy.rect.y)
         print(f"Final position: {final_pos}")
         print(f"Moved: {final_pos != initial_pos}")
         pygame.quit()
         ```
      2. `uv run python test_enemy_move.py` → Assert output contains "Moved: True"
    Expected Result: 敵人坦克可以自動移動
    Evidence: Test output in .sisyphus/evidence/task-6-enemy-move.txt

  **Scenario: 敵人坦克可以發射子彈**
    Tool: Bash
    Preconditions: EnemyTank class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from enemy import EnemyTank
         import pygame
         pygame.init()
         enemy = EnemyTank(x=100, y=100)
         enemy.direction = 'right'
         bullet = enemy.shoot()
         print(f"Enemy bullet created: {bullet is not None}")
         if bullet:
             print(f"Bullet owner: {bullet.owner}")
         pygame.quit()
         ```
      2. `uv run python test_enemy_shoot.py` → Assert output contains "Enemy bullet created: True"
      3. Assert bullet owner is 'enemy'
    Expected Result: 敵人坦克可以發射子彈
    Evidence: Test output in .sisyphus/evidence/task-6-enemy-shoot.txt

  **Evidence to Capture**:
  - [x] 敵人初始化測試：.sisyphus/evidence/task-6-enemy-init.txt
  - [x] 敵人移動測試：.sisyphus/evidence/task-6-enemy-move.txt
  - [x] 敵人射擊測試：.sisyphus/evidence/task-6-enemy-shoot.txt

  **Commit**: YES
  - Message: `feat: 實現敵人坦克類別`
  - Files: `src/enemy.py`
  - Pre-commit: `uv run python -c "from src.enemy import EnemyTank; print('OK')"`

---

- [x] 7. 實現遊戲管理器類別

  **What to do**:
  - [x] 創建 `src/game.py` 文件
  - [x] 實現 Game 類別
  - [x] 實現遊戲狀態管理（開始、遊戲中、勝利、失敗）
  - [x] 實現計分系統（消滅敵人得分）
  - [x] 實現敵人生成邏輯（隨機生成 3-5 台敵人）
  - [x] 實現碰撞檢測系統（坦克與子彈、坦克與地圖）
  - [x] 實現勝利/失敗條件判斷
  - [x] 實現生命值顯示
  - [x] 實現分數顯示

  **Must NOT do**:
  - 不要實現過於複雜的遊戲邏輯

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: 遊戲管理器整合多個元件，邏輯相對複雜
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (依賴 Tasks 3, 4, 6)
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 3, 4, 6

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - `src/tank.py`: 玩家坦克類別實現
  - `src/enemy.py`: 敵人坦克類別實現
  - `src/bullet.py`: 子彈類別實現
  - `src/map.py`: 地圖類別實現

  **API/Type References** (contracts to implement against):
  - pygame.sprite.Group: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group - 精靈組管理
  - pygame.sprite.groupcollide: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.groupcollide - 精靈組碰撞檢測
  - pygame.font: https://www.pygame.org/docs/ref/font.html - 字體渲染（分數和生命值顯示）

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame sprite group 文檔: https://www.pygame.org/docs/ref/sprite.html
  - pygame font 文檔: https://www.pygame.org/docs/ref/font.html

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - pygame.sprite.Group: 管理所有遊戲物件（玩家、敵人、子彈）
  - pygame.sprite.groupcollide: 檢測不同精靈組之間的碰撞
  - pygame.font: 顯示遊戲資訊（分數、生命值）

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 遊戲可以正確初始化**
    Tool: Bash
    Preconditions: Game class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from game import Game
         import pygame
         pygame.init()
         game = Game()
         print(f"Game initialized")
         print(f"Player lives: {game.player_lives}")
         print(f"Score: {game.score}")
         print(f"Enemies: {len(game.enemies)}")
         pygame.quit()
         ```
      2. `uv run python test_game_init.py` → Assert output contains "Game initialized"
      3. Assert enemies count between 3 and 5
    Expected Result: 遊戲正確初始化，敵人數量在 3-5 台之間
    Evidence: Test output in .sisyphus/evidence/task-7-game-init.txt

  **Scenario: 碰撞檢測正常運作**
    Tool: Bash
    Preconditions: Game class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from game import Game
         import pygame
         pygame.init()
         game = Game()
         # Create a bullet that will hit an enemy
         from bullet import Bullet
         bullet = Bullet(x=game.player.rect.x, y=game.player.rect.y, direction=(1, 0), owner='player')
         enemy = list(game.enemies)[0]
         bullet.rect.center = enemy.rect.center
         initial_score = game.score
         game.check_collisions()
         print(f"Initial score: {initial_score}, Final score: {game.score}")
         print(f"Score increased: {game.score > initial_score}")
         pygame.quit()
         ```
      2. `uv run python test_game_collision.py` → Assert output contains "Score increased: True"
    Expected Result: 子彈擊中敵人後分數增加
    Evidence: Test output in .sisyphus/evidence/task-7-game-collision.txt

  **Scenario: 勝利條件正確判斷**
    Tool: Bash
    Preconditions: Game class implemented
    Steps:
      1. Create test script:
         ```python
         import sys
         sys.path.append('src')
         from game import Game
         import pygame
         pygame.init()
         game = Game()
         # Remove all enemies to simulate victory
         game.enemies.empty()
         game.check_game_over()
         print(f"Game over: {game.game_over}")
         print(f"Game won: {game.game_won}")
         pygame.quit()
         ```
      2. `uv run python test_game_victory.py` → Assert output contains "Game won: True"
    Expected Result: 所有敵人被消滅後判斷為勝利
    Evidence: Test output in .sisyphus/evidence/task-7-game-victory.txt

  **Evidence to Capture**:
  - [x] 遊戲初始化測試：.sisyphus/evidence/task-7-game-init.txt
  - [x] 碰撞檢測測試：.sisyphus/evidence/task-7-game-collision.txt
  - [x] 勝利條件測試：.sisyphus/evidence/task-7-game-victory.txt

  **Commit**: YES
  - Message: `feat: 實現遊戲管理器類別`
  - Files: `src/game.py`
  - Pre-commit: `uv run python -c "from src.game import Game; print('OK')"`

---

- [x] 8. 實現遊戲主循環

  **What to do**:
  - [x] 更新 `main.py` 文件
  - [x] 實現遊戲主循環（while True）
  - [x] 處理遊戲事件（鍵盤輸入、退出事件）
  - [x] 調用遊戲管理器的 update() 方法
  - [x] 繪製所有遊戲物件（地圖、玩家、敵人、子彈）
  - [x] 更新遊戲畫面（pygame.display.flip()）
  - [x] 控制遊戲幀率（pygame.time.Clock）

  **Must NOT do**:
  - 不要讓遊戲循環過於複雜

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: 主循環是遊戲的核心，需要確保正確實現
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (依賴 Task 7)
  - **Blocks**: Task 9
  - **Blocked By**: Task 7

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - `src/game.py`: 遊戲管理器類別實現

  **API/Type References** (contracts to implement against):
  - pygame.event.get(): https://www.pygame.org/docs/ref/event.html - 事件處理
  - pygame.time.Clock: https://www.pygame.org/docs/ref/time.html#pygame.time.Clock - 幀率控制
  - pygame.display.flip(): https://www.pygame.org/docs/ref/display.html - 更新顯示

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - pygame event 文檔: https://www.pygame.org/docs/ref/event.html
  - pygame time 文檔: https://www.pygame.org/docs/ref/time.html

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - pygame.event.get(): 處理玩家輸入和系統事件
  - pygame.time.Clock: 控制遊戲幀率（通常 60 FPS）
  - pygame.display.flip(): 更新遊戲畫面

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 遊戲可以正常啟動並運行**
    Tool: interactive_bash (tmux)
    Preconditions: Game loop implemented
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window to open (timeout: 5s)
      3. Take screenshot: `.sisyphus/evidence/task-8-game-start.png`
      4. Send "q" or ESC to quit the game
      5. Assert process exits with code 0
    Expected Result: 遊戲啟動，顯示遊戲畫面，可以正常退出
    Evidence: Game start screenshot .sisyphus/evidence/task-8-game-start.png

  **Scenario: 遊戲循環以 60 FPS 運行**
    Tool: Bash
    Preconditions: Game loop implemented
    Steps:
      1. Run `uv run python main.py` for 3 seconds
      2. Check CPU usage is reasonable (not 100% CPU)
      3. Take screenshot: `.sisyphus/evidence/task-8-game-fps.png`
      4. Terminate game
    Expected Result: 遊戲運行流暢，幀率穩定
    Evidence: Game FPS screenshot .sisyphus/evidence/task-8-game-fps.png

  **Evidence to Capture**:
  - [x] 遊戲啟動截圖：.sisyphus/evidence/task-8-game-start.png
  - [x] 遊戲 FPS 截圖：.sisyphus/evidence/task-8-game-fps.png

  **Commit**: YES
  - Message: `feat: 實現遊戲主循環`
  - Files: `main.py`
  - Pre-commit: `timeout 3s uv run python main.py || true`

---

- [x] 9. 整合所有元件

  **What to do**:
  - [x] 確保所有遊戲元件正確整合
  - [x] 測試玩家控制（上下左右移動、空格射擊）
  - [x] 測試敵人 AI 行為
  - [x] 測試碰撞檢測（子彈擊中坦克、坦克撞擊障礙物）
  - [x] 測試地圖系統（隨機生成、磚塊破壞）
  - [x] 測試勝利/失敗條件
  - [x] 優化遊戲性能（如有必要）

  **Must NOT do**:
  - 不要添加新功能
  - 不要過度優化（保持代碼清晰）

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: 整合測試需要全面檢查所有元件
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (依賴 Task 8)
  - **Blocks**: Task 10
  - **Blocked By**: Task 8

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - 所有先前實現的類別（tank.py, enemy.py, bullet.py, map.py, game.py）

  **API/Type References** (contracts to implement against):
  - (無新的 API 引用，整合現有元件)

  **Test References** (testing patterns to follow):
  - (無測試參考，因為使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - (無新的文檔參考)

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - (整合所有現有元件，確保正確運作)

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 玩家可以控制坦克移動和射擊**
    Tool: interactive_bash (tmux)
    Preconditions: Game integrated
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Send ArrowUp (3 times) → Assert tank moves up
      4. Screenshot: `.sisyphus/evidence/task-9-player-up.png`
      5. Send ArrowRight (3 times) → Assert tank moves right
      6. Screenshot: `.sisyphus/evidence/task-9-player-right.png`
      7. Send Space → Assert bullet appears
      8. Screenshot: `.sisyphus/evidence/task-9-player-shoot.png`
      9. Send "q" to quit
    Expected Result: 玩家坦克可以正確響應按鍵輸入
    Evidence: Player control screenshots (.sisyphus/evidence/task-9-player-*.png)

  **Scenario: 敵人 AI 正常運作**
    Tool: interactive_bash (tmux)
    Preconditions: Game integrated
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Wait 3 seconds (enemies should move)
      4. Screenshot: `.sisyphus/evidence/task-9-enemy-move.png`
      5. Wait 2 seconds (enemies may shoot)
      6. Screenshot: `.sisyphus/evidence/task-9-enemy-shoot.png`
      7. Send "q" to quit
    Expected Result: 敵人自動移動和射擊
    Evidence: Enemy AI screenshots (.sisyphus/evidence/task-9-enemy-*.png)

  **Scenario: 碰撞檢測正常運作**
    Tool: interactive_bash (tmux)
    Preconditions: Game integrated
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Player shoots bullet at enemy (Space + ArrowUp to aim)
      4. Wait for bullet to hit enemy
      5. Screenshot: `.sisyphus/evidence/task-9-collision-hit.png`
      6. Check if score increased
      7. Send "q" to quit
    Expected Result: 子彈擊中敵人後，敵人消失，分數增加
    Evidence: Collision screenshot .sisyphus/evidence/task-9-collision-hit.png

  **Scenario: 磚塊可以被破壞**
    Tool: interactive_bash (tmux)
    Preconditions: Game integrated
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Screenshot: `.sisyphus/evidence/task-9-brick-before.png`
      4. Player shoots at a brick
      5. Wait for bullet to hit brick
      6. Screenshot: `.sisyphus/evidence/task-9-brick-after.png`
      7. Assert brick disappeared
      8. Send "q" to quit
    Expected Result: 磚塊被子彈擊中後消失
    Evidence: Brick destruction screenshots (.sisyphus/evidence/task-9-brick-*.png)

  **Scenario: 勝利條件達成**
    Tool: interactive_bash (tmux)
    Preconditions: Game integrated
    Steps:
      1. Modify game to spawn only 1 enemy (for quick testing)
      2. Run `uv run python main.py`
      3. Wait for game window (timeout: 5s)
      4. Player shoots and destroys all enemies
      5. Wait for victory screen (timeout: 5s)
      6. Screenshot: `.sisyphus/evidence/task-9-victory.png`
      7. Assert "Victory" message displayed
    Expected Result: 消滅所有敵人後顯示勝利畫面
    Evidence: Victory screenshot .sisyphus/evidence/task-9-victory.png

  **Scenario: 失敗條件達成**
    Tool: interactive_bash (tmux)
    Preconditions: Game integrated
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Let player tank be hit by enemy bullets (don't move)
      4. Wait for all 3 lives to be lost (timeout: 30s)
      5. Screenshot: `.sisyphus/evidence/task-9-defeat.png`
      6. Assert "Game Over" message displayed
    Expected Result: 玩家生命歸零後顯示失敗畫面
    Evidence: Defeat screenshot .sisyphus/evidence/task-9-defeat.png

  **Evidence to Capture**:
  - [x] 玩家控制截圖：.sisyphus/evidence/task-9-player-*.png
  - [x] 敵人 AI 截圖：.sisyphus/evidence/task-9-enemy-*.png
  - [x] 碰撞檢測截圖：.sisyphus/evidence/task-9-collision-hit.png
  - [x] 磚塊破壞截圖：.sisyphus/evidence/task-9-brick-*.png
  - [x] 勝利截圖：.sisyphus/evidence/task-9-victory.png
  - [x] 失敗截圖：.sisyphus/evidence/task-9-defeat.png

  **Commit**: YES
  - Message: `refactor: 整合所有遊戲元件並修復問題`
  - Files: (所有必要的修改)
  - Pre-commit: `timeout 5s uv run python main.py || true`

---

- [x] 10. 完整 QA 驗證

  **What to do**:
  - [x] 執行完整的端到端測試
  - [x] 驗證所有遊戲功能正常運作
  - [x] 驗證遊戲性能良好（流暢運行）
  - [x] 生成最終截圖和證據
  - [x] 確認遊戲符合所有需求
  - [x] 檢查代碼品質（Clean Code、SOLID 原則）

  **Must NOT do**:
  - 不要修改遊戲邏輯（除非發現 Bug）
  - 不要添加新功能

  **Recommended Agent Profile**:
  > Select category + skills based on task domain. Justify each choice.
  - **Category**: `unspecified-high`
    - Reason: 完整 QA 需要全面檢查所有功能
  - **Skills**: [`python-expert`]
    - `python-expert`: 確保代碼遵循 Python 最佳實踐和 Clean Code 原則
  - **Skills Evaluated but Omitted**:
    - (無其他相關技能需要省略)

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (依賴 Task 9)
  - **Blocks**: None (final task)
  - **Blocked By**: Task 9

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - 所有先前實現的類別和遊戲邏輯

  **API/Type References** (contracts to implement against):
  - (無新的 API 引用，最終驗證)

  **Test References** (testing patterns to follow):
  - (無測試參考，使用 Agent-Executed QA)

  **Documentation References** (specs and requirements):
  - 原始需求文檔

  **External References** (libraries and frameworks):
  - pygame 官方文檔: https://www.pygame.org/docs/

  **WHY Each Reference Matters** (explain the relevance):
  - (最終驗證，確保遊戲符合所有需求)

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.
  > Every criterion MUST be verifiable by running a command or using a tool.
  > REPLACE all placeholders with actual values from task context.

  **Agent-Executed QA Scenarios (MANDATORY — per-scenario, ultra-detailed):**

  **Scenario: 完整遊戲流程 - 勝利**
    Tool: interactive_bash (tmux)
    Preconditions: All game features implemented
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Screenshot start screen: `.sisyphus/evidence/task-10-full-victory-01-start.png`
      4. Play game: ArrowUp/Down/Left/Right to move, Space to shoot
      5. Destroy all enemies (screenshot progress: `.sisyphus/evidence/task-10-full-victory-02-playing.png`)
      6. Wait for victory screen (timeout: 10s)
      7. Screenshot victory: `.sisyphus/evidence/task-10-full-victory-03-victory.png`
      8. Assert victory message displayed
      9. Send "q" to quit
    Expected Result: 完整的勝利遊戲流程正常運作
    Evidence: Full victory game flow screenshots (.sisyphus/evidence/task-10-full-victory-*.png)

  **Scenario: 完整遊戲流程 - 失敗**
    Tool: interactive_bash (tmux)
    Preconditions: All game features implemented
    Steps:
      1. Run `uv run python main.py`
      2. Wait for game window (timeout: 5s)
      3. Screenshot start screen: `.sisyphus/evidence/task-10-full-defeat-01-start.png`
      4. Don't move, let player be hit by enemy bullets
      5. Wait for all lives to be lost (screenshot progress: `.sisyphus/evidence/task-10-full-defeat-02-playing.png`)
      6. Wait for game over screen (timeout: 30s)
      7. Screenshot defeat: `.sisyphus/evidence/task-10-full-defeat-03-defeat.png`
      8. Assert "Game Over" message displayed
      9. Send "q" to quit
    Expected Result: 完整的失敗遊戲流程正常運作
    Evidence: Full defeat game flow screenshots (.sisyphus/evidence/task-10-full-defeat-*.png)

  **Scenario: 遊戲性能和穩定性測試**
    Tool: Bash
    Preconditions: All game features implemented
    Steps:
      1. Run `uv run python main.py` for 60 seconds
      2. Monitor CPU and memory usage
      3. Take periodic screenshots (every 20 seconds):
         - `.sisyphus/evidence/task-10-perf-01-20s.png`
         - `.sisyphus/evidence/task-10-perf-02-40s.png`
         - `.sisyphus/evidence/task-10-perf-03-60s.png`
      4. Assert game remains stable (no crashes, freezes)
      5. Assert frame rate remains consistent (~60 FPS)
      6. Terminate game
    Expected Result: 遊戲運行穩定，性能良好
    Evidence: Performance test screenshots (.sisyphus/evidence/task-10-perf-*.png)

  **Scenario: 代碼品質檢查**
    Tool: Bash
    Preconditions: All game code implemented
    Steps:
      1. Run `python -m py_compile src/*.py` → Assert no syntax errors
      2. Run `ruff check src/` → Check code style (if ruff available)
      3. Run `uv run python -c "import src.tank; import src.enemy; import src.bullet; import src.map; import src.game; print('All imports OK')"` → Assert all modules can be imported
      4. Generate code statistics:
         ```bash
         wc -l src/*.py > .sisyphus/evidence/task-10-code-stats.txt
         ```
    Expected Result: 代碼無語法錯誤，可正常匯入
    Evidence: Code statistics .sisyphus/evidence/task-10-code-stats.txt

  **Evidence to Capture**:
  - [x] 完整勝利流程截圖：.sisyphus/evidence/task-10-full-victory-*.png
  - [x] 完整失敗流程截圖：.sisyphus/evidence/task-10-full-defeat-*.png
  - [x] 性能測試截圖：.sisyphus/evidence/task-10-perf-*.png
  - [x] 代碼統計：.sisyphus/evidence/task-10-code-stats.txt

  **Commit**: YES
  - Message: `test: 完整 QA 驗證和最終優化`
  - Files: (所有必要的修改)
  - Pre-commit: `python -m py_compile src/*.py`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `feat: 建立專案結構和 uv 配置` | pyproject.toml, README.md, main.py | uv sync --dry-run |
| 2 | `chore: 安裝 pygame 依賴` | uv.lock | uv run python -c "import pygame" |
| 3 | `feat: 實現子彈類別` | src/bullet.py | uv run python -c "from src.bullet import Bullet" |
| 4 | `feat: 實現地圖類別` | src/map.py | uv run python -c "from src.map import Map" |
| 5 | `feat: 實現玩家坦克類別` | src/tank.py | uv run python -c "from src.tank import PlayerTank" |
| 6 | `feat: 實現敵人坦克類別` | src/enemy.py | uv run python -c "from src.enemy import EnemyTank" |
| 7 | `feat: 實現遊戲管理器類別` | src/game.py | uv run python -c "from src.game import Game" |
| 8 | `feat: 實現遊戲主循環` | main.py | timeout 3s uv run python main.py |
| 9 | `refactor: 整合所有遊戲元件並修復問題` | (所有修改) | timeout 5s uv run python main.py |
| 10 | `test: 完整 QA 驗證和最終優化` | (所有修改) | python -m py_compile src/*.py |

---

## Success Criteria

### Verification Commands
```bash
# 啟動遊戲
uv run python main.py
# 預期: 遊戲視窗開啟，顯示遊戲畫面

# 檢查代碼語法
python -m py_compile src/*.py
# 預期: 無錯誤

# 檢查依賴
uv pip list
# 預期: 包含 pygame
```

### Final Checklist
- [x] 遊戲可啟動（`uv run python main.py`）
- [x] 玩家可用方向鍵移動、空格鍵射擊
- [x] 敵人自動移動和射擊
- [x] 地圖隨機生成障礙物
- [x] 碰撞檢測正常運作
- [x] 勝利/失敗邏輯正確
- [x] 計分系統運作
- [x] 遊戲性能良好（60 FPS）
- [x] 代碼無語法錯誤
- [x] 所有 "Must Have" 功能已實現
- [x] 所有 "Must NOT Have" 功能未實現
