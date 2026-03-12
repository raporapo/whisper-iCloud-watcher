@echo off
echo === Whisper iCloud Watcher セットアップ ===

:: Pythonバージョン確認
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pythonが見つかりません。https://python.org からインストールしてください
    pause
    exit /b 1
)

:: 仮想環境を作成
python -m venv .venv
call .venv\Scripts\activate

:: GPU確認してインストール分岐
python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GPU検出 → GPU版をインストールします
    pip install -r requirements-gpu.txt
) else (
    echo ℹ️ GPU未検出 → CPU版をインストールします
    pip install -r requirements.txt
)

:: config.yamlがなければテンプレートをコピー
if not exist config.yaml (
    copy config.example.yaml config.yaml
    echo 📝 config.yaml を作成しました。内容を編集してください
)

:: 監視フォルダを作成
if not exist "%USERPROFILE%\Desktop\whisper-input" (
    mkdir "%USERPROFILE%\Desktop\whisper-input"
)

echo.
echo ✅ セットアップ完了！
echo ① config.yaml を編集してください
echo ② 起動: .venv\Scripts\activate して python src/main.py
pause