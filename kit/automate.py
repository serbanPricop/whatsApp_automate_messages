import pywhatkit as pwk
import requests
from bs4 import BeautifulSoup
import time, re

payload = {
    'email' : 'email',
    'password': 'password'
}

message = "Bună ziua,\n\nVă reamintim că astăzi, ora {}, Academia realizează o noua sesiune Live la care vă așteptăm cu drag să participați.Mai jos, vă atașăm ID-ul și parola aferentă sesiunii de pe platforma Zoom.\n\nMeeting link: {} \nID: {}\nPasscode: {} \n\nO zi frumoasă!"

ana_link = 'meeting_link'
ana_meeting_id = 'meeting_id'
ana_pass = 'pass'

andrei_link = 'meeting_link'
andrei_meeting_id = 'meeting_id'
andrei_pass = 'pass'

serban_link = 'meeting_link'
serban_meeting_id = 'meeting_id'
serban_pass = 'pass'

def getPhoneNumber(users_hrefs):
            users_phone_number = []
            for user_href in users_hrefs:
                user_page = s.get(user_href)
                html = BeautifulSoup(user_page.content,'html.parser')
                user_page_text = html.find('input',{'name':'telefon_parinte_1'})
                users_phones_numbers = user_page_text.get('value')
                users_phone_number.append(users_phones_numbers)
            users_phone_number = list(dict.fromkeys(users_phone_number))
            return users_phone_number

def sendMessage(students_phones,link,meeting_id,password):
    for student in students_phones:
        number_with_prefix = student.split('0',1)[1]
        try:
            print(message.format(teacher_and_hours[0],link,meeting_id,password))
            # pwk.sendwhatmsg_instantly(phone_no=f"+40{number_with_prefix}",message= message.format(teacher_and_hours[0],ana_link,ana_meeting_id,ana_pass),tab_close=True)
            file.writelines('Message sent to '+number_with_prefix +'\n')
            # time.sleep(60)                
        except:
            file.write('Message not sent to '+number_with_prefix +'\n')

file = open('raport.txt','w')

with requests.Session() as s:
    p = s.post('login path',data=payload)
    
    page = s.get('classes path')
    soup = BeautifulSoup(page.content,'html.parser')
    result = soup.find_all('tr',{'class':'table-primary'})

    user_details = []
    tds = []
    anchors = []
    hours = []
    i = 0
    
    for td in result:
        tds.extend(td.find_all('a')[::2])

    for td in tds:
        anchors.append(td.get('href'))
    
    for anchor in anchors:
        classes_ongoining = s.get(anchor)
        html = BeautifulSoup(classes_ongoining.content,'html.parser')
        user_anchors = html.select('td a')[::4]
        user_hours = html.select('span',{'class':'text'})
        teachers = html.select('option[selected]')[2:4]

        users_hrefs = []

        for user_anchor in user_anchors:
            users_hrefs.append(user_anchor.get('href'))

        user_details.append([([teacher.text for teacher in teachers]),getPhoneNumber(users_hrefs)])
        hours = []
        students_phones = user_details[i][1]
        teacher_and_hours = user_details[i][0]

        match teacher_and_hours[1]:
            case 'Ana':
                sendMessage(students_phones,ana_link,ana_meeting_id,ana_pass)
            case 'Andrei':
                sendMessage(students_phones,andrei_link,andrei_meeting_id,andrei_pass)
            case 'Serban P':
                sendMessage(students_phones,serban_link,serban_meeting_id,serban_pass)
                
        i+=1
