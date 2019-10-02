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

inc.get_file(url, datapath, filename)
raw_ips = inc.parse_file(datapath, filename)
ips = inc.sort(raw_ips)
nets = inc.collapse(ips, mask, remote_site_ext_ip, local_site_ext_ip)
inc.generate_config(datapath, ipsec_conf_file, cisco_conf_file, nets, self_ip, local_net, gre_int_ip)

