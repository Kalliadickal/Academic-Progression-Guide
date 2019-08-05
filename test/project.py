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
from scipy.stats import skew

root=os.getcwd()

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
                m=-1
            try:
                m=int(m)
                if(m>=-1 and m<=200):
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
               if(marks[i][j-1]==-1):
                   mark.append(-1)
               else:
                    t=marks[i][j-4]+marks[i][j-5]  #code to find the total mark for each
                    m=marks[i][j]/t*100        # subject and then convert all obtained
                    m=round(m,2)             # marks to out of 100
                    mark.append(m)             
             #   except:
             #       mark.append(-1)
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
    avg=[]
    for j in a:
        count=0
        total=0
        for i in j:
            if i==-1:    #code to ensure that the absentees don't affect avg. marks
                count=count+1
            else:
                total=total+i
        m=total/(len(j)-count)
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
def get_fail_subjects(regno,classname):
    subj=' '
    for i in allclass[classname]['roll_marks']:
        if i[0]==regno:
            for j in range(len(i[1])):
                if i[1][j]<40 and i[1][j]!=-1:
                    subj=subj+(allclass[classname]['subjects'][j])+"\t\t   "                    
    return subj
#------------------------------------------------------------------------------
def get_absent_subjects(regno,classname):
    subj=''
    for i in allclass[classname]['roll_marks']:
        if i[0]==regno:
            for j in range(len(i[1])):
                if i[1][j]==-1:
                    subj=subj+(allclass[classname]['subjects'][j])+"\t\t   " 
    return subj
#------------------------------------------------------------------------------
def get_fail_absent(classname):
    flist=get_allfailed_list(allclass[classname]['roll_marks'])
    fails=flist[0]
    absents=flist[1]
    sfails=[]
    sabs=[]
    for i in fails:
        subj=get_fail_subjects(i,classname)
        sfails.append((i,get_names(i),subj))
    for i in absents:
        subj=get_absent_subjects(i,classname)
        sabs.append((i,get_names(i),subj))
    return [sfails,sabs]
#------------------------------------------------------------------------------

def get_failed_list(rollmark):
    # Funcition accepting marks of all students and printing the list of failed
    # students and returning a list of the failed students

    fail_list=[]
    absent=[]
    for i in rollmark:
        for j in i[1]:
                if j<40:
                    if(j==-1):
                        if i[0] not in absent:
                            absent.append(i[0])
                    else:   
                        if i[0] not in fail_list:
                            fail_list.append(i[0])
    for i in fail_list:
        if i in absent:
            absent.remove(i)
       
    return [fail_list,absent]
    

#----------------------------------------------------------------------------
def get_allfailed_list(rollmark):
    # Funcition accepting marks of all students and printing the list of failed
    # students and returning a list of the failed students

    fail_list=[]
    absent=[]
    for i in rollmark:
        for j in i[1]:
                if j<40:
                    if(j==-1):
                        if i[0] not in absent:
                            absent.append(i[0])
                    else:   
                        if i[0] not in fail_list:
                            fail_list.append(i[0])

    return [fail_list,absent]
    

#----------------------------------------------------------------------------
def get_plot_summary(rollmarks,c):
    distinct=0
    iclass=0
    iiclass=0
    pclass=0    
    fail_list=get_failed_list(rollmarks)
    fails=fail_list[0]
    absent=fail_list[1]

    #avg=get_avg_marks(studentmarks)
    for j in rollmarks:
        if j[0] in absent:
            continue
        elif j[0] in fails:
            continue
        else:
            i=sum(j[1])/len(j[1])
            if i>=80:
                distinct=distinct+1
            elif i>=60:
                iclass=iclass+1
            elif i>=50:
                iiclass=iiclass+1
            else:
                pclass=pclass+1
    failed=len(fails)
    absentees=len(absent)
    summary = [absentees,failed,pclass,iiclass,iclass,distinct]
    summarytemp=[absentees,failed,pclass,iiclass,iclass,distinct]
    labels = ['Absent','Failed', 'Pass Class', 'II Class', 'I Class','Distinction']
    explode = [0.02,0.02, 0.0, 0.0, 0.0, 0.0]
    colors=['red','#ff6361','#58508d','#ffa600','#bc5090','skyblue']
    
    pp=[]
    for k in range(len(summary)): # to remove any class values that are zero
        if summary[k]==0:
            pp.append(k)
    pp.sort(reverse=True)
    for i in pp:
            summary.pop(i)
            labels.pop(i)
            colors.pop(i)
            explode.pop(i)
           
    labels=tuple(labels)    
    explode=tuple(explode)
    plt.pie(summary, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=110)
    c=c.split("_")
    plt.title(c[0]+" Semester: "+c[1], bbox={'facecolor':'.91', 'pad':3})
    plt.axis('equal')
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return [figdata_png.decode('UTF-8'),summarytemp]
#------------------------------------------------------------------------------
def get_skewness(classname):
    smarks=allclass[classname]['subject_marks']
    skewdata=get_skew_data(smarks)
    sk=[]
    for i in skewdata:
        sk.append(skew(i))
    skdict={}
    count=0
    for i in allclass[classname]['subjects']:
        skdict[i]=round(sk[count],2)
        count=count+1
    return skdict

