# 📖 Установка и настройка

## Полное руководство по установке

### 1. Предварительные требования

#### Системные требования
- **ОС:** Ubuntu 20.04+, Debian 11+, или любая Linux с поддержкой Python 3.8+
- **Память:** Минимум 2GB RAM (рекомендуется 4GB+)
- **Диск:** 2GB свободного места
- **Процессор:** Любой современный CPU

#### Установленные компоненты
- **OpenClaw** (уже должен быть установлен)
- **Python 3.8+**
- **ffmpeg**
- **Git** (для клонирования репозитория)

### 2. Установка зависимостей

#### Ubuntu/Debian
```bash
# Обновление системы
sudo apt-get update
sudo apt-get upgrade -y

# Установка ffmpeg
sudo apt-get install -y ffmpeg

# Установка Python и pip
sudo apt-get install -y python3 python3-pip python3-venv

# Установка faster-whisper
pip3 install faster-whisper

# Альтернативно через venv (рекомендуется)
python3 -m venv ~/.openclaw-whisper-venv
source ~/.openclaw-whisper-venv/bin/activate
pip install faster-whisper
```

#### CentOS/RHEL
```bash
# Установка EPEL репозитория
sudo yum install -y epel-release

# Установка зависимостей
sudo yum install -y ffmpeg python3 python3-pip

# Установка faster-whisper
pip3 install faster-whisper
```

### 3. Настройка OpenClaw

#### Клонирование репозитория
```bash
# Создание директории для скриптов
mkdir -p ~/.openclaw/workspace/scripts

# Копирование скрипта транскрипции
cp scripts/transcribe_faster_whisper.py ~/.openclaw/workspace/scripts/

# Даем права на выполнение
chmod +x ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py
```

#### Настройка конфигурации OpenClaw

##### Вариант A: Добавление в существующий конфиг
Откройте файл `~/.openclaw/config.json` и добавьте блок `tools.media.audio`:

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

##### Вариант B: Создание нового конфига
Если у вас нет конфига, создайте его:

```bash
cat > ~/.openclaw/config.json << 'CONFIG'
{
  "$schema": "https://docs.openclaw.ai/schemas/config/v1.json",
  "version": "1.0",
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
              "{{UserHome}}/.openclaw/workspace/scripts/transcribe_f
er_whisper.py",
              "{{MediaPath}}"
            ],
            "timeoutSeconds": 180
          }
        ]
      }
    }
  }
}
CONFIG
```

### 4. Перезапуск OpenClaw Gateway

```bash
# Перезапуск службы
systemctl --user restart openclaw-gateway.service

# Проверка статуса
systemctl --user status openclaw-gateway.service

# Просмотр логов
journalctl --user -u openclaw-gateway.service -f
```

### 5. Настройка Telegram бота

#### Создание бота
1. Откройте Telegram и найдите `@BotFather`
2. Отправьте `/newbot` и следуйте инструкциям
3. Сохраните полученный токен

#### Настройка OpenClaw для Telegram
```bash
# Добавление Telegram канала
openclaw channels add telegram --token YOUR_BOT_TOKEN
```

### 6. Тестирование системы

#### Тест 1: Проверка зависимостей
```bash
# Проверка ffmpeg
ffmpeg -version

# Проверка faster-whisper
python3 -c "from faster_whisper import WhisperModel; print('✅ faster-whisper установлен')"

# Тест скрипта
python3 ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py --help
```

#### Тест 2: Тестовое аудио
```bash
# Создание тестового аудио
echo "Тест распознавания речи" | espeak -v ru --stdout | ffmpeg -i pipe:0 test.wav

# Тест транскрипции
python3 ~/.openclaw/workspace/scripts/transcribe_faster_whisper.py test.wav
```

#### Тест 3: Полный цикл
1. Отправьте голосовое сообщение боту в Telegram
2. Проверьте логи OpenClaw
3. Убедитесь, что текст появился в диалоге

### 7. Оптимизация производительности

#### Настройка переменных окружения
```bash
# В файле ~/.bashrc или ~/.profile
export OPENCLAW_WHISPER_MODEL="small"
export OPENCLAW_WHISPER_DEVICE="cpu"
export OPENCLAW_WHISPER_COMPUTE="int8"
export OPENCLAW_WHISPER_LANG="ru"
```

#### Оптимизация для слабых серверов
```bash
# Использование tiny модели
export OPENCLAW_WHISPER_MODEL="tiny"

# Уменьшение использования памяти
export OPENCLAW_WHISPER_COMPUTE="int8"
```

### 8. Мониторинг и логирование

#### Логи транскрипции
```bash
# Просмотр логов транскрипции
tail -f /tmp/openclaw-whisper.log

# Мониторинг использования памяти
htop

# Проверка дискового пространства
df -h
```

### 9. Обновление системы

#### Обновление faster-whisper
```bash
pip3 install --upgrade faster-whisper
```

#### Обновление скриптов
```bash
cd ~/.openclaw/workspace/github_projects/openclaw-telegram-voice-transcription
git pull origin main
cp scripts/transcribe_faster_whisper.py ~/.openclaw/workspace/scripts/
```

### 10. Устранение неполадок

#### Проблема: "ModuleNotFoundError: No module named 'faster_whisper'"
**Решение:**
```bash
pip3 install faster-whisper
# или
python3 -m pip install faster-whisper
```

#### Проблема: "ffmpeg: command not found"
**Решение:**
```bash
sudo apt-get install ffmpeg
```

#### Проблема: Telegram не отправляет аудио
**Решение:**
1. Проверьте настройки Telegram (экономия трафика)
2. Обновите Telegram до последней версии
3. Проверьте разрешения на микрофон

### 11. Дополнительные ресурсы

- [Документация OpenClaw](https://docs.openclaw.ai)
- [Документация Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**🎉 Поздравляем! Система настроена и готова к работе!**
