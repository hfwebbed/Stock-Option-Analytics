import math
# should solve quadratic equation

def square_of(some_number):
    return some_number * some_number


def square_root_of(some_number):
    return math.sqrt(some_number)


a = 2.0
b = 3.0
c = -4.0
print("a=", a,"b=", b,"c=", c)

d = square_of(b) - 4 * a * c
if d < 0:
    print("no roots for this equation")
    quit()

# find x1 and x2 for this equation


x1 = (-1 * b + square_root_of(d)) / 2 * a
x2 = (-1 * b - square_root_of(d)) / 2 * a

# do not edit enything below this comment
roots = [x1,x2]
print("calculated x1 and x2 are equal to ", roots)
for root in roots:
    check = a * square_of(root) + b * root + c
    if math.fabs(check) < 0.00001 :
        print("root" , root , " is correct")
    else:
        print("x1 is not correct because a * root  * root + b * root + c =",check)






