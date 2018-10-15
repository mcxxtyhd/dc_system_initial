import re

class convertMethod:
    # 查看是否是数字
    def method48(self, inString):
        # 只要转数字不成功就是字符串
        stringOld = str(inString)
        tFlag=True

        # 能转换成功就是数字
        try:
            intNew = float(stringOld)
        except Exception:
            tFlag = False
        finally:
            return tFlag

    # 确认是否是制定的数字类型
    def method49(self, inString):
        tFlag=False
        outString = str(inString)
        # 数字打头
        pattern = re.compile(r'^[0-9]')

        match = pattern.search(outString)

        # 1、先判断是否是数字打头
        if match:
            # 第二个字母不得是 ;或者：
            pattern3 = re.compile(r'^[0-9][:：]')
            match3 = pattern3.search(outString)
            if match3:
                # 这部分是不符合的
                pass
            else:
                tFlag = True
                print(outString)

        # 2、在判断是否由负号和数字打头
        if tFlag == False:
            pattern2 = re.compile(r'^-[0-9]')
            match2 = pattern2.search(outString)
            if match2:
                tFlag = True
                print(outString)

        # 3、再判断是否由 '〈'  '≥' '>' 打头
        if tFlag == False:
            pattern4 = re.compile(r'^[〈≥>]')
            match4 = pattern4.search(outString)
            if match4:
                tFlag = True
                print(outString)

        # 4、再判断是否由  '>='  '<=' '<<'打头
        if tFlag == False:
            pattern5 = re.compile(r'^>=|<=|<<')
            match5 = pattern5.search(outString)
            if match5:
                tFlag = True
                print(outString)

        return tFlag


    # 查看是否包含中文
    def method50(self,inString):
        outString=str(inString)
        # 汉字
        pattern = re.compile(r'[\u4e00-\u9fa5]+')

        match = pattern.search(outString)

        if match:
            print(outString)
            return True
        else:
            return False

    def method51(self,inString):
        outString=inString.strip()
        # 汉字
        pattern = re.compile(r'[\u4e00-\u9fa5]+')

        # 如果是F打头
        if inString.startswith('F'):
            result1 = pattern.findall(inString)
            for t in result1:
                outString = outString.replace(t, str(''))

        # 将空的括号给去掉
        if outString.__contains__("(") and outString.__contains__(")"):
            if outString.index("(") + 1 == outString.index(")"):
                outString = outString.replace("(", "")
                outString = outString.replace(")", "")

        return outString

    def method52(self, inString):

        if inString=='ICU一病区' or inString=='ICU二病区' or inString=='东院区ICU病房':
            return 'ICU'
        else:
            return inString

    def method53(self, inString):

        if inString=='东二病区(急诊内科)' or inString=='东二病区(急诊监护)':
            return '东二病区'
        else:
            return inString

    def method54(self, inString):

        if inString=='东十一(疼痛科)' or inString=='东十一病区(中医科)' or inString=='东十一病区(疼痛科)' or inString=='东十一（中医科）':
            return '东十一病区'
        else:
            return inString

    def method55(self, inString):

        if inString=='东院区外科一病房' or inString=='东院区外科二病房':
            return '外科'
        else:
            return inString

    def method56(self, inString):

        if inString=='产科(中三)' or inString=='产科(北三)':
            return '产科'
        else:
            return inString

    def method57(self, inString):

        if inString=='介入  (综合二层)病房' or inString=='介入治疗(综合二)':
            return '介入'
        else:
            return inString

    def method58(self, inString):

        if inString=='化疗  (中心五)病房' or inString=='化疗  (中心四)病房' or inString=='化疗五(中心五)' or inString=='化疗四(中心四)':
            return '化疗'
        else:
            return inString

    def method59(self, inString):

        if inString=='呼吸内科一(东三)' or inString=='呼吸内科二(西三)':
            return '呼吸内科'
        else:
            return inString

    def method60(self, inString):

        if inString=='呼吸监护病区(RICU)' or inString=='呼吸监护病区（RICU)':
            return 'RICU'
        else:
            return inString

    def method61(self, inString):

        if inString=='妇科(中一)' or inString=='妇科(南一)' or inString=='妇科病房(北二)':
            return '妇科'
        else:
            return inString

    def method62(self, inString):

        if inString=='康复一病区' or inString=='康复二病区' or inString=='康复五病区':
            return '康复'
        else:
            return inString

    def method63(self, inString):

        if inString=='心内  (西九)病房' or inString=='心内(西九)':
            return '心内'
        else:
            return inString

    def method64(self, inString):

        if inString=='放疗  (中心三)病房' or inString=='放疗  (中心二)病房' or inString=='放疗三(中心三)' or inString=='放疗二(中心二)':
            return '放疗'
        else:
            return inString

    def method65(self, inString):

        if inString=='皮科  (综合二层)病房' or inString=='皮肤科(综合二)':
            return '皮肤科'
        else:
            return inString

    def method66(self, inString):

        if inString=='血液七(中心七)' or inString=='血液八(中心八)' or inString=='血液六(中心六)':
            return '血液科'
        else:
            return inString