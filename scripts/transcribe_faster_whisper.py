#!/usr/bin/env python3
"""
OpenClaw Telegram Voice Transcription Script
Локальное распознавание голосовых сообщений через Faster Whisper
"""

import os
import sys
from faster_whisper import WhisperModel

def main():
    if len(sys.argv) < 2:
        print("usage: transcribe_faster_whisper.py <audio_path>", file=sys.stderr)
        return 2

    audio_path = sys.argv[1]
    model_name = os.environ.get("OPENCLAW_WHISPER_MODEL", "small")
    device = os.environ.get("OPENCLAW_WHISPER_DEVICE", "cpu")
    compute_type = os.environ.get("OPENCLAW_WHISPER_COMPUTE", "int8")
    language = os.environ.get("OPENCLAW_WHISPER_LANG", "ru") or None

    print(f"🔧 Параметры: model={model_name}, device={device}, lang={language}", file=sys.stderr)
    print(f"📁 Обрабатываю: {os.path.basename(audio_path)}", file=sys.stderr)
    
    try:
        model = WhisperModel(model_name, device=device, compute_type=compute_type)
        print("✅ Модель загружена", file=sys.stderr)
        
        segments, info = model.transcribe(
            audio_path,
            language=language,
            vad_filter=True,
            beam_size=5,
        )
        
        text = " ".join((seg.text or "").strip() for seg in segments).strip()
        
        if text:
            print(f"✅ Распознано: {text}", file=sys.stderr)
        else:
            print("📭 Текст не распознан", file=sys.stderr)
        
        print(text)
        return 0
        
    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
