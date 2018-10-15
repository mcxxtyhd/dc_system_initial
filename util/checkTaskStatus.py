import psutil

# 拿到所有的进程名称
def getAllTaskNames():
    taskName=[]

    # 拿到所有的进程ID
    for single_processid in psutil.pids():
        try:
            processor = psutil.Process(single_processid)
            # 将进程ID转换为名称
            taskName.append(processor.name())
        except  Exception:
            pass
    return taskName

def getTargetTaskStatus(taskList):
    # 初始化传出的字典
    dictList={}
    # 所有的进程名称
    all_exist_task_names=getAllTaskNames()
    for single_message in taskList:
        rFirst=single_message.rindex('/')
        allLength=len(single_message)

        # 进程名称
        first_message=single_message[rFirst+1:allLength]

        # 控件的名称
        second_message=single_message[0:rFirst]
        second_message=second_message[second_message.rindex('/')+1:len(second_message)]

        # 组合的名称  以逗号间隔
        combine_message=second_message+','+first_message

        # 在本机查找一下是否有该进程名
        if first_message in all_exist_task_names:
            dictList.update({combine_message:'yes'})
        else:
            dictList.update({combine_message: 'no'})

    return dictList
