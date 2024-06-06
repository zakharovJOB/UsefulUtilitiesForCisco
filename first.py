from netmiko import ConnectHandler
import re

# Параметры подключения к устройству
device_params = {
    'device_type': 'cisco_ios',  # Тип устройства, например, cisco_ios, juniper, etc.
    'host': 'RU-KURGAN-DIST01',       # IP-адрес устройства
    'username': 'admin',         # Имя пользователя
    'password': 'admin',      # Пароль
    'secret': 'enable_password', # Enable пароль, если требуется
}

# IP-адрес хоста, для которого ищем MAC-адрес
host_ip = '8.8.8.8'


def process_device(device_params, host_ip):
    log = []

    try:
        log.append(f"Подключение к устройству {device_params['host']}...")
        connection = ConnectHandler(**device_params)
        connection.enable()
        log.append("Успешное подключение.")

        # Шаг 1: Получение MAC-адреса
        arp_command = f'show ip arp {host_ip}'
        arp_output = connection.send_command(arp_command)
        log.append(f"Результат команды '{arp_command}':\n{arp_output}")
        
        # Извлечение MAC-адреса из вывода команды
        mac_address_match = re.search(r'(\w{4}\.\w{4}\.\w{4})', arp_output)
        if mac_address_match:
            mac_address = mac_address_match.group(1)
            log.append(f"Найден MAC-адрес: {mac_address}")
        else:
            raise ValueError("MAC-адрес не найден")

        # Шаг 2: Поиск интерфейса по MAC-адресу
        mac_command = f'show mac address-table | include {mac_address}'
        mac_output = connection.send_command(mac_command)
        log.append(f"Результат команды '{mac_command}':\n{mac_output}")

        # Убедимся, что mac_output содержит нужную строку
        lines = mac_output.splitlines()
        interface = None
        for line in lines:
            if mac_address in line:
                # Попробуем извлечь интерфейс из строки
                interface_match = re.search(r'(Gi.+|GigabitEthernet.+|Fa.+|FastEthernet.+|Ethernet.+|Eth.+|Po.+)', line)
                if interface_match:
                    interface = interface_match.group(0)
                    log.append(f"Найден интерфейс: {interface}")
                    break

        if not interface:
            raise ValueError("Интерфейс не найден")

        # Шаг 3: Получение полной конфигурации интерфейса
        interface_command = f'show run interface {interface}'
        interface_output = connection.send_command(interface_command)
        log.append(f"Результат команды '{interface_command}':\n{interface_output}")
        
        connection.disconnect()
        log.append("Соединение закрыто.")

        return f"Устройство: {device_params['host']}\nMAC-адрес: {mac_address}\nИнтерфейс: {interface}\nКонфигурация интерфейса:\n{interface_output}\n\n", log
    except Exception as e:
        log.append(f"Ошибка: {e}")
        return f"Ошибка при обработке устройства {device_params['host']}: {e}\n\n", log

# Опрос устройства и сохранение результата в файл
result, log = process_device(device_params, host_ip)

with open('output.txt', 'w') as output_file:
    output_file.write(result)

with open('debug_log.txt', 'w') as log_file:
    for entry in log:
        log_file.write(entry + '\n')

print("Опрос устройства завершен. Логи сохранены в debug_log.txt")