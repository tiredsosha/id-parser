# ID Parser

Простой mqtt клиент для парсинга ID парка

## Зависимости

Python 3.8  
asyncio-mqtt 0.11.0  
pydantic 1.8.2  
PyYAML 6.0

## Установка
- Скопировать репозиторий в корневую директорию(!!!) ubuntu   
- Из папки репозитория запустить установщик командой
```bash
sudo su
bash install.sh user
```
Где user - это имя юзера, которые вы устанавливали при установки ubuntu

## Настройка
В файле config.yaml содержится инфа о mqtt сервер, развернутом в парке  
Пример файла:
```yaml
host: localhost
username: admin
password: computer
id: id
```
Где host - это ip mqtt сервера (если развернуто на компе с админкой, то можно оставить localhost), username - логин для mqtt, password - пароль для mqtt, id - ID парка  
Все параметры обязательные  
После изменения параметров в конфиге нужно обязательно перезагрузить комп админки!

## Использование
Клиент шлет id каждые 5 секунд в топик /park/id/status  
Так же клиент слушает топик /park/id/command, если на него приходит сообщение, то он перезаписывает id в файле и шлет новый
