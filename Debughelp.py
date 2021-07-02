import inspect
import sys

DEBUG = False

def retrieve_name_ex(var):
    stacks = inspect.stack()
    try:
        callFunc = stacks[1].function
        code = stacks[2].code_context[0]
        startIndex = code.index(callFunc)
        startIndex = code.index("(", startIndex + len(callFunc)) + 1
        endIndex = code.index(")", startIndex)
        return code[startIndex:endIndex].strip()
    except:
        return ""

def outputVar(var):
    print("{} = {}".format(retrieve_name_ex(var),var))
    
def DEBUG_INFO(args:tuple):
    if not DEBUG:
        return

    print("call stack:")

    try:
        raise Exception
    except Exception:
        # 也可以通过异常获取栈信息
        # tb_frame 代表当前栈信息，tb_frame.f_back 代表上一层调用栈信息，tb_frame.f_back.f_back 代表上上层调用，以此类推
        trace = sys.exc_info()[2].tb_frame
        while trace is not None:
            info = "\t{func}({file}:{line})".format(file=trace.f_code.co_filename[trace.f_code.co_filename.rfind("\\")+1:], line=trace.f_lineno, func=trace.f_code.co_name)
            print(info)
            trace = trace.f_back
    print("args:")
    print(args)    
    
    
