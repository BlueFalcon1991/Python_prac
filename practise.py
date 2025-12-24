# def greet(name):
#     """This function greets the person passed as a parameter."""
#     print(f"Hello, {name}!")

# greet("priyab")


# mlist = [x for x in range(0,11) if x%2==0]
# print(mlist)

# def check_even():
#     num=int(input('enter a number:'))
#     if num%2==0:
#         print(f'the number: {num}, is even!')
#     else:
#         print(f'the number:{num} is odd')

# check_even()



emp_data=[('A',1100),('B',400),('C',500)]
def emp_month(emp_data):
    
    fin_emp=''
    fin_hrs=0
    for name,time in emp_data:
        if time > fin_hrs:
            fin_hrs=time
            fin_emp=name
        else:
            pass
        
    return[fin_emp,fin_hrs]

c=emp_month(emp_data)
print(c)