#-----------------------------------------------------------------------------
def get_skew_data(smarks):
    skdata=[]
    for j in smarks:
        a=[]
        for k in range(7):
            a.append(0)
        for i in j:
                if i<40:
                    if(i!=-1):
                        a[0]=a[0]+1
                elif i<50:
                    a[1]=a[1]+1
                elif i<60:
                    a[2]=a[2]+1
                elif i<70:
                    a[3]=a[3]+1
                elif i<80:
                    a[4]=a[4]+1
                elif i<90:
                    a[5]=a[5]+1
                elif i<100:
                    a[6]=a[6]+1
        skdata.append(a)
    return skdata
#-----------------------------------------------------------------------------
def get_skew_value(i):
    if i<-.7:
        return 'The mark distribution shows a very high difficuly level in terms of marks scored'
    elif i<-0.3:
        return 'The mark distribution shows a high difficuly level in terms of marks scored'
    elif i<0.3:
        return 'The mark distribution shows a moderate difficuly level in terms of marks scored'
    elif i<0.7:
        return 'The mark distribution shows the difficulty level is low in terms of marks scored'
    else:
        return 'The mark distribution shows a very low difficuly level in terms of marks scored'
#-----------------------------------------------------------------------------
def get_subject_dict(): # extracts semester wise subjects and marks from allclass
    allsubjects={}
    for c in allclass.keys():
        csem=c.split('_')
        sem=csem[1]
        if sem not in allsubjects.keys():
            allsubjects[sem]={}
        subj=allclass[c]['subjects']
        smarks=allclass[c]['subject_marks']
        classdict=get_subject_class(subj,smarks)
        for i in classdict.keys():
            if i not in allsubjects[sem].keys():
                allsubjects[sem][i]=[(classdict[i],c)]
            else:
                allsubjects[sem][i].append((classdict[i],c))
    return allsubjects
    
#----------------------------------------------------------------------------
def get_semsubjects():
    semdict=get_subject_dict()
    allsubj=[]
    allsems=[]
    for sems in semdict.keys():
        allsems.append(sems)
    allsems.sort()
    for i in allsems:
        semsubj=[]
        for j in semdict[i]:
            semsubj.append(j)
        allsubj.append(semsubj)
    print(allsubj)
    return allsubj 
#-----------------------------------------------------------------------------
def get_a_subject(subj,sem):
    semdict=get_subject_dict()
    slist=semdict[sem][subj]
    plots=[]
    for i in slist:
         a=plot_pie(i[1],i[0])
         b=printskew(subj,i[1])
         plots.append((a,b))
    return plots
#-----------------------------------------------------------------------------
def printskew(subj,clas):
    sdict=get_skewness(clas)
    skew=sdict[subj]
    skewstr="The subject skewness is "+str(skew)
    skval=get_skew_value(skew)
    skewstr=skewstr+".  "+skval
    return skewstr
#-----------------------------------------------------------------------------
def get_subject_charts(classname):
    subj=allclass[classname]['subjects']
    smarks=allclass[classname]['subject_marks']
    g=[]
    classdict=get_subject_class(subj,smarks)
    classkew=get_skewness(classname)
    skewstr={}
    #for i in classkew.keys():
    for i in classdict.keys():
        skval=classkew[i]
        skewstr[i]='The subject skewness is '+str(skval)
        cd=classdict[i]
        val=get_skew_value(skval)
        skew=skewstr[i]+'. '+val
        g.append((plot_pie(i,cd),skew))
    
    return g
       
