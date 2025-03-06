num =-3.082
fk = 2.3 * (num)**3 +5.75*(num)**2 - 7.41 * (num) -10.06
fsecond = 13.8  * num + 11.5
fpro= 6.9 * (num)**2 + 11.5* (num) - 7.41
#fpro = -1.38 * (num)**3 - 5.42 * (num)**2 + 2.57 * num + 10.95
#newx = num - fk/fpro
#print(1 + fpro/57, fpro)
def getValue(value):
    return 2.3 * (value)**3 +5.75*(value)**2 - 7.41 * (value) -10.06
equasion = num - fk/57
#print(equasion, getValue(equasion), abs(equasion - num))


a = -2
b = 0
counter = 0
while (abs(a - b) > 0.001):
    x = (a + b) / 2
    counter+=1
    fa = getValue(a)
    fb = getValue(b)
    fx = getValue(x)

    print(str(counter),"a = " + str(a), "b "+ str(b),"x " + str(x), "f(a) = " + str(fa), "f(b) = "+str(fb) , "f(x)" + str(fx), "|a - b| = " + str(abs(a - b)))
    if(fa * fx < 0):
        b = x
    else:
        a = x