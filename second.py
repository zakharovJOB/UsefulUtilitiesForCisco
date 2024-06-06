from netmiko import ConnectHandler
import re

# Параметры подключения к устройству
device_params = {
    'device_type': 'cisco_ios',  # Тип устройства, например, cisco_ios, juniper, etc.
    'host': 'RU-KURGAN-SW1',       # IP-адрес устройства или доменное имя
    'username': 'admin',         # Имя пользователя
    'password': 'admin',      # Пароль
    'secret': 'enable_password', # Enable пароль, если требуется
}

# MAC-адрес, для которого ищем интерфейс
mac_address = '01190.e815.a911'



def find_interface_by_mac(device_params, mac_address):
    log = []

    try:
        log.append(f"Подключение к устройству {device_params['host']}...")
        connection = ConnectHandler(**device_params)
        connection.enable()
        log.append("Успешное подключение.")

        # Поиск интерфейса по MAC-адресу
        mac_command = f'show mac address-table | include {mac_address}'
        mac_output = connection.send_command(mac_command)
        log.append(f"Результат команды '{mac_command}':\n{mac_output}")

        # Извлечение интерфейса из вывода команды
        interface_match = re.search(r'(\S+)$', mac_output)
        if interface_match:
            interface = interface_match.group(1)
            log.append(f"Найден интерфейс: {interface}")
        else:
            raise ValueError("Интерфейс не найден")
        
        connection.disconnect()
        log.append("Соединение закрыто.")

        return f"MAC-адрес: {mac_address}\nИнтерфейс: {interface}\n\n", log
    except Exception as e:
        log.append(f"Ошибка: {e}")
        return f"Ошибка при обработке устройства {device_params['host']}: {e}\n\n", log

# Поиск интерфейса по MAC-адресу и сохранение результата в файл
result, log = find_interface_by_mac(device_params, mac_address)

with open('interface_output.txt', 'w') as output_file:
    output_file.write(result)

with open('debug_log_mac.txt', 'w') as log_file:
    for entry in log:
        log_file.write(entry + '\n')

print("Поиск завершен. Результаты сохранены в interface_output.txt. Логи сохранены в debug_log_mac.txt")