#-----------------------------------------------------------------------------
def plot_pie(cl,summary):
    labels = ['Absent','Failed', 'Pass Class', 'II Class', 'I Class','Distinction']
    colors=['red','#ff6361','#58508d','#ffa600','#bc5090','skyblue']
    pp=[]
    for k in range(len(summary)):
        if summary[k]==0:
            pp.append(k)
    pp.sort(reverse=True)
    for i in pp:
            summary.pop(i)
            labels.pop(i)
            colors.pop(i)
    labels=tuple(labels)
    plt.pie(summary, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=110)
    plt.title(cl)
    #plt.axis('equal')
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png.decode('UTF-8')
#-----------------------------------------------------------------------------
def get_bar_chart(data,cnames):
    
    classes=[]
    for i in cnames:
        classes.append(i.replace("_"," "))
    # set width of bar
    barWidth = 0.25
    for i in range(len(data[1])):
        data[2][i]=data[2][i]+data[3][i]+data[4][i]+data[5][i]
    b1=data[1]
    b2=data[2]
    b3=data[5]
    
    r1 = np.arange(len(b1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
 
    # Make the plot
    plt.bar(r1, b1, color='#ed1123', width=barWidth, edgecolor='white', label='Failed')
    plt.bar(r2, b2, color='#f40087', width=barWidth, edgecolor='white', label='Passed')
    plt.bar(r3, b3, color='#751fff', width=barWidth, edgecolor='white', label='Distinction')
 
    # Add xticks on the middle of the group bars
    plt.xlabel('Classes', fontweight='bold')
    
    plt.xticks([r + barWidth for r in range(len(b1))], classes,rotation=20)
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

def plot_graph(classmark,regno,sclass):
    average=get_avg_marks(classmark['subject_marks'])
    roll_mark=classmark['roll_marks']
    sem=sclass[-1:]
    for i in range(len(roll_mark)):
        if roll_mark[i][0]==int(regno):
            ridx=i
            break
    
    xt=classmark['subjects']
 #   plt.style.use("greyscale")    
    plt.plot(range(len(average)),average,label="Class Average Marks")
    plt.plot(range(len(average)),classmark['roll_marks'][ridx][1],label="Students Mark")
    plt.legend()
    plt.xticks(np.arange(len(average)), xt, rotation=30)
    plt.title("COMPARATIVE GRAPH FOR SEMESTER "+sem)
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    #plt.show()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png.decode('UTF-8')
 
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
    allfiles=os.listdir(root+"\\app\\SHEETS")
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
def get_subjects(sheet):
    subjects=[]
    for j in range(len(sheet[0])):
        for i in range(len(sheet)):
            if(sheet[i][j]=='Subjects'):
               while(i<len(sheet)):
                       if(sheet[i][j]!=''):
                           subjects.append(sheet[i][j])
                       i=i+1
               subjects=subjects[1:]
               return subjects
#------------------------------------------------------------------------------
def get_allclass(excels):
    allclass={}
    for i in excels:
        if(i[0]=='~'):      # code to avoid opening any temporary excel files that will be 
            continue       # existing in the directory if any excel file is opened
        class_data={}
        filename=root+"\\app\\SHEETS\\"+i+".xlsx";
        wb = open_workbook(filename)
        #name=i.split("_")
        # reading the excel file containing marks
        #print("Details of Class "+name[0]+" "+name[1]+" "+"Semester: "+name[2]+"\n\n")
        df=get_df(wb)
        # converting the excel file into a python list variable     
        roll_name=get_roll_name(df)
        # roll no and name of all students
        class_data['roll_name']=roll_name
        rolls=roll_name[0]
        
        marks=get_marks(df)     #endmarks,attendance and cia marks: subjectwise
        subject_marks=marks[0] 
        #the list containing the final marks of all students subject wise
        class_data['subject_marks']=subject_marks    
    
        attendance=get_student_marks(marks[1])
        #list with attendance of each student
        class_data['attendance']=attendance
    
        ciamarks=get_student_marks(marks[2])

        cia=get_marks_tuple(ciamarks,rolls)
        #cia marks of each student
        class_data['cia']=cia
    
        studentmarks=get_student_marks(subject_marks)
        studentmark=get_marks_tuple(studentmarks,rolls)
        # student wise marks
        class_data['student_marks']=studentmarks
    
        class_data['roll_marks']=studentmark
        subjects=get_subjects(df)
        #to get all the subjects in that semester
        class_data['subjects']=subjects
        
        allclass[i]=class_data
    return allclass

#-------------------------------------------------------------------------------
def get_marks_tuple(marks,roll):
    roll_marks=[]
    for i in range(len(marks)):
        roll_marks.append((roll[i],marks[i]))
    return roll_marks
#-------------------------------------------------------------------------------
def get_subject_class(subjects,smarks): #function to return the mark distribution
    classd={}                       # of each subjects as a dictionary
    for i in range(len(smarks)):
        absent=0
        pclass=0
        fail=0
        iiclass=0
        iclass=0
        distinct=0
        for j in smarks[i]:
            if j>=80:
                distinct=distinct+1
            elif j>=60:
                iclass=iclass+1
            elif j>=50:
                iiclass=iiclass+1
            elif j>=40:
                pclass=pclass+1
            elif j==-1:
                absent=absent+1
            else:
                fail=fail+1
        classd[subjects[i]]=[absent,fail,pclass,iiclass,iclass,distinct]
    return classd
#-------------------------------------------------------------------------------

def get_passdetails(names):
    passdetails={}
    passdetails['teacher']=[]
    for i in names:
        if(i[0]=='~'):      # code to avoid opening any temporary excel files that will be 
            continue       # existing in the directory if any excel file is opened

        filename=root+"\\app\\SHEETS\\"+i+".xlsx";
        wb = open_workbook(filename)
        name=i.split("_")
        cname=name[0]
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

def get_all_classes():
    classes=[]
    for i in passdetails.keys():
        classes.append(i)
    classes.remove('teacher')
    return classes

#------------------------------------------------------------------------------
def student_login(sclass,regno):
        graphs=[]
        for i in allclass.keys():
            if sclass in i:
                    graphs.append(plot_graph(allclass[i],regno,i))
        return graphs
#------------------------------------------------------------------------------
def get_student_graphs(regno):
    sclass=get_class(regno)
    return (student_login(sclass,regno))
    
#-------------------------------------------------------------------------------
def transpose_list(data):
    newdata=[]
    for i in range(len(data[0])):
        nd=[]
        for j in range(len(data)):
            nd.append(data[j][i])
        newdata.append(nd)
    return newdata
#------------------------------------------------------------------------------
def admin_login():
        allsummary=[]
        plots=[]
        for i in allclass.keys():
            plot_summary=get_plot_summary(allclass[i]['roll_marks'],i)
            allsummary.append(plot_summary[1]) 
            plots.append((plot_summary[0],i))
        markclass=transpose_list(allsummary)
        g=get_bar_chart(markclass,classnames)
        plots.append(g)
        return plots
#------------------------------------------------------------------------------
def get_progression_graph(regno):
    regno=int(regno)
    sclass=get_class(regno)
    classavg=[]
    student=[]
    pgdict=get_class_progression(sclass,regno)
    for i in range(len(pgdict.keys())):
        k=str(i+1)
        student.append(pgdict[k][0])
        classavg.append(pgdict[k][1])
    splot=get_avg_marks(student)
    cplot=get_avg_marks(classavg)
    sems=[]
    for i in range(len(cplot)):
        sems.append('Semester '+str(i+1))
    plt.plot(range(len(cplot)),cplot,label="Class Average Marks",color='blue')
    plt.plot(range(len(splot)),splot,label="Students Mark",color='green')
    plt.legend()
    plt.xticks(np.arange(len(splot)), sems, rotation=15)
    plt.title("Comparative Student Progression Graph")
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    #plt.show()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    #plt.show()
    return figdata_png.decode('UTF-8')

#------------------------------------------------------------------------------
def get_class_progression(classname,regno):
    student_classavg={}
    sm=[]
    for i in allclass.keys():
        if classname in i:
                semavg=get_avg_marks(allclass[i]['subject_marks'])
                for j in allclass[i]['roll_marks']:
                    if j[0]==regno:
                        sm=j[1]
                sem=i[-1:]
                student_classavg[sem]=[sm,semavg]
    return student_classavg

#------------------------------------------------------------------------------
def get_allclass_progression():
    classavg=get_allclass_avgs()
    sems=0
    for i in classavg.values():
        if len(i)>sems:
            sems=len(i)
    xt=[]
    for i in range(sems):
        semname='Semester '+str((i+1))
        xt.append(semname)
 #   plt.style.use("greyscale")    
    
    for i in classavg.keys():
        plt.plot(range(len(classavg[i])),classavg[i],label=i)
    plt.legend()
    plt.xticks(np.arange(sems), xt)
    plt.title("Class Progression Chart for All Classes")
    figfile = BytesIO()
    plt.savefig(figfile,format='png')
    plt.clf()
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    return figdata_png.decode('UTF-8')

#------------------------------------------------------------------------------
def get_allclass_avgs():
    classavg={}
    for i in allclass.keys():
        semavg=get_avg_marks(allclass[i]['subject_marks'])
        classavg[i]=semavg
    classes=get_all_classes()
    classdict={}
    for i in classes:
        count=1
        clist=[]
        while count<=6:
            try:
                cname=i+'_'+str(count)
                clist.append(classavg[cname])
                count=count+1
            except:
                break
        classdict[i]=clist
    semwise={}
    for i in classdict.keys():
        cavg=get_avg_marks(classdict[i])
        semwise[i]=cavg
    return semwise
#------------------------------------------------------------------------------
def teacher_login(classname):
    classes=[]
    classsummary=[]
    plots=[]
    for i in allclass.keys():
        if classname in i:
                plot_summary=get_plot_summary(allclass[i]['roll_marks'],i)
                plots.append((plot_summary[0],i))
                classsummary.append(plot_summary[1]) 
                classes.append(i)
    summaryclass=get_student_marks(classsummary) #just doing transpose
    g=get_bar_chart(summaryclass,classes)
    plots.append(g)
    return plots

#------------------------------------------------------------------------------
def get_names(regno):
    sname=[]
    b=[]
    a=[]
    b=get_class(regno)
    a=passdetails[b]
    for i in a:
        if i[0]==int(regno):
            sname=i[1]
            return sname
    return -1

#------------------------------------------------------------------------------
def get_corr(classname):
    atm=allclass[classname]['attendance']
    sm=allclass[classname]['student_marks']
    atmavg=get_avg_marks(atm)
    smavg=get_avg_marks(sm)
    atcorr=np.corrcoef(atmavg,smavg)
    atcorr=atcorr[0,1]
    atcorr=round(atcorr,2)
    atstring='The attendance-marks correlation is '+str(atcorr)
    if atcorr < -0.7:
        atstring=atstring+' ,there is strong negative correlatoin between attendance and marks'
    elif atcorr < -.03:
        atstring=atstring+' ,there is moderate negative correlatoin between attendance and marks'
    elif atcorr < -0.1:
        atstring=atstring+' ,there is weak negative correlatoin between attendance and marks'
    elif atcorr < 0.1:
        atstring=atstring+' ,there is no correlatoin between attendance and marks'
    elif atcorr <0.3:
        atstring=atstring+' ,there is weak positive correlatoin between attendance and marks'
    elif atcorr < 0.7:
        atstring=atstring+' ,there is moderate positive correlatoin between attendance and marks'
    else:
        atstring=atstring+' ,there is strong positive correlatoin between attendance and marks'
    return atstring

#-----------------------------------------------------------------------------------------------
def reload():
    global filenames,passnames,classnames,allclass,passdetails
    filenames=get_filenames()   # get the name of all files in the direcotry
    passnames=filenames[0]          # saving fies with names into [assnames
    classnames=filenames[1]         # saving files with marks to excels
        
    allclass=get_allclass(classnames)   #saving all marks into dictionary variable
    passdetails=get_passdetails(passnames) #saving all passwrords and usernames into passdetails
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
Project Features

    * semsester wise mark of each class in one graph for admin (done)

    * for teacher to get the list of studetnts with some criteria
    * attendance vs marks  (done)
    *  Credit
    *  Quality control
    
'''