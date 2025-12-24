emp_data=[('A',100),('B',400),('C',200)]
def emp_month(emp_data):
    
    fin_emp=''
    fin_hrs=0
    for name,time in emp_data:
        if time > fin_hrs:
            fin_hrs=time
            fin_emp=name
        else:
            pass
        
    return(fin_emp,fin_hrs)

c=emp_month(emp_data)
print(c)
    