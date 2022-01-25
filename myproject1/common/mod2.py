def mysum(a):
    result=0
    for i in range(1,a+1):
        result += i
    return result
if __name__=="__main__":
    mysum(100)