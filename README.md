Tracery stone
=====================
Этот набор скриптов обрабатывает файл, содержащий IP-адреса и генерирует файлы конфигурации для 
KAME и маршрутизатора Cisco. Основная статья доступна по ссылке 
[dreamcatcher.ru](http://dreamcatcher.ru/2019/10/02/доступ-к-удаленным-сетям-с-помощью-ipsec-gre-туннеля-между-cisco-ios-и-freebsd)

Установка:
-----------------------------------
Все примеры даны для FreeBSD 12.
Для работы необходимо добавить модули:

    pip-3.6 install requests
    pip-3.6 install pandas
    pip-3.6 install netaddr

Использование:
-----------------------------------

Для работы скрипта необходимо указать параметры:

    datapath = 'data'                                               # Каталог для сохранения файлов
    ipsec_conf_file = 'ipsec.conf'
    cisco_conf_file = 'cisco.conf'                                  
    filename = 'rawip'                                              # Имя файла с базой IP адресов
    url = 'https://github.com/zapret-info/z-i/raw/master/dump.csv'  # Адрес дампа сетей
    mask = '/16'                                                    # Маска для суммаризации сетей
    self_ip = '10.229.33.4/32'                                      # IP внешнего интерфейса
    gre_int_ip = '10.255.200.6'                                     # IP туннельного интерфейса
    local_net = '10.255.0.0/16'                                     # Локальная сеть за Cisco
    remote_site_ext_ip = 'xxx.xxx.xxx.xxx'                          # Внешний IP адрес Cisco
    local_site_ext_ip = 'yyy.yyy.yyy.yyy'                           # Внешний IP адрес FreeBSD
