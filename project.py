# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:14:55 2018

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 22:05:38 2018

@author: admin
"""
from difflib import SequenceMatcher
import numpy as np
import matplotlib.pyplot as plt
from xlrd import open_workbook
import os
from io import BytesIO
import base64

'''
----------------------------------------------------------------------------
The function definitions starts here...
'''

def get_roll_name(sheet):
    # funtion to return all the name and roll nos. of students
    # from a given sheet
    
    for i in range(len(sheet)):     
        roll=[]
        name=[]
        for j in range(len(sheet[i])):
            try:
                n=int(sheet[i][j])
                if(n>1000000):
                    roll.append(n)
                    name.append(sheet[i+1][j])
            except:
                continue
        if(len(roll)>=len(sheet[i])/8):
            break
        
    return [roll,name]

#------------------------------------------------------------------------------

def get_roll_name_pass(sheet):
    # funtion to return all the name and roll nos. of students
    # from a given sheet
    
    student=[]
    tr=()
    for j in range(len(sheet[0])):
        if(type(sheet[0][j])==str):
            k=SequenceMatcher(a=sheet[0][j],b='Teacher').ratio()
            if(k>=0.5):
                tr=(sheet[1][j],str(sheet[2][j]))

        try:
            n=int(sheet[0][j])
            if(n>1000000):
                student.append((n,sheet[1][j],int(sheet[2][j])))
                
        except:

            continue
   
    return [student,tr]

#------------------------------------------------------------------------------

def get_marks(sheet): 
    # fun. to return the subject wise marks subject wise attendance
    # after receiving the entire sheet
    
    marks=[]             
    for i in range(len(sheet)):
        mark=[]
        for j in range(len(sheet[i])):
            m=sheet[i][j]
            if m=='AA' or m=='NP' :
                m=0
            try:
                m=int(m)
                if(m>=0 and m<=200):
                    mark.append(m)
            except:
                continue
        if(len(mark)>=len(sheet[i])/2):
            marks.append(mark)
            
    endmark=[]
    attendance=[]
    cia=[]
    count=0
    for i in range(len(marks)):
        mark=[]
        a=[]
        ciam=[]
        for j in range(len(marks[0])):
            count=count+1
            if(count%6==0):
                try:
                    t=marks[i][j-4]+marks[i][j-5]  #code to find the total mark for each
                    m=marks[i][j]/t*100        # subject and then convert all obtained
                    m=round(m,2)             # marks to out of 100
                    mark.append(m)             
                except:
                    mark.append(-1)
            if((count-3)%6==0):
                t=marks[i][j-2]
                try:
                    m=marks[i][j]/t*100
                except:
                    m=-1
                ciam.append(round(m,2))
            if((count-4)%6==0):
                at=marks[i][j]
                if(at==5):
                    attn=97.5
                elif at==4:
                    attn=92.5
                elif at==3:
                    attn=87.5
                elif at==2:
                    attn=82.5
                elif at==1:
                    attn=77.5
                else:
                    attn=75
                a.append(attn)   #code to extract the attendance marks
        endmark.append(mark)
        attendance.append(a)
        cia.append(ciam)
    return [endmark,attendance,cia]

#-------------------------------------------------------------------------------

def get_avg_marks(a):
    # function to print the average marks of each subj. and to return it
    # after receiveing the subject wise marks
    
    count=0
    avg=[]
    for i in a:
        count=count+1
        m=sum(i)/len(i)
        avg.append(round(m,2))    
    return avg

#--------------------------------------------------------------------------------

def get_df(book):      
    #fun. to return the data frame of the entire details in 
    # a sheet after receiveing the excel workbook
    
    s=book.sheets()[0]
    df=[]
    for col in range(s.ncols):
        values = []
        for row in range(s.nrows):
            values.append(s.cell(row,col).value)
        #print(values)
        df.append(values)
    return(df)

#--------------------------------------------------------------------------------
def get_student_marks(endmark): 
    # fun. to convert the subject wise marks into
    #  student wise marks   : basically does the transpose
    
    studentmark=[]
    for i in range(len(endmark[0])):
        m=[]
        for j in range(len(endmark)):
            m.append(endmark[j][i])
        studentmark.append(m)
        #studentmark : list contianing the final marks of all students, student wise
    return studentmark

#------------------------------------------------------------------------------

def get_failed_list(studentmark):
    # Funcition accepting marks of all students and printing the list of failed
    # students and returning a list of the failed students
    
    count=0
    fail_list=[]
    for i in range(len(studentmark)):
        for j in range(len(studentmark[0])):
            if studentmark[i][j]<40:
                fail_list.append(i)
                count=count+1
                break

    return fail_list
    

#----------------------------------------------------------------------------
def get_plot_summary(studentmarks,c):
    distinct=0
    iclass=0
    iiclass=0
    pclass=0    
    fails=get_failed_list(studentmarks)
    avg=get_avg_marks(studentmarks)
    
    count=0
    for i in avg:
        try:
            if fails.index(count):
                count=count+1
                continue
        except: 
            if i>=80:
                distinct=distinct+1
            elif i>=60:
                iclass=iclass+1
            elif i>=50:
                iiclass=iiclass+1
            else:
                pclass=pclass+1
        count=count+1
    
    failed=len(fails)
    
    summary = [failed,pclass,iiclass,iclass,distinct]
    
    if(sum(summary)!=len(avg)):
        print("there is some error")
    
    labels = 'Failed', 'Pass Class', 'II Class', 'I Class','Distinction'
    
 
    explode = (0.1, 0.0, 0.0, 0.0, 0.0)  # explode 1st slice
    colors=['#ff6361','#58508d','#ffa600','#bc5090','skyblue']
    plt.pie(summary, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
    c=c.split("_")
    plt.title(c[0]+" "+c[1]+" "+"Semester: "+c[2], bbox={'facecolor':'.91', 'pad':3})
    plt.axis('equal')
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return [figdata_png.decode('UTF-8'),summary]

#-----------------------------------------------------------------------------
def get_bar_chart(data,cnames):
    
    classes=[]
    for i in cnames:
        classes.append(i.replace("_"," "))
    # set width of bar
    barWidth = 0.25
    for i in range(len(data[1])):
        data[1][i]=data[1][i]+data[2][i]+data[3][i]+data[4][i]
    b1=data[0]
    b2=data[1]
    b3=data[4]
    
    r1 = np.arange(len(b1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
 
    # Make the plot
    plt.bar(r1, b1, color='#ed1123', width=barWidth, edgecolor='white', label='Failed')
    plt.bar(r2, b2, color='#f40087', width=barWidth, edgecolor='white', label='Passed')
    plt.bar(r3, b3, color='#751fff', width=barWidth, edgecolor='white', label='Distinction')
 
    # Add xticks on the middle of the group bars
    plt.xlabel('Classes', fontweight='bold')
    
    plt.xticks([r + barWidth for r in range(len(b1))], classes,rotation=40)
    plt.title("Semester Wise Results")
    # Create legend & Show graphic
    plt.legend()
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png.decode('UTF-8')
    

#--------------------------------------------------------------------------------
    
def plot_graph(classmark,regno):
    average=get_avg_marks(classmark['subject_marks'])
    roll_name=classmark['roll_name']
    xt=[]
    for i in range(len(roll_name[0])):
        if roll_name[0][i]==regno:
            break
    
    for j in range(len(average)):
        xt.append('Sub.')
        xt[j]=xt[j]+str(j+1)
 #   plt.style.use("greyscale")    
    plt.plot(range(len(average)),average,label="Class Average Marks")
    plt.plot(range(len(average)),classmark['student_marks'][i],label="Students Mark")
    plt.legend()
    plt.xticks(np.arange(len(average)), xt, rotation=30)
    plt.title("COMPARATIVE GRAPH FOR: "+roll_name[1][i])
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png.decode('UTF-8')
    #plt.show()  
    
#------------------------------------------------------------------------------
    
def get_class(regno):
            reg=int(regno)
            userstr=str(reg)
            if userstr[4]=='1':
                sclass='CME20'+userstr[:2]
            else:
                sclass='CMS20'+userstr[:2] 
            return sclass
#----------------------------------------------------------------------------------
    
def login(user,password):
    passdata=passdetails
    flag=0
    try: 
            sclass=get_class(user)
            for i in passdata[sclass]:
                   roll=int(i[0]) 
                   user=int(user)
                   if user==roll:
                        sname=i[1]
                        try:  
                            password=int(password)
                            if password==i[2]:
                                sclass=sclass[:3]+'_'+sclass[3:]
                                flag=1
                                return ([2,user,sname,sclass])
                            else:
                                return([-1])
                        except:
                            return ([-1])
            if(flag==0):
                return [-1]
    except:
            if user==admin and password==adminpass:
                    flag=1
                    return ([0])
            for i in passdata['teacher']:
                    k=SequenceMatcher(a=i[0],b=user).ratio()
                    if(k>=0.9):
                        if password==i[1]:
                                flag=1
                                return [1,user]
            if(flag==0):
                return [-1]
#------------------------------------------------------------------------------
def get_filenames():
    allfiles=os.listdir("D:\Paul Sem 6\Project\python files\excel")
    excels=[]
    names=[]
    for f in allfiles:
        if(f[-5:]==".xlsx" and f[0]!='~'):
            if (f[-10:-5]=="NAMES"):
                names.append(f[:-5])
            else:
                excels.append(f[:-5])
    return [names,excels]
    
#------------------------------------------------------------------------------
def get_allclass(excels):
    allclass={}
    for i in excels:
        if(i[0]=='~'):      # code to avoid opening any temporary excel files that will be 
            continue       # existing in the directory if any excel file is opened
        class_data={}
        filename="D:\\Paul Sem 6\\Project\\python files\\excel\\"+i+".xlsx";
        wb = open_workbook(filename)
        #name=i.split("_")
        # reading the excel file containing marks
        #print("Details of Class "+name[0]+" "+name[1]+" "+"Semester: "+name[2]+"\n\n")
        df=get_df(wb)
        # converting the excel file into a python list variable     
        roll_name=get_roll_name(df)
        # roll no and name of all students
        class_data['roll_name']=roll_name
     
        marks=get_marks(df)     #endmarks,attendance and cia marks: subjectwise
        subject_marks=marks[0] 
        #the list containing the final marks of all students subject wise
        class_data['subject_marks']=subject_marks    
    
        attendance=get_student_marks(marks[1])
        #list with attendance of each student
        class_data['attendance']=attendance
    
        cia=get_student_marks(marks[2])
        #cia marks of each student
        class_data['cia']=cia
    
        studentmark=get_student_marks(subject_marks)
        # student wise marks
        class_data['student_marks']=studentmark
    
        allclass[i]=class_data
    return allclass


#-------------------------------------------------------------------------------

def get_passdetails(names):
    passdetails={}
    passdetails['teacher']=[]
    for i in names:
        if(i[0]=='~'):      # code to avoid opening any temporary excel files that will be 
            continue       # existing in the directory if any excel file is opened

        filename="D:\\Paul Sem 6\\Project\\python files\\excel\\"+i+".xlsx";
        wb = open_workbook(filename)
        name=i.split("_")
        cname=name[0]+name[1]
        # reading the excel file containing marks
        df=get_df(wb)
        # converting the excel file into a python list variable 
        passdetails[cname]=[]    
        passwords=get_roll_name_pass(df)
        for i in passwords[0]:
            passdetails[cname].append(i)

        passdetails['teacher'].append(passwords[1])
    return passdetails
    
#------------------------------------------------------------------------------
def student_login(sclass,regno):
        graphs=[]
        for i in allclass.keys():
            try:
                if i.index(sclass)==0:
                    graphs.append(plot_graph(allclass[i],regno))
            except:
                        continue
        return graphs
#------------------------------------------------------------------------------
def get_student_graphs(regno):
    sclass=get_class(regno)
    sclass=sclass[:3]+'_'+sclass[3:]
    return (student_login(sclass,regno))
    
#-------------------------------------------------------------------------------
def admin_login():
        allsummary=[]
        plots=[]
        for i in allclass.keys():
            plot_summary=get_plot_summary(allclass[i]['student_marks'],i)
            allsummary.append(plot_summary[1]) 
            plots.append(plot_summary[0])
        markclass=get_student_marks(allsummary)
        g=get_bar_chart(markclass,classnames)
        plots.append(g)
        return plots

#------------------------------------------------------------------------------
def teacher_login(classname):
    classes=[]
    classsummary=[]
    class_sem=classname[:3]+"_"+classname[3:]
    plots=[]
    for i in allclass.keys():
        try:
            if i.index(class_sem)==0:
                plot_summary=get_plot_summary(allclass[i]['student_marks'],i)
                plots.append(plot_summary[0])
                classsummary.append(plot_summary[1]) 
                classes.append(i)
        except:
           continue
    summaryclass=get_student_marks(classsummary) #just doing transpose
    g=get_bar_chart(summaryclass,classes)
    plots.append(g)
    return plots
    
'''---------------------------------------------------------------------------
The program code starts here
'''
admin='admin'
adminpass='admin'

filenames=get_filenames()   # get the name of all files in the direcotry
passnames=filenames[0]          # saving fies with names into [assnames
classnames=filenames[1]         # saving files with marks to excels
    
allclass=get_allclass(classnames)   #saving all marks into dictionary variable
passdetails=get_passdetails(passnames) #saving all passwrords and usernames into passdetails
'''
logdata=login(username,p)
if logdata[0]==2:
    student_login(logdata[1],logdata[2])
  
to be done later

    * for teacher to get the list of studetnts with some criteria
    * attendance vs marks
    
'''
