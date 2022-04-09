def rounded_division(n1,n2,string,percent):
    x=rounded(n1/n2)
    if percent==True:
        x=rounded(x*100)
    if string==True:
        return str(x)
    return x
def rounded(number):
    return int(number*1000)/1000
def RELU(number):
    if number<0:
        return 0
    return number
def iinput(text):
    try:
        return int(input(text))
    except:
        return 0
