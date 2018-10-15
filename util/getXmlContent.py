from xml.dom.minidom import parse
import xml.dom.minidom

import xml.etree.ElementTree as ET


class loadConfig:
    def __init__(self, filepath):
        self.filepath = filepath

    def getTagContent(self, tag):

        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(self.filepath)
        collection = DOMTree.documentElement
        if collection.hasAttribute(tag):
            return collection.getAttribute(tag)
        else:
            return 'NO'

    # 判断子节点是否修改
    def judgeIfSonUpdate(self, address):

        tree = ET.parse(self.filepath)
        root = tree.getroot()
        for country in root.findall('agent'):
            if country.attrib['address'] == address:
                years = country.findall('isUpdate')
                return years[0].text

    # 将子节点置为已修改(NO)
    def changeSonUpdate(self, address):

        tree = ET.parse(self.filepath)
        root = tree.getroot()
        for country in root.findall('agent'):
            if country.attrib['address'] == address:
                years = country.findall('isUpdate')
                years[0].text='NO'
                tree.write(self.filepath)

                backContent=str(address)+',子节点xml已经修改完毕'
                return backContent

    # # 判断所有子节点是否修改 修改了就把父节点置为no
    # def judgeAllUpdate(self, address):
    #
    #     tree = ET.parse(self.filepath)
    #     root = tree.getroot()
    #     for country in root.findall('agent'):
    #         years = country.findall('isUpdate')
    #         if years[0].text=='YES':
    #             return False
    #     # 走到这里说明所有的都修改完毕了 那就开始改


test=loadConfig("D:\\pythonProject\\testDeploy\\config.xml")
print(test.getTagContent("isNeedUpdate"))