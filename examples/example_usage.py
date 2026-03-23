#!/usr/bin/env python3
"""
Пример использования OpenClaw Telegram Voice Transcription
"""

import os
import json
from pathlib import Path

def print_example_config():
    """Пример конфигурации OpenClaw"""
    config = {
        "tools": {
            "media": {
                "audio": {
                    "enabled": True,
                    "language": "ru",
                    "echoTranscript": True,
                    "echoFormat": "📝 {transcript}",
                    "models": [
                        {
                            "type": "cli",
                            "command": "python3",
                            "args": [
                                "{{UserHome}}/.openclaw/workspace/scripts/transcribe_faster_whisper.py",
                                "{{MediaPath}}"
                            ],
                            "timeoutSeconds": 180
                        }
                    ]
                }
            }
        }
    }
    
    print("📋 Пример конфигурации OpenClaw:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print()

def print_environment_variables():
    """Переменные окружения для настройки"""
    env_vars = {
        "OPENCLAW_WHISPER_MODEL": "small",
        "OPENCLAW_WHISPER_DEVICE": "cpu",
        "OPENCLAW_WHISPER_COMPUTE": "int8",
        "OPENCLAW_WHISPER_LANG": "ru"
    }
    
    print("🌍 Переменные окружения:")
    for key, value in env_vars.items():
        print(f"export {key}=\"{value}\"")
    print()

def print_test_commands():
    """Команды для тестирования"""
    commands = [
        "# Проверка зависимостей",
        "ffmpeg -version",
        "python3 -c \"from faster_whisper import WhisperModel; print('✅ faster-whisper установлен')\"",
        "",
        "# Тест скрипта",
        "python3 ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py --help",
        "",
        "# Создание тестового аудио",
        "echo 'Тест распознавания речи' | espeak -v ru --stdout | ffmpeg -i pipe:0 test.wav",
        "",
        "# Тест транскрипции",
        "python3 ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py test.wav",
        "",
        "# Перезапуск OpenClaw",
        "systemctl --user restart openclaw-gateway.service",
        "",
        "# Просмотр логов",
        "journalctl --user -u openclaw-gateway.service -f"
    ]
    
    print("🧪 Команды для тестирования:")
    for cmd in commands:
        if cmd.startswith("#"):
            print(f"\n{cmd}")
        elif cmd:
            print(f"$ {cmd}")
    print()

def main():
    print("=" * 60)
    print("🎤 OpenClaw Telegram Voice Transcription - Примеры использования")
    print("=" * 60)
    print()
    
    print_example_config()
    print_environment_variables()
    print_test_commands()
    
    print("=" * 60)
    print("📚 Дополнительные ресурсы:")
    print("- Документация: docs/INSTALLATION.md")
    print("- Скрипты: scripts/")
    print("- Конфигурации: configs/")
    print("=" * 60)

if __name__ == "__main__":
    main()
