
class dc_configsituation:
    def __init__(self):
        self.dc_configsituation_id = ''
        self.dc_configsituation_address = ''
        self.dc_configsituation_pluginname = ''
        self.dc_configsituation_content = ''
        self.dc_configsituation_isupdate = ''

    def initPara(self, dc_configsituation_id, dc_configsituation_address, dc_configsituation_pluginname,dc_configsituation_content,dc_configsituation_isupdate):
        self.dc_configsituation_id = dc_configsituation_id
        self.dc_configsituation_address = dc_configsituation_address
        self.dc_configsituation_pluginname = dc_configsituation_pluginname
        self.dc_configsituation_content = dc_configsituation_content
        self.dc_configsituation_isupdate = dc_configsituation_isupdate

class dc_plugin:
    def __init__(self):
        self.dc_plugin_id = ''
        self.dc_plugin_name = ''
        self.dc_plugin_location = ''

    def initPara(self, dc_plugin_id, dc_plugin_name, dc_plugin_location):
        self.dc_plugin_id = dc_plugin_id
        self.dc_plugin_name = dc_plugin_name
        self.dc_plugin_location = dc_plugin_location

class dc_configsituation:
    def __init__(self):
        self.dc_pluginsituation_id = ''
        self.dc_pluginsituation_name = ''
        self.dc_pluginsituation_address = ''
        self.dc_pluginsituation_isupdate = ''

    def initPara(self, dc_pluginsituation_id, dc_pluginsituation_name, dc_pluginsituation_address,dc_pluginsituation_isupdate):
        self.dc_pluginsituation_id = dc_pluginsituation_id
        self.dc_pluginsituation_name = dc_pluginsituation_name
        self.dc_pluginsituation_address = dc_pluginsituation_address
        self.dc_pluginsituation_isupdate = dc_pluginsituation_isupdate
