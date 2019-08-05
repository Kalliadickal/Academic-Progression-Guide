# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 21:43:41 2019

@author: SANJU
"""

import numpy as np
import array as ar
import pandas as pd
'''
mat1=ar.array('i',[1,2,3,4])
print("Matrix using array package\n",mat1)
m2=[[2,5,8],[9,6,3],[1,4,7]]
mat2=np.array(m2)
print("Matrix using numpy package and list\n",mat2)
m3=((1,6,9),(10,7,4),(2,5,7))
mat4=np.array(m3)
print("Matrix using numpy package and tuple\n",mat4)
print("The mean value of\n",mat4,"\tis: ",np.mean(mat4))
print("Modulus of\n",mat4,"and\n",mat2,"is\n",np.mod(mat4,mat2))
'''


'''
n=int(input("Enter the number of Rows\n"))
m=int(input("Enter the number of Columns\n"))
mat3 = [ [0] * m for i in range(n) ]
for i in range (n):
    for j in range(m):
        print("Enter Element No:",i,j)
        mat3[i][j] = int(input())
mat3=np.matrix(mat3)
print("The entered matrix is\n",mat3)
print("\nThe Inverse of \n", np.matrix(mat3),"\n is\n",np.linalg.inv(mat3))
mat3_mean=np.mean(mat3)
mat3N=mat3-mat3_mean
mat3N=mat3N/np.max(mat3)
print("The Normalized matrix is\n",mat3N)
mat3=np.matrix(mat3).astype(float)
mat3rec=np.reciprocal(mat3)
print("The Reciprocal matrix is\n",mat3rec)
mat33=np.take(mat3rec,[0,1,2])
mat3cot=1/np.tan(mat33)
print("The cot values are\t",mat3cot)
''''
'''
n=int(input("Enter the number of Emp\n"))
m1=['ID','Age','Salary','Exp']
m=len(m1)
mat3 = [ [0] * m for i in range(n) ]
age = [ [0] * m for i in range(n) ]
for i in range (n):
    for j in range(m):
        print("Enter",m1[j],":")
        mat3[i][j] = int(input())
mat3=np.matrix(mat3)
df=pd.DataFrame(mat3,columns=['ID','Age','Salary','Exp'])
print("The employee details are\n",df)
age=df.loc[df['Age'].idxmin()]
print("The youngest employee is\n",age)
exp=df.loc[df['Exp'].idxmax()]
print("The most expirenced employee is\n",exp)
print("Details according to salary\n",df.sort_values('Salary',ascending=False))
df1=df[(df['Age'] >= 30) & (df['Age'] <= 40)]
print("The average salary of employee between 30 and 40 age group is",df1['Salary'].mean())
'''