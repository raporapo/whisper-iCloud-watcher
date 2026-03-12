import whisper
import torch
from pathlib import Path

class Transcriber:
    def __init__(self, config):
        model_size = config.get("model_size", "medium")
        self.output_dir = Path(config.get("output_dir", "~/Desktop/transcripts")).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # ① GPU自動検知
        if torch.cuda.is_available():
            self.device = "cuda"
            print(f"GPU使用: {torch.cuda.get_device_name(0)}")
        else:
            self.device = "cpu"
            print("CPU使用")
            # CPUのときはlargeを自動でmediumに落とす
            if "large" in model_size:
                print(f"⚠️ large → medium に自動変更（CPU環境）")
                model_size = "medium"

        print(f"モデル読み込み中: {model_size} ...")
        self.model = whisper.load_model(model_size, device=self.device)
        print("モデル準備完了")

    # ② 文字起こし実行
    def run(self, audio_path: Path) -> str | None:
        output_path = self.output_dir / f"{audio_path.stem}.txt"

        if output_path.exists():
            print(f"スキップ（処理済み）: {audio_path.name}")
            return None

        print(f"文字起こし開始: {audio_path.name}")
        try:
            result = self.model.transcribe(
                str(audio_path),
                language="ja",
                verbose=False
            )
            text = result["text"]
            output_path.write_text(text, encoding="utf-8")
            print(f"完了 → {output_path.name}")
            return text

        except Exception as e:
            print(f"エラー: {e}")
            return None