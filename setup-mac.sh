#!/bin/bash

echo "=== Whisper iCloud Watcher セットアップ ==="

# Pythonバージョン確認
python3 --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Python3が見つかりません。https://python.org からインストールしてください"
    exit 1
fi

# 仮想環境を作成
python3 -m venv .venv
source .venv/bin/activate

# GPU確認してインストール分岐
if python3 -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
    echo "✅ GPU検出 → GPU版をインストールします"
    pip install -r requirements-gpu.txt
else
    echo "ℹ️ GPU未検出 → CPU版をインストールします"
    pip install -r requirements.txt
fi

# config.yamlがなければテンプレートをコピー
if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "📝 config.yaml を作成しました。内容を編集してください"
fi

# 監視フォルダを作成
mkdir -p ~/Desktop/whisper-input

echo ""
echo "✅ セットアップ完了！"
echo "① config.yaml を編集してください"
echo "② 起動: source .venv/bin/activate && python src/main.py"