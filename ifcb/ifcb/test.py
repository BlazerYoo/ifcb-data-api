from msg import success_msg, info_msg, error_msg
import datetime

def innerFunc():
    info_msg('running innerFunc')
    success_msg('innerFunc success!')
    #raise Exception('innerFunc failed!')

def middleFunc():
    try:
        info_msg('running middleFunc')
        innerFunc()
        raise Exception('')
        #success_msg('middleFunc succcess!')
    except Exception as ex:
        raise Exception('middleFunc failed! -> ' + str(ex))

def outerFunc():
    try:
        info_msg('running outerFunc')
        middleFunc()
        success_msg('outerFunc succcess!')
    except Exception as ex:
        error_msg('print from outer -> ' + str(ex))

a = datetime.datetime(2023, 6, 21, 12, 12, 12)
print(f'time is: {a}')