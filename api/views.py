from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
from .models import *

#@csrf_exempt
#def hello(request):
#    if 'payload' in request.POST:
#        payload = json.loads(request.POST['payload'])
#        git_url = payload['repository']['clone_url']

        #Homeworks 폴더 안에서 clone 하고 싶어서 -> 실패, 이렇게 해도 git clone은 베이스 프로젝트에서 실행됨.
#        command = 'cd Homeworks'
#        command = command.split()
#        subprocess.call(command, shell=True)

#        command = 'git clone ' + str(git_url)
#        command = command.split()
#        subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

        #기존의 repository name과 중복될 경우 (clone 에러 발생할 경우) pull 하도록 하기.



#    f = open('Testcases/Inputs.txt', "r")
#    inputs = f.readlines() #read Inputs
#    f = open('Testcases/Outputs.txt', "r")
#    outputs = f.readlines() #read Outputs


#    for input, output in zip(inputs, outputs)
#        result = subprocess.check_output(["python", "Homeworks/"+payload['repository']['git_url'], input]) #채점 대상 파일은 push 알람에서 주는 정보에 따라 달라지도록.
#        result = int(result.decode('utf-8'))
#        if result is output:
#            final_result = "pass"
#        else:
#            final_result = "fail"
#            break

#    return render(request, "push.html", {"result": result})


@csrf_exempt
def createhw(request):
    if 'payload' in request.POST:
        payload = json.loads(request.POST['payload'])
        action = payload['action']
        hwname = payload['repository']['name']
        organization = payload['repository']['owner']['login']
       
        if '-' in hwname: #학생이 hw을 accept해서 rp가 create되었을 때
            words = hwname.split("-")

            if action=="created":
                if not Classroom_student.objects.filter(classroom=organization).filter(student=words[1]).exists():
                    cs = Classroom_student(classroom=organization, student=words[1])
                    cs.save()
                    if not Homework_student.objects.filter(homework=words[0].upper()).filter(student=words[1]).exists():
                        hs = Homework_student(homework=words[0].upper(), student=words[1])
                        hs.save()

            elif action=="deleted":
                if Homework_student.objects.filter(homework=words[0].upper()).filter(student=words[1]).exists():
                    hs = Homework_student(homework=words[0].upper(), student=words[1])
                    hs.delete()

 
        else: #교수님이 문제를 내서 rp가 create 되었을때 / 교수님께 HW name에 절대 - 를 포함해서는 안된다고 안내해야함 - 별로다...

 
            if action=="created":
                if Classrooms.objects.filter(organization=organization).exists():
                    c = Classrooms.objects.get(organization=organization)
                else:
                    c = Classrooms(organization=organization)
                    c.save()
                h = Homeworks(classroom=c, hw_name=hwname)
                h.save()

            elif action=="deleted":
                if Classrooms.objects.filter(organization=organization).exists():
                    if Homeworks.objects.filter(hw_name=hwname).exists():
                        h = Homeworks.objects.get(hw_name=hwname)
                        h.delete()

    hws = Homeworks.objects.all()
    return render(request, "hwlist.html", {'hws':hws})
            

def hwlist(request):
        my_hws = Homework_student.objects.get(student="jhj1116")
        return render(request, "myhw.html", {'hws':my_hws})
