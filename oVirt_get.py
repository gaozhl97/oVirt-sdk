"""
@Version:    V1.0
@author:    gaozhl
@time:      2021.03.11
"""
import requests
import re
import xml.etree.ElementTree as ET

CACERT = r'./ca.crt'
auth = ('admin@internal', 'Xlj#!1125')
headers = {
    'Version':  '4',
    'Accept':   'application/xml',
}


def get_API():
    """Get the API
    获取ovirt-engine的所有api 
    返回api列表

    Args:
        NULL
    Returns:
        API list of ovirt engine
    """
    # 请求内容
    response_get_API = requests.get('https://billing-app-012/ovirt-engine/api',
                                    headers=headers, auth=auth, verify=CACERT)
    data = response_get_API.text
    # print(data)

    # deal the response to get the API functions
    root = ET.fromstring(data)
    API = []
    for child in root:
        # 先行判断防止出现KeyError
        if 'rel' in child.attrib:
            # print(child.tag, child.attrib)
            API_func = child.attrib['rel']
            # print("API function:" + API_func)
            API.append("/ovirt-engine/api/" + API_func)
    return API


def get_DATA_CENTER():
    """Get the id of data center
    获取data center的id

    Args:
        NULL
    Returns:
        id of data center.
    """
    # requests
    response_get_DATA_CENTER = requests.get(
        'https://billing-app-012/ovirt-engine/api/datacenters',
        headers=headers, auth=auth, verify=CACERT)
    data = response_get_DATA_CENTER.text
    # print(data)

    # deal the response to get the id
    root = ET.fromstring(data)
    for child in root:
        if 'id' in child.attrib:
            # print(child.tag, child.attrib)
            id = child.attrib['id']
    return id


def get_HOST():
    """Get the host in data center

    Args:
        NULL
    Returns:
        hosts in data center.
    """
    response_get_HOST = requests.get(
        'https://billing-app-012/ovirt-engine/api/hosts',
        headers=headers, auth=auth, verify=CACERT)
    data = response_get_HOST.text
    # print(data)

    # deal the response to get the HOST infomation
    root = ET.fromstring(data)
    HOST = []
    for child in root:
        # print(child.tag, child.attrib)
        if 'id' in child.attrib:
            # 读取data center的主机相关参数
            HOST_address = child.find('address').text
            HOST_comment = child.find('comment').text
            HOST_name = child.find('name').text
            HOST_id = child.attrib['id']
            # 构建临时的host相关参数到一条list中
            HOST_temp = [HOST_id, HOST_address, HOST_name, HOST_comment]
            # 汇总到总的HOST信息
            HOST.append(HOST_temp)
    return HOST


def get_STOREAGEDOMAINS():
    """Get the iso storeagedomains
    得到ISO文件所在的存储域storeagedomains

    Args:
        NULL
    Returns:
        storeagedomains of the iso
    """
    response_get_storeagedomains = requests.get(
        'https://billing-app-012/ovirt-engine/api/storagedomains',
        headers=headers, auth=auth, verify=CACERT)
    data = response_get_storeagedomains.text
    # print(data)

    # deal the response to get the iso storeagedomains id
    # maybe somewhere is wrong with it.
    # ISO_STOREAGEDOMAINS = []
    # root = ET.fromstring(data)
    # for child in root.iter("mac_pool"):
    #     if 'id' in child.attrib:
    #         # print(child.attrib['id'])
    #         ISO_STOREAGEDOMAINS.append(child.attrib['id'])
    # return ISO_STOREAGEDOMAINS
    STOREAGEDOMAINS = []
    root = ET.fromstring(data)
    for child in root:
        # print(child.tag, child.attrib)
        if 'id' in child.attrib:
            # print(child.attrib['id'])
            STOREAGEDOMAINS_id = child.attrib['id']
            STOREAGEDOMAINS_name = child.find('name').text
            STOREAGEDOMAINS_description = child.find('description').text
            STOREAGEDOMAINS_temp = [
                STOREAGEDOMAINS_id, STOREAGEDOMAINS_name, STOREAGEDOMAINS_description]
            # print(STOREAGEDOMAINS_temp)
            STOREAGEDOMAINS.append(STOREAGEDOMAINS_temp)
    return STOREAGEDOMAINS


def get_ISO_id(iso_storeagedomains):
    """Get the id of ISO in iso storeagedomains

    Args:
        id of iso_storeagedomains
    Returns:
        the id of iso in iso storeagedomains
    """
    url_iso = 'https://billing-app-012/ovirt-engine/api/storagedomains/' + \
        iso_storeagedomains + '/disks'
    # print(url_iso)
    response_get_ISO_id = requests.get(url=url_iso, headers=headers, auth=auth, verify=CACERT)
    data = response_get_ISO_id.text
    # 此处的data会返回所有的磁盘与存储的id内容
    # print(data)

    ISO_infomation = []
    root = ET.fromstring(data)
    for child in root:
        if 'id' in child.attrib:
            ISO_id = child.attrib['id']
            ISO_name = child.find('name').text
            ISO_temp = [ISO_id, ISO_name]
            ISO_infomation.append(ISO_temp)
    return ISO_infomation


def main():
    # 获取所有API
    print("\n==========API:")
    get_API()
    for i in range(len(get_API())):
        print(get_API()[i])

    # 获取data center的id
    print("\n==========DATA_CENTER id:")
    id = get_DATA_CENTER()
    print(id)

    # 获取data center的HOST相关信息
    print("\n==========HOST infomation:\n \
        [HOST_id, HOST_address, HOST_name, HOST_comment]:")
    get_HOST()
    for i in range(len(get_HOST())):
        print(get_HOST()[i])
        # Get the host id:
        # print(get_HOST()[i][0])

    # 获取iso的storeagedomains
    print("\n==========iso storeagedomains id: \n \
        [STOREAGEDOMAINS_id, STOREAGEDOMAINS_name, STOREAGEDOMAINS_description]")
    for i in range(len(get_STOREAGEDOMAINS())):
        print(get_STOREAGEDOMAINS()[i])

    # 此处取ISO的值
    print("\n==========iso id:")
    iso_storeagedomains = get_STOREAGEDOMAINS()[1][0]
    print("Using domains id:\t" + iso_storeagedomains)
    get_ISO_id(iso_storeagedomains)
    for i in range(len(get_ISO_id(iso_storeagedomains))):
        print(get_ISO_id(iso_storeagedomains)[i])


if __name__ == '__main__':
    main()
