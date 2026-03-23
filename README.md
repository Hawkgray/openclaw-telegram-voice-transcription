# 🎤 OpenClaw Telegram Voice Transcription

**Локальное распознавание голосовых сообщений Telegram с помощью Faster Whisper**

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Enabled-green)](https://openclaw.ai)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)](https://telegram.org)
[![Faster Whisper](https://img.shields.io/badge/Faster%20Whisper-Local-orange)](https://github.com/SYSTRAN/faster-whisper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Возможности

- **Локальное распознавание речи** без внешних API
- **Интеграция с OpenClaw** для автоматической транскрипции
- **Поддержка Telegram голосовых сообщений** (OGG/Opus)
- **Мультиязычность** (русский, английский и другие)
- **Высокая скорость** благодаря Faster Whisper
- **Конфигурируемые модели** (tiny, base, small, medium, large)

## 📋 Требования

- **OpenClaw** установленный и настроенный
- **Python 3.8+** с пакетами:
  - `faster-whisper`
  - `ffmpeg`
- **Telegram Bot** с токеном

## ⚡ Быстрый старт

### 1. Установка зависимостей
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg python3-pip
pip3 install faster-whisper
```

### 2. Создание скрипта транскрипции
```bash
mkdir -p ~/.openclaw/workspace/scripts
cat > ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py << 'SCRIPT'
#!/usr/bin/env python3
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

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        audio_path,
        language=language,
        vad_filter=True,
        beam_size=5,
    )
    text = " ".join((seg.text or "").strip() for seg in segments).strip()
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
SCRIPT

chmod +x ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py
```

### 3. Настройка OpenClaw
Добавьте в конфиг OpenClaw (`~/.openclaw/config.json`):

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "language": "ru",
        "echoTranscript": true,
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
```

### 4. Перезапуск OpenClaw Gateway
```bash
systemctl --user restart openclaw-gateway.service
```

## 🎯 Использование

1. **Отправьте голосовое сообщение** в Telegram боту
2. **OpenClaw автоматически транскрибирует** аудио
3. **Текст появится в диалоге** как `📝 {transcript}`
4. **Ассистент ответит** на основе распознанного текста

## ⚙️ Конфигурация

### Модели Whisper
```bash
# Для слабого сервера (быстрее, но хуже качество)
export OPENCLAW_WHISPER_MODEL=tiny

# Для нормального сервера (баланс скорости/качества)
export OPENCLAW_WHISPER_MODEL=small

# Для мощного сервера (лучшее качество)
export OPENCLAW_WHISPER_MODEL=medium
```

### Язык распознавания
```bash
# Русский (по умолчанию)
export OPENCLAW_WHISPER_LANG=ru

# Английский
export OPENCLAW_WHISPER_LANG=en

# Автоопределение
unset OPENCLAW_WHISPER_LANG
```

## 📊 Производительность

| Модель | Скорость | Память | Качество | Рекомендация |
|--------|----------|--------|----------|--------------|
| tiny   | ⚡⚡⚡⚡⚡ | 1GB    | ⭐⭐      | Тестирование |
| base   | ⚡⚡⚡⚡   | 1.5GB  | ⭐⭐⭐     | Базовая      |
| small  | ⚡⚡⚡     | 2GB    | ⭐⭐⭐⭐    | Производство |
| medium | ⚡⚡      | 5GB    | ⭐⭐⭐⭐⭐   | Качество     |
| large  | ⚡        | 10GB   | ⭐⭐⭐⭐⭐⭐  | Максимальное |

## 🐛 Диагностика

### Проверка зависимостей
```bash
# Проверка ffmpeg
which ffmpeg
ffmpeg -version

# Проверка faster-whisper
python3 -c "from faster_whisper import WhisperModel; print('✅ faster-whisper установлен')"

# Тест скрипта
python3 ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py /path/to/audio.ogg
```

### Логирование
```bash
# Просмотр логов OpenClaw
journalctl --user -u openclaw-gateway.service -f

# Логи транскрипции
tail -f /tmp/openclaw-whisper.log
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 🙏 Благодарности

- [OpenClaw](https://openclaw.ai) - за потрясающую платформу
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) - за быструю реализацию Whisper
- [Telegram](https://telegram.org) - за отличный мессенджер

## 📞 Контакты

**Elnur Aliev** - [@alievbro](https://t.me/alievbro)

**GitHub:** [alievbro](https://github.com/alievbro)

---

⭐ **Если этот проект был полезен, поставьте звезду на GitHub!**
