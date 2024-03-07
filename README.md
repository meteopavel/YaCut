# Проект YaCut
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Основные используемые инструменты
* Python        3.11.5
* Flask-Migrate 3.1.0
* Flask-WTF     1.0.0
* SQLAlchemy    1.4.29
* python-dotenv 0.19.2

## Развёртывание проекта на локальном компьютере
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:meteopavel/yacut.git
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
linux: source env/bin/activate
windows: source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Использование
```python
flask db upgrade
flask run
```
Команда запустит сервер flask. После этого ресурс станет доступен по
адресу http://127.0.0.1:5000. Сервис можно использовать как через 
браузер, так и через API:

### /api/id/ — POST-запрос на создание новой короткой ссылки;
Пример запроса:
```json
{
  "url": "string",
  "custom_id": "string"
}
```
Поле "custom_id" является опциональным. При его отсутствии, или если оно будет пустым, короткая ссылка будет сгенерирована автоматически.
Ожидаемый ответ:
```json
{
  "url": "string",
  "short_link": "string"
}
```
### /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.
Ожидаемый ответ:
```json
{
  "url": "string"
}
```
Полная документация доступна в файле openapi.yml

## Автор
[Павел Найденов](https://github.com/meteopavel)