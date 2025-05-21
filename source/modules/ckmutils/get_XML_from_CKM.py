import requests
import xml.etree.ElementTree as ET

def get_XML_from_CKM_size(url,header,size):
    print('Downloading XML bite-sized')
    offset = 0
    #size = 20
    xml_list=[]
    for i in range(100):
        url_sized = url + '?size=' + str(size) + '&offset=' + str(offset + i * size)
        #print(url_sized)
        xml_response = requests.get(url_sized, headers=header)
        xml_response.encoding = 'utf-8-sig'
        xml = xml_response.text
        #print(url_sized)
        #print(xml_response.status_code)
        #print(len(xml_response.text))
        if len(xml_response.text)<200:
            break
        else:
            xml_list.append(xml)
    if len(xml_list) > 1:
        for i in range(1,len(xml_list)):
            prev = xml_list[i-1]
            prev_list = prev.split('<')
            prev_list = prev_list[:-1]
            prev = '<'.join(prev_list)
            current = xml_list[i]
            current_list = current.split('<')
            current_list = current_list[3:]
            current = '<'.join(current_list)
            current = '<'+current
            xml_list[i] = prev+current
        xml = xml_list[-1]
    else:
        xml = xml_list[0]
    return ET.fromstring(xml)

def get_XML_from_CKM(url,header):
    print('Downloading XML one-page-only')
    xml_response = requests.get(url, headers=header)
    xml_response.encoding = 'utf-8-sig'
    xml = xml_response.text
    return ET.fromstring(xml)

def main():
    #SWAGGER: https://ckm.openehr.org/ckm/rest-doc/
    #print(get_file_list('../../data', 'adl'))
    XML = get_XML_from_CKM_size('https://ckm.openehr.org/ckm/rest/v1/archetypes',{},150)
    #XML = get_XML_from_CKM_size('https://ckm.salut.gencat.cat/ckm/rest/v1/archetypes',{"Authorization": "Basic cmVzdC5hcGk6c056ajIxJksxazEj"},20)

    print(XML)
    print(len(XML))
    for x in XML:
        print(x)
        if x.find('uid') is not None:
            print(x.find('uid').text)

    tree = XML
    #print(tree.tag)

    for i in range(len(tree)):
        print(tree[i].find('resourceMainId').text)
        print(tree[i].find('resourceMainDisplayName').text)
        print(tree[i].find('cid').text)
        print(tree[i].find('projectName').text)
        print(tree[i].find('cidProject').text)




if __name__ == '__main__':
    main()
