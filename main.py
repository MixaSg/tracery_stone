#
#
#

import include as inc

datapath = 'data'
ipsec_conf_file = 'ipsec.conf'
cisco_conf_file = 'cisco.conf'
filename = 'rawip'
url = 'https://github.com/zapret-info/z-i/raw/master/dump.csv'      # Адрес дампа сетей
mask = '/16'                                                        # Маска для суммаризации сетей
self_ip = '10.229.33.4/32'                                          # IP внешнего интерфейса
gre_int_ip = '10.255.200.6'                                         # IP туннельного интерфейса
local_net = '10.255.0.0/16'
remote_site_ext_ip = 'xxx.xxx.xxx.xxx'
local_site_ext_ip = 'yyy.yyy.yyy.yyy'
exclude_net = ['10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '100.64.0.0/10', '127.0.0.0/8', '169.254.0.0/16',
               '192.0.0.0/24', '192.0.2.0/24', '198.18.0.0/15', '198.51.100.0/24', '203.0.113.0/24',
               '224.0.0.0/4', '240.0.0.0/4']


inc.get_file(url, datapath, filename)
raw_ips = inc.parse_file(datapath, filename)
ips = inc.sort(raw_ips)
nets = inc.collapse(ips, mask, exclude_net, remote_site_ext_ip, local_site_ext_ip)
inc.generate_config(datapath, ipsec_conf_file, cisco_conf_file, nets, self_ip, local_net, gre_int_ip)

