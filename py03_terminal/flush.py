import os
import sys
import time
"""
https://stackoverflow.com/questions/39177788/python-sys-stdout-flush-on-2-lines-in-python-2-7

"""

def flushProcessBar():
    print("-- Singleline Flush --")
    import time
    cnt = 1
    while cnt <100:
        sys.stdout.flush()
        time.sleep(0.01)
        ## 注意使用 软回车 "\r"，这样才可以刷新缓冲
        msg = "idx: {:02d}\r".format(cnt)
        sys.stdout.write(msg)
        cnt += 1
    ## 保留结果
    print("idx: {:02d}".format(cnt))

def flushProcessBar2():
    print("-- Multilines Flush --")
    idxs = [0,0,0]
    lens = len(idxs)
    CURSOR_UP_ONE = '\x1b[1A'  # go to the upperline
    ERASE_LINE = '\x1b[2K'     # overwrite the data
    tag = lens*"{}{}".format(CURSOR_UP_ONE, ERASE_LINE)
    print("==>\n"*lens,end="\r")
    for x in range(100):
        time.sleep(0.01)
        for i in range(lens):
            idxs[i] +=1
        msg = "".join("idx: {}\n".format(i) for i in idxs)
        sys.stdout.write(tag)
        sys.stdout.write(msg)
        sys.stdout.flush()

if __name__ == "__main__":
    flushProcessBar()
    flushProcessBar2()

