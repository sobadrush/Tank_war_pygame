# 坦克大戰

經典街機遊戲「坦克大戰」的 Python 實現版本。使用 `pygame` 開發，支援單人遊玩。

## 功能特性

- 🎮 經典坦克遊戲玩法
- 🏮 像素風格圖形
- ⌨️ 支援鍵盤控制
- 🎯 敵人 AI 和關卡系統
- 💾 遊戲進度保存

## 系統需求

- **Python** 版本：3.9 或以上
- **作業系統**：macOS / Linux / Windows
- **主要依賴**：pygame 2.1.0+

## 安裝方式

### 使用 uv（推薦）

首先確保已安裝 [uv](https://docs.astral.sh/uv/)，然後：

```bash
# 進入專案目錄
cd tank-war

# 安裝依賴並建立虛擬環境
uv sync

# 創建虛擬環境（如需要）
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

### 手動安裝

```bash
# 建立虛擬環境
python3.9 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows

# 安裝依賴
pip install pygame>=2.1.0
```

## 運行方式

### 使用 uv 運行

```bash
# 直接運行
uv run python main.py

# 或在虛擬環境中運行
source .venv/bin/activate
python main.py
```

### 直接運行

```bash
python main.py
```

## 遊戲控制

| 按鍵 | 功能 |
|------|------|
| `↑` / `W` | 向上移動 |
| `↓` / `S` | 向下移動 |
| `←` / `A` | 向左移動 |
| `→` / `D` | 向右移動 |
| `Space` | 射擊 |
| `ESC` | 暫停/返回主選單 |
| `Q` | 結束遊戲 |
| `R` | 遊戲結束/勝利後重新開始 |

## 專案結構

```
tank-war/
├── src/                    # 原始碼目錄
│   └── __init__.py        # 套件初始化
├── .sisyphus/             # Sisyphus 任務管理
│   └── evidence/          # 任務執行證據
├── pyproject.toml         # uv 專案配置
├── main.py                # 遊戲主程式入口
└── README.md              # 本說明文件
```

## 開發

### 建立開發環境

```bash
# 使用 uv 安裝開發依賴
uv sync --dev

# 或手動安裝
pip install -e ".[dev]"
```

### 執行測試

```bash
uv run pytest tests/
```

### 代碼格式檢查

```bash
# 使用 black 格式化
uv run black src/ main.py

# 使用 isort 排序 import
uv run isort src/ main.py

# 使用 mypy 檢查類型
uv run mypy src/ main.py
```

## 貢獻指南

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -am 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

## 授權

本專案採用 MIT 授權。詳見 [LICENSE](LICENSE) 檔案。

## 聯絡方式

有任何問題或建議，歡迎通過 GitHub Issues 聯絡。

## 素材下載
- [素材下載連結](https://www.bilibili.com/read/cv24103936/?opus_fallback=1)

---

**祝你遊戲愉快！** 🎮✨
