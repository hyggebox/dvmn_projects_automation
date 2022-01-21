# dvmn_projects_automation
Сервис ProjectsAutomation

___________________
## Переменные окружения
Определите переменные окружения в файле `.env` в формате: `ПЕРЕМЕННАЯ=значение`:
- `TELEGRAM_TOKEN` — токен телеграм-бота
- `DEBUG` — дебаг-режим. Поставьте `True` для включения, `False` -- для 
выключения отладочного режима. По умолчанию дебаг-режим отключен.
- `SECRET_KEY` — секретный ключ проекта.
- `DATABASE_URL` - URL базы данных
- `HEROKU_APP_NAME` - название приложения в Heroku

Запуск бота : 
```commandline
python manage.py bot
```
команда прописана в Procfile, но для запуска в heroku нужно вручную включить второй dynos

Загрузка json происходит из папки media приложения командой

```commandline
python manage.py import_from_json
```