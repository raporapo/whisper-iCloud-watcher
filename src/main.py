from pathlib import Path
import yaml
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from transcriber import Transcriber


# loading
def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r' ,encoding='utf-8') as f:
        return yaml.safe_load(f)
    
class VoiceMemoHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.transcriber = Transcriber(config)
        self.processing = set() #処理中に重複防止
    
    def on_created(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)
        if path.suffix.lower() not in [".m4a", ".wav", ".mp3"]:
            return
        if str(path) in self.processing:
            return

        self.processing.add(str(path))
        self._handle(path)
        self.processing.discard(str(path))

    def _handle(self, path):
        print(f"検知: {path.name}")
        self._wait_stable(path)
        text = self.transcriber.run(path)
        if text:
            self.notifier.send(path.name, text)

    def _wait_stable(self, path, interval=6, retries=10):
        prev_size = -1
        for _ in range(retries):
            try:
                current_size = path.stat().st_size
                if current_size == prev_size and current_size > 0:
                    return
                prev_size = current_size
            except FileNotFoundError:
                pass
            time.sleep(interval)

if __name__ == "__main__":
    config = load_config()
    watch_dir = Path(config["watch_dir"]).expanduser()

    handler = VoiceMemoHandler(config)
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=False)
    observer.start()

    print(f"監視中: {watch_dir}")
    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()