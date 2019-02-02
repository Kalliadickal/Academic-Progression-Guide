# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:15:09 2019

@author: admin
"""
from flask import Flask, render_template
import project

app = Flask(__name__)


@app.route("/")
def template_test():
    filenames=project.get_filenames()   # get the name of all files in the direcotry
#   passnames=project.filenames[0]          # saving fies with names into [assnames
    classnames=filenames[1]         # saving files with marks to excels  
    #g=project.get_student_graphs(1740123)
    t=project.teacher_login('CMS2017')
    a=project.admin_login()

    return render_template('template.html', my_list=classnames,graphs=t+a)


if __name__ == '__main__':
    app.run(debug=True)

'''    
    allclass=project.get_allclass(classnames)   #saving all marks into dictionary variable
 #   passdetails=project.get_passdetails(passnames) #saving all passwrords and usernames into passdetails

    print("\nAcademic Progression Guide\n\nThe available details are : \n")
    for i in allclass.keys():
        name=i.split("_")
        print("Class: "+name[0]+name[1]+" Semester: "+name[2])
''' 