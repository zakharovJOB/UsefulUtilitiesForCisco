# UsefulUtilitiesForCisco
**First**

Этот скрипт предназначен для подключения к сетевому устройству Cisco, выполнения команд на нём и получения конфигурации интерфейса, к которому подключен определённый хост. Скрипт также записывает результаты и журнал выполнения в файлы.

Подробное описание работы скрипта:
Импорт библиотек:

netmiko: для подключения к сетевому устройству и выполнения команд.
re: для работы с регулярными выражениями, используемыми для извлечения данных из текстового вывода.
Задание параметров подключения:

device_params: словарь, содержащий параметры подключения к устройству:
device_type: тип устройства (cisco_ios).
host: имя или IP-адрес устройства (RU-KURGAN-DIST01).
username: имя пользователя (admin).
password: пароль (admin).
secret: enable пароль (enable_password).
IP-адрес хоста:

host_ip: IP-адрес хоста, для которого нужно найти MAC-адрес (8.8.8.8).
Функция process_device:

Основная функция, выполняющая все шаги по подключению и выполнению команд на устройстве.

Логи:

log: список для хранения сообщений лога, которые будут записаны в файл debug_log.txt.
Подключение к устройству:

Добавляет сообщение о подключении к устройству в лог.
Подключается к устройству с использованием параметров из device_params.
Переходит в режим enable.
Добавляет сообщение об успешном подключении в лог.
Шаг 1: Получение MAC-адреса:

Выполняет команду show ip arp {host_ip} для получения MAC-адреса по IP-адресу.
Добавляет результат команды в лог.
Извлекает MAC-адрес с помощью регулярного выражения r'(\w{4}\.\w{4}\.\w{4})'.
Если MAC-адрес найден, добавляет его в лог, иначе выбрасывает ошибку.
Шаг 2: Поиск интерфейса по MAC-адресу:

Выполняет команду show mac address-table | include {mac_address} для поиска интерфейса по MAC-адресу.
Добавляет результат команды в лог.
Разделяет вывод команды на строки и ищет строку, содержащую MAC-адрес.
Извлекает интерфейс с помощью регулярного выражения r'(Gi.+|GigabitEthernet.+|Fa.+|FastEthernet.+|Ethernet.+|Eth.+|Po.+)'.
Если интерфейс найден, добавляет его в лог, иначе выбрасывает ошибку.
Шаг 3: Получение полной конфигурации интерфейса:

Выполняет команду show run interface {interface} для получения конфигурации интерфейса.
Добавляет результат команды в лог.
Завершение работы:

Закрывает соединение.
Добавляет сообщение о закрытии соединения в лог.
Возвращает результат и лог.
Опрос устройства и сохранение результата в файл:

Вызывает функцию process_device и сохраняет результат в файл output.txt.
Сохраняет лог в файл debug_log.txt.
Вывод сообщения о завершении:

Выводит сообщение о завершении опроса и сохранении логов.
Возможные проблемы и их решение:
Если MAC-адрес или интерфейс не найден, скрипт выбрасывает ошибку и записывает её в лог.
Логирование промежуточных результатов помогает в отладке и выявлении проблем на каждом этапе работы.
Этот скрипт должен корректно обрабатывать различные форматы интерфейсов, такие как Gi1/0/16, GigabitEthernet3/48, Fa0/1, FastEthernet0/1, Ethernet1, Eth2, Po1, и записывать соответствующие логи для упрощения отладки.

Second
Этот скрипт предназначен для подключения к сетевому устройству Cisco, поиска интерфейса по заданному MAC-адресу и записи результатов в файл. Скрипт также записывает журналы выполнения для отладки.

Подробное описание работы скрипта:
Импорт библиотек:

netmiko: для подключения к сетевому устройству и выполнения команд.
re: для работы с регулярными выражениями, используемыми для извлечения данных из текстового вывода.
Задание параметров подключения:

device_params: словарь, содержащий параметры подключения к устройству:
device_type: тип устройства (cisco_ios).
host: имя или IP-адрес устройства (RU-KURGAN-SW1).
username: имя пользователя (admin).
password: пароль (admin).
secret: enable пароль (enable_password).
MAC-адрес:

mac_address: MAC-адрес, для которого нужно найти интерфейс (01190.e815.a911).
Функция find_interface_by_mac:

Основная функция, выполняющая все шаги по подключению и выполнению команды на устройстве.

Логи:

log: список для хранения сообщений лога, которые будут записаны в файл debug_log_mac.txt.
Подключение к устройству:

Добавляет сообщение о подключении к устройству в лог.
Подключается к устройству с использованием параметров из device_params.
Переходит в режим enable.
Добавляет сообщение об успешном подключении в лог.
Поиск интерфейса по MAC-адресу:

Выполняет команду show mac address-table | include {mac_address} для поиска интерфейса по MAC-адресу.

Добавляет результат команды в лог.

Извлечение интерфейса:

Извлекает интерфейс из вывода команды с помощью регулярного выражения r'(\S+)$'.
Если интерфейс найден, добавляет его в лог, иначе выбрасывает ошибку.
Завершение работы:

Закрывает соединение.
Добавляет сообщение о закрытии соединения в лог.
Возвращает результат и лог.
Поиск интерфейса по MAC-адресу и сохранение результата в файл:

Вызывает функцию find_interface_by_mac и сохраняет результат в файл interface_output.txt.
Сохраняет лог в файл debug_log_mac.txt.
Вывод сообщения о завершении:

Выводит сообщение о завершении поиска и сохранении логов.
Возможные проблемы и их решение:
Если интерфейс не найден, скрипт выбрасывает ошибку и записывает её в лог.
Логирование промежуточных результатов помогает в отладке и выявлении проблем на каждом этапе работы.
Этот скрипт поможет вам найти интерфейс, к которому подключен определённый MAC-адрес, и сохранить эту информацию вместе с журналами выполнения команд для дальнейшего анализа.


