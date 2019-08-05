import os
from flask import Flask, render_template, redirect, url_for, request, session, abort, flash, send_from_directory
from werkzeug import secure_filename
from app import app
import project as pr
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
username=''
password=''

@app.route('/')
def index():
    logdata=pr.login(username,password)
    if not session.get('logged_in'):
        return render_template('login.html')
        
    elif logdata[0]==2:
            session['logged_in'] = True
            return render_template('index2.html',user=username)
        
    elif logdata[0]==1:
            session['logged_in'] = True
        
            return render_template("aboutteacher.html",user=username)
    else:
        pr.reload();
        classlist=pr.get_all_classes();
    		
    return render_template("aboutadminmain.html",list=classlist,user=username)
@app.route('/index1')
def index1():
    return render_template("index1.html",user=username)

@app.route('/index2')
def index2():
    return render_template("index2.html",user=username)

@app.route('/aboutadminmain')
def aboutadminmain():
    pr.reload();
    classlist=pr.get_all_classes();
    return render_template("aboutadminmain.html",list=classlist)

@app.route('/aboutteacher')
def aboutteacher():
    pr.reload();
    return render_template("aboutteacher.html")

@app.route('/about')
def about():
    pr.reload() 
    return render_template("about.html")

@app.route('/about1')
def about1():
    t=pr.teacher_login(username)
    return render_template("about1.html",graph=t,user=username)

@app.route('/about2')
def about2():
    s=pr.get_student_graphs(username)
    s1=pr.get_progression_graph(username)
    s.append(s1)
    return render_template("about2.html",graph=s,name=name2,class1=class2)

@app.route('/updatedata', methods = ['GET', 'POST'])
def updatedata():
     if request.method == 'POST':
         return render_template("about.html")
   
@app.route('/overall', methods = ['GET', 'POST'])
def overall():
     if request.method == 'POST':
         a=pr.admin_login()
         return render_template("overall.html",graph=a)
     
@app.route('/classwise', methods = ['GET', 'POST'])
def classwise():
     if request.method == 'POST':
         ca=request.form['classno'];
         classgraph=pr.teacher_login(ca)
         return render_template("classreport.html",graph=classgraph,user=ca)
     
@app.route('/class1', methods = ['GET', 'POST'])
def classwise1():
     if request.method == 'POST':
         classgraph=pr.teacher_login(username)
         return render_template("about1.html",graph=classgraph,user=username)

@app.route('/studentwise', methods = ['GET', 'POST'])
def studentwise():
     if request.method == 'POST':
         ca=request.form['regno'];
         try:
             studentgraph=pr.get_student_graphs(ca)
             sname=pr.get_names(ca)
             
             b=pr.get_class(ca)
             s1=pr.get_progression_graph(ca)
             studentgraph.append(s1)
             return render_template("studentreport.html",graph=studentgraph,name=sname,class1=b)
         except:
             classlist=pr.get_all_classes();
             return render_template("aboutadminmain.html",list=classlist)
         
@app.route('/student1', methods = ['GET', 'POST'])
def student1():
     if request.method == 'POST':
         ca=request.form['regno'];
         try:
             studentgraph=pr.get_student_graphs(ca)
             sname=pr.get_names(ca)
             
             b=pr.get_class(ca)
             s1=pr.get_progression_graph(ca)
             studentgraph.append(s1)
             return render_template("studentreport1.html",graph=studentgraph,name=sname,class1=b)
         except:
             
             return render_template("aboutteacher.html")
     
@app.route('/eachclass', methods = ['GET', 'POST'])
def eachclass():
   if request.method == 'POST':
       semgraph=pr.get_allclass_progression()
       return render_template("semwiseclass.html",graph=semgraph)


@app.route('/eachclasssub', methods = ['GET', 'POST'])
def eachclasssub():
   if request.method == 'POST':
       subname=pr.get_semsubjects()
       return render_template("subjectanalysis.html",slist=subname)
       
@app.route('/subwise', methods = ['GET', 'POST'])
def subwise():
   if request.method == 'POST':
           try:
               subname1=request.form["subjectname"]
               subname=pr.get_a_subject(subname1,subname1[3])
               return render_template("subjectanalysis1.html",graph=subname,sub=subname1,sem=subname1[3]) 
           except:
               subname=pr.get_semsubjects()
               return render_template("subjectanalysis.html",slist=subname)

@app.route('/semwise', methods = ['GET', 'POST'])
def semwise():
   if request.method == 'POST':
       cname=request.form["subject"]
       sgraphs=pr.get_subject_charts(cname)
       return render_template("classsem.html",subjects=sgraphs,users=cname)
  
@app.route('/semwise1', methods = ['GET', 'POST'])
def semwise1():
   if request.method == 'POST':
       cname=request.form["subject"]
       sgraphs=pr.get_subject_charts(cname)
       return render_template("classsem1.html",subjects=sgraphs,users=cname)
   
@app.route('/faillist', methods = ['GET', 'POST'])
def faillist():
   if request.method == 'POST':
       cname=request.form["faillist"]
       flist=pr.get_fail_absent(cname)
       return render_template("faillist.html",faillist=flist,users=cname)
  
@app.route('/faillist1', methods = ['GET', 'POST'])
def faillist1():
   if request.method == 'POST':
       cname=request.form["faillist"]
       flist=pr.get_fail_absent(cname)
       return render_template("faillist1.html",faillist=flist,users=cname)
   
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    target = os.path.join(APP_ROOT, 'SHEETS/')
    print(target)
    	
    for file in request.files.getlist("file"):
    		print(file)
    		filename=file.filename
    		destination = "/".join([target, filename])
    		print(destination)
    		file.save(destination)
    pr.reload()
    return render_template("about.html")
@app.route('/remove', methods = ['GET', 'POST'])
def remove_file():
    target = os.path.join(APP_ROOT, 'SHEETS/')
    print(target)
    	
    for file in request.files.getlist("file1"):
    		print(file)
    		filename=file.filename
    		destination = "/".join([target, filename])
    		print(destination)
    		file.save(destination)
    		os.remove(destination)
    
    return render_template("about.html")
	
@app.route('/contact')
def contact():
    return render_template("contact.html")
@app.route('/contact1')
def contact1():
    return render_template("contact1.html")
@app.route('/contact2')
def contact2():
    return render_template("contact2.html")


@app.route('/login', methods=['GET', 'POST'])
def login1():
    error = None
    global username
    global name2
    global class2
    username=request.form['username']
    password=request.form['password']
    logdata=pr.login(username,password)
    
    if request.method == 'POST':
        if logdata[0]==2:
            name2=logdata[2]
            class2=logdata[3]
            session['logged_in'] = True
            return render_template('index2.html',user=username,name=name2,class1=class2)
        elif logdata[0]==0:
            session['logged_in'] = True
            pr.reload();
            classlist=pr.get_all_classes();
            return render_template('aboutadminmain.html',user=username,list=classlist)
        elif logdata[0]==1:
            session['logged_in'] = True
            return render_template("aboutteacher.html",user=username)
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))
