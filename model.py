from sqlalchemy import Column, String, INT, ForeignKey, Time, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 客户端地址信息
class dc_agent(Base):
    # 表的名字:
    __tablename__ = 'dc_agent'

    # 表的结构:
    dc_agent_id = Column(INT(), primary_key=True)

    dc_agent_address = Column(String(200))

    dc_agent_name = Column(String(200))

    dc_agent_operate = Column(String(200))

    dc_agent_ServerStatus = Column(String(200))

    dc_agent_LastConnectTime = Column(DateTime)

# 所有控件
class dc_plugin(Base):
    # 表的名字:
    __tablename__ = 'dc_plugin'

    # 表的结构:
    dc_plugin_id = Column(INT(), primary_key=True)

    dc_plugin_name = Column(String(200))

    dc_plugin_location = Column(String(4000))

# 控件情况
class dc_pluginsituation(Base):
    # 表的名字:
    __tablename__ = 'dc_pluginsituation'

    # 表的结构:
    dc_pluginsituation_id = Column(INT(), primary_key=True)

    dc_agent_id = Column(INT(), ForeignKey('dc_agent.dc_agent_id'))

    dc_pluginsituation_name = Column(String(200))

    dc_pluginsituation_isupdate = Column(String(40))

    dc_pluginsituation_ServerStatus = Column(String(40))

# 配置文件情况
class dc_pluginsituation_service(Base):
    # 表的名字:
    __tablename__ = 'dc_pluginsituation_service'

    # 表的结构:
    dc_pluginsituation_service_id = Column(INT(), primary_key=True)

    dc_pluginsituation_service_name = Column(String(100))

    dc_pluginsituation_service_status = Column(String(40))

    dc_pluginsituation_id = Column(INT(),ForeignKey('dc_pluginsituation.dc_pluginsituation_id'))

    dc_pluginsituation_service_Operate = Column(String(40))

    dc_pluginsituation_service_ServerStatus = Column(String(40))

# 配置文件情况
class dc_configsituation(Base):
    # 表的名字:
    __tablename__ = 'dc_configsituation'

    # 表的结构:
    dc_configsituation_id = Column(INT(), primary_key=True)

    dc_pluginsituation_id = Column(INT(), ForeignKey('dc_pluginsituation.dc_pluginsituation_id'))

    dc_configsituation_configname = Column(String(100))

    dc_configsituation_content = Column(String(999999))

    dc_configsituation_isupdate = Column(String(40))

    dc_configsituation_isManualEdit = Column(String(40))

    dc_configsituation_ServerStatus = Column(String(40))

