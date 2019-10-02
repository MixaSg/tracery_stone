import requests
import re
import numpy as np
import ipaddress
import netaddr
import io


def get_file(url, datapath, filename):
    """
    :param url:
    :param datapath:
    :param filename:
    :return:
    """
    print('Download file from: ', url)
    response = requests.get(url)
    print('Status: ', response.status_code)
    response.encoding = 'utf-8'
    raw_file = response.content

    paradata_file = io.open(str(datapath) + "/" + str(filename) + ".txt", "w", encoding="utf-8")
    paradata_file.write(str(raw_file))
    paradata_file.close()
    print("File was stored\n")


def parse_file(datapath, filename):
    """
    :param datapath:
    :param filename:
    :return:
    """
    raw_file = open(str(datapath) + "/" + str(filename) + ".txt", "r")
    raw_ips = []

    for text in raw_file.readlines():
        text = text.rstrip()
        found = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', text)
        raw_ips.extend(found)

    ips = np.asarray(raw_ips)   # Переводим в формат numpy
    print("Total IP addresses found: ", ips.shape[0])
    return ips


def sort(raw_ips):
    """
    :param raw_ips:
    :return:
    """
    return np.sort(raw_ips)


def collapse(ips, mask, remote_site_ext_ip, local_site_ext_ip):
    """
    :param ips:
    :param mask:
    :return:
    """
    tmp_net = []
    net = []
    for i in range(0, ips.shape[0]):
        tmp_net.append(ipaddress.ip_interface(str(str(netaddr.IPAddress(ips[i], flags=netaddr.ZEROFILL).ipv4()) + mask)))  # Чистим строки от лишних 0 в начале октета, добавляем маску
        net.append(str(tmp_net[i].network))                         # Получаем адрес сети согласно маске

    nets = np.asarray(net)                                           # Переводим в numpy
    nets = np.unique(nets, axis=0)                                    # Удаляем дубликаты

    # Для предотвращения ошибок маршрутизации, мы должны удалить из массива сети,
    # соотетствующие remote_site_ext_ip, local_site_ext_ip по mask

    delete_remote = str(ipaddress.ip_interface(str(str(netaddr.IPAddress(remote_site_ext_ip, flags=netaddr.ZEROFILL).ipv4()) + mask)).network)
    delete_local = str(ipaddress.ip_interface(str(str(netaddr.IPAddress(local_site_ext_ip, flags=netaddr.ZEROFILL).ipv4()) + mask)).network)

    nets = np.delete(nets, np.where(nets == delete_remote))
    nets = np.delete(nets, np.where(nets == delete_local))

    print('Total networks: ', nets.shape[0])
    return nets


def generate_config(datapath, ipsec_conf_file, cisco_conf_file, nets, self_ip, local_net, gre_int_ip):
    """
    :param datapath:
    :param conf_file:
    :param nets:
    :param self_ip:
    :param local_net:
    :return:
    """
    ipsec_file = open(datapath + "/" + str(ipsec_conf_file), "w")

    ipsec_file.write(str('flush;\n'))
    ipsec_file.write(str('spdflush;\n'))
    ipsec_file.write(str('spdadd -4 ' + self_ip + ' 8.8.8.8/32 any -P out none;\n'))
    ipsec_file.write(str('spdadd -4 8.8.8.8/32 ' + self_ip + ' any -P in none;\n\n'))
    ipsec_file.write(str('spdadd -4 ' + local_net + ' 8.8.8.8/32 any -P out none;\n'))
    ipsec_file.write(str('spdadd -4 8.8.8.8/32 ' + local_net + ' any -P in none;\n\n'))

    for i in range(0, nets.shape[0]):
        ipsec_file.write(str('spdadd -4 ' + self_ip + ' ' + nets[i] + ' any -P out none;\n'))
        ipsec_file.write(str('spdadd -4 ' + nets[i] + ' ' + self_ip + ' any -P in none;\n\n'))
        ipsec_file.write(str('spdadd -4 ' + local_net + ' ' + nets[i] + ' any -P out none;\n'))
        ipsec_file.write(str('spdadd -4 ' + nets[i] + ' ' + local_net + ' any -P in none;\n\n'))
    ipsec_file.close()

    cisco_file = open(datapath + '/' + str(cisco_conf_file), 'w')

    for i in range(0, nets.shape[0]):
        net = ipaddress.IPv4Network(nets[i], strict=True).network_address
        mask = ipaddress.IPv4Network(nets[i], strict=True).netmask
        cisco_file.write('ip route ' + str(net) + ' ' + str(mask) + ' ' + str(gre_int_ip) + '\n')
        cisco_file.write(str('ip prefix-list RIP seq ' + str(i + 100) + ' permit ' + nets[i] + ' \n'))
    cisco_file.close()




