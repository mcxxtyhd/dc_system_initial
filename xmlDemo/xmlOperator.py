import xml.etree.ElementTree as ET

class xmlOperator:
    def __init__(self,xmlPath):
        self.xmlPath=xmlPath
        self.tree = ET.parse(self.xmlPath)
        self.root = self.tree.getroot()

    # 获得指定xml文件的制定内容
    def getDataByXml(self,targetAddress):
        targetData = {}

        for fatherNode in self.root.findall('agent'):
            if fatherNode.get('address') == targetAddress:
                for i in fatherNode:
                    for sonNode in i:
                        # 获得指定的信息
                        targetData.update({i.attrib.get('name'): sonNode.text})

        return targetData

    # 更改指定xml文件的制定内容
    def editDataByXml(self,targetAddress,targetPlugin):

        for fatherNode in self.root.findall('agent'):
            if fatherNode.get('address') == targetAddress:
                for i in fatherNode:
                    for sonNode in i:
                        if i.attrib.get('name') in targetPlugin:
                            # 获得指定的信息
                            sonNode.text='NO'

        self.tree.write(self.xmlPath)

    # 查找一下是否需要新加地址节点
    def addNewAgent(self, AgentAddress,plugins):
        isFind = 1
        for fatherNode in self.root.findall("agent"):
            # 查看是否能找到这个节点
            if fatherNode.get('address') == AgentAddress:
                isFind = 2

        if isFind == 1:
            # 创建新节点并添加为root的子节点
            newEle = ET.Element("agent")
            newEle.attrib = {"address": str(AgentAddress)}

            for i in plugins:
                newElesSonPlugin = ET.Element("plugin")
                newElesSonPlugin.set('name', i)

                newElesSonUpdate = ET.Element("update")
                newElesSonUpdate.text='NO'
                newElesSonPlugin.append(newElesSonUpdate)
                newEle.append(newElesSonPlugin)

            self.root.append(newEle)
            # 写回原文件
            self.tree.write(self.xmlPath,"UTF-8")

    # 查找一下是否需要新加地址节点
    def addNewPlugin(self,newPluginName):

        # 遍历每个地址
        for fatherNode in self.root.findall("agent"):
            tFlag=False

            # 遍历每个插件
            for pluginNode in fatherNode.findall("plugin"):
                # 查找该地址中是否有该插件
                if pluginNode.get('name') == newPluginName:
                    tFlag = True
                    break

            # 没有找到该新的插件
            if tFlag==False:
                # 就往这个节点加这个新的插件
                newElesSonPlugin = ET.Element("plugin")
                newElesSonPlugin.set('name', newPluginName)
                newElesSonUpdate = ET.Element("update")
                newElesSonUpdate.text = 'NO'
                newElesSonPlugin.append(newElesSonUpdate)
                # 加到该agent端的所有插件之中
                fatherNode.append(newElesSonPlugin)

        # 写回原文件
        self.tree.write(self.xmlPath, "UTF-8")

    # 查找一下是否需要新加地址节点
    def deletePlugin(self, deletePluginName):

        # 遍历每个地址
        for fatherNode in self.root.findall("agent"):

            # 遍历每个插件
            for pluginNode in fatherNode.findall("plugin"):
                # 查找该地址中是否有该插件
                if pluginNode.get('name') == deletePluginName:
                    fatherNode.remove(pluginNode)

        # 写回原文件
        self.tree.write(self.xmlPath, "UTF-8")
