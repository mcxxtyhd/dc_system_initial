import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 初始化数据库连接:
from internetProgramming.FileDownClass import FileDownClass
from model import dc_pluginsituation, dc_plugin, dc_pluginsituation_service,dc_agent,dc_configsituation
from util.getlocalhostAddress import getlocaladdress
import pymssql

class agent:
    def __init__(self,server_address,server_port,server_database,server_user,server_password):
        self.server_address=server_address
        self.server_port = server_port
        self.server_database = server_database
        self.server_user = server_user
        self.server_password = server_password
        self.local_address=getlocaladdress()

        engine = create_engine('mssql+pymssql://'+str(self.server_user)+':'+str(self.server_password)+'@'+str(self.server_address)+':'+str(self.server_port)+'/'+str(self.server_database)+'?charset=utf8')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建Session:
        self.session = DBSession()

    # 初始化agent端的控件信息 (需要新增哪些控件情况数据，已经有了的就不增加数据)
    def init_agent_plugins(self,agent_address):
        # 初始化当前地址的对应的主键 id
        current_agent_id=''

        # 1、客户端地址的信息初始化
        target_agent=self.session.query(dc_agent).filter(dc_agent.dc_agent_address == agent_address).all()
        if not target_agent:
            new_agent=dc_agent(dc_agent_address=agent_address,dc_agent_operate='empty')
            self.session.add(new_agent)
            self.session.flush()
            current_agent_id = new_agent.dc_agent_id
        else:
            current_agent_id = target_agent[0].dc_agent_id

        # 2、控件情况信息的初始化
        all_exist_plugins=[]
        # # 查找agent上所有控件的情况

        target_agent=self.session.query(dc_pluginsituation).join(dc_agent).filter(dc_agent.dc_agent_address == agent_address).all()
        for single_agent_plugin in target_agent:
            all_exist_plugins.append(single_agent_plugin.dc_pluginsituation_name)

        all_plugins = self.session.query(dc_plugin).all()
        for single_plugin in all_plugins:
            # 查看每一个控件，这个agent地址是否有对应的控件与其匹配
            if single_plugin.dc_plugin_name not in all_exist_plugins:
                # 没有就新增
                single_dc_pluginsituation=dc_pluginsituation( dc_agent_id=current_agent_id, dc_pluginsituation_name=single_plugin.dc_plugin_name,dc_pluginsituation_isupdate='yes')
                self.session.add(single_dc_pluginsituation)
                self.session.flush()

        self.session.commit()

    # 获得指定agent端控件的更新情况
    def get_agent_updatedplugins(self,agent_address):
        all_need_update_plugin=[]

        # 对所有的控件进行查询
        all_plugins = self.session.query(dc_pluginsituation).join(dc_agent).filter(dc_agent.dc_agent_address == agent_address).filter(dc_pluginsituation.dc_pluginsituation_isupdate=='yes').all()

        for i in all_plugins:
            all_need_update_plugin.append(i.dc_pluginsituation_name)
        return all_need_update_plugin

    # 更新指定agent的控件更新情况
    def update_agent_plugins(self,agent_address,plugins_update):
        # 查找对应地址、并且在更新控件列表中
        all_update_plugins = self.session.query(dc_pluginsituation).join(dc_agent).filter(dc_agent.dc_agent_address == agent_address).filter(dc_pluginsituation.dc_pluginsituation_name.in_(plugins_update)).all()
        for single_plugin in all_update_plugins:
            single_plugin.dc_pluginsituation_isupdate = 'no'
            self.session.flush()
        self.session.commit()

    # 拿到制定客户端地址的控件更新动作信息
    def get_agent_plugins_action(self, agent_address):
        dict = {}
        # 初始化控件放在服务器的地址
        target_agent_address = "C:/TheoTestShell"
        # 1、先是拿到该地址的所有控件
        all_plugins=self.session.query(dc_pluginsituation).join(dc_agent).filter(dc_agent.dc_agent_address==agent_address).all()

        # 2、之后在每个控件下查找是否有需要更新的服务
        for single_plugin in all_plugins:
            # 3、查找该控件下所有的有操作的服务
            single_plugin_allservices=self.session.query(dc_pluginsituation_service).join(dc_pluginsituation).filter(dc_pluginsituation.dc_pluginsituation_id==single_plugin.dc_pluginsituation_id,dc_pluginsituation_service.dc_pluginsituation_service_Operate!= 'empty').all()
            for single_service in single_plugin_allservices:

                # 4、拼凑成字典传给客户端(说明要进行什么操作)

                # 拿到控件的名称
                operate_plugin_name=str(single_plugin.dc_pluginsituation_name)
                # 去掉压缩的type
                operate_plugin_name=operate_plugin_name[0:len(operate_plugin_name) - 4]
                # 整合名称
                operate_plugin_name=target_agent_address+r'/'+operate_plugin_name+r'/'+single_service.dc_pluginsituation_service_name
                dict.update({operate_plugin_name:single_service.dc_pluginsituation_service_Operate})

                # 5、修改数据库对应的状态进行更替(如果启动或者关闭失败仍然改变状态  这个问题暂时忽略)
                if single_service.dc_pluginsituation_service_Operate=='turnon':
                    single_service.dc_pluginsituation_service_status = 'on'
                else:
                    single_service.dc_pluginsituation_service_status = 'off'

                single_service.dc_pluginsituation_service_Operate = 'empty'
                self.session.flush()
        self.session.commit()
        return dict

    # 拿到制定客户端地址的配置文件更新状态
    def get_agent_plugins_config(self, agent_address):
        all_configs={}
        # 找到该IP下面的所有控件
        all_plugins=self.session.query(dc_pluginsituation).join(dc_agent).filter(dc_agent.dc_agent_address==agent_address).all()

        for single_plugin in all_plugins:
            # 查找需要更新的配置文件(即需要重新读取的配置文件)
            agent_configs = self.session.query(dc_configsituation).filter(dc_configsituation.dc_pluginsituation_id==single_plugin.dc_pluginsituation_id,dc_configsituation.dc_configsituation_isupdate=='yes').all()
            for single_config in agent_configs:

                # 拿到控件的名称
                update_plugin_name = str(single_plugin.dc_pluginsituation_name)

                # 去掉压缩的type
                update_plugin_name = update_plugin_name[0:len(update_plugin_name) - 4]

                # 将控件的ID放在这里
                update_plugin_name=str(update_plugin_name)+','+str(single_config.dc_configsituation_id)
                all_configs.update({update_plugin_name:single_config.dc_configsituation_configname})

        return all_configs

    # 读取从agent端传来的配置文件信息
    def update_agent_config(self, agent_config_update_data):
        # 第一个参数是[地址，控件名称，配置文件名称]，第二个是文件内容
        for agent_plugin,agent_service in eval(agent_config_update_data).items():
            pluginconfig_data_split=str(agent_plugin).split(',')
            # IP地址
            agent_address=pluginconfig_data_split[0]
            # 配置文件id
            plugin_id = pluginconfig_data_split[1]
            # 控件名称
            plugin_name=pluginconfig_data_split[2]
            # 配置文件名称
            config_name=pluginconfig_data_split[3]

            target_config=self.session.query(dc_configsituation).get(plugin_id)
            # 先清空
            target_config.dc_configsituation_content=''
            # 遍历插入数据
            for single_line in agent_service:
                target_config.dc_configsituation_content+=single_line
            # 关闭读取文件
            target_config.dc_configsituation_isupdate='no'

            self.session.flush()
        self.session.commit()

    # 拿到需要更新的控件配置文件内容信息
    def get_target_configs_data(self, agent_ipaddress):
        # 初始化控件配置文件字典
        configs_data={}

        # 找到该IP下面的所有控件
        all_plugins = self.session.query(dc_pluginsituation).join(dc_agent).filter(dc_agent.dc_agent_address == agent_ipaddress).all()

        for single_plugin in all_plugins:
            # 查找需要经过手动更改后的的配置文件
            agent_configs = self.session.query(dc_configsituation).filter(dc_configsituation.dc_pluginsituation_id == single_plugin.dc_pluginsituation_id,
                                                                          dc_configsituation.dc_configsituation_isManualEdit == 'yes').all()
            for single_config in agent_configs:
                # 获取文件内容
                target_plugin_config_path=str(single_plugin.dc_pluginsituation_name).split('.')[0]
                target_plugin_config_path+=r'/'+single_config.dc_configsituation_configname
                configs_data.update({target_plugin_config_path:str(single_config.dc_configsituation_content)})

                # 将此文件的更新状态改为无需更新
                single_config.dc_configsituation_isManualEdit='no'
                self.session.flush()

        self.session.commit()
        return configs_data

    # 拿到客户端程序的操作动作
    def get_target_agent_action(self, agent_ipaddress):
        action_data = ''

        # 找到该IP下面的agent
        target_agent = self.session.query(dc_agent).filter(dc_agent.dc_agent_address == agent_ipaddress).first()
        if target_agent.dc_agent_operate!='empty':

            # 获取操作动作
            action_data=target_agent.dc_agent_operate

            # 置为空
            target_agent.dc_agent_operate='empty'
            self.session.flush()
            self.session.commit()
            return action_data
        else:
            return 'empty'

#
# theo = agent('192.168.11.162', '1434', 'dc_system', 'sa', '123')
# print(theo.get_target_agent_action('192.168.13.133'))