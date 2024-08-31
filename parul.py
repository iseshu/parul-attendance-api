import json
import requests
from bs4 import BeautifulSoup
import random, string


class Parul():
    def __init__(self):
        req = requests.get("https://ums.paruluniversity.ac.in/Login.aspx",allow_redirects=True)
        soup = BeautifulSoup(req.text, 'html.parser')
        self.viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
        self.viewstategenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        self.cookies = req.cookies
        res = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase+string.digits, k=24))
        self.res = "ASP.NET_SessionId="+res

    def login(self,email,password):
            self.EMAIL = email
            data = {
                '__LASTFOCUS': '',
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': self.viewstate,
                '__VIEWSTATEGENERATOR': self.viewstategenerator,
                '__VIEWSTATEENCRYPTED': '',
                'rblRole':'Student',
                'hfWidth': '1042',
                'hfHeight': '714',
                'hfLoginMethod': 'Password',
                'txtUsername': email,
                'txtPassword': password,
                'btnLogin': 'Login',
            }
            req = requests.post("https://ums.paruluniversity.ac.in/Login.aspx", data=data, cookies=self.cookies, allow_redirects=True)

    def get_me(self):
            req = requests.get("https://ums.paruluniversity.ac.in/StudentPanel/STU_Student/STU_Student_ProfileView.aspx", cookies=self.cookies)
            soup = BeautifulSoup(req.text, 'html.parser')
            name = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblStudentLCName"}).text
            status = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblStudentStatusID"}).text
            course = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblCourseName"}).text
            admin_no = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblEnrollmentNo"}).text
            div = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblCurrentDivision"}).text
            bach_no = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblCurrentLabBatchNo"}).text
            roll_no = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblCurrentRollNo"}).text
            mobile_no = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblPhoneStudent1"}).text
            email = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_ucStudentInfoCompact_lblEmail"}).text
            gender = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblGender"}).text
            Mother_Tongue = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherTongueLanguageID"}).text
            Date_of_Birth = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblBirthDate"}).text
            AadharCard_No = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblAadhaarCardNo"}).text
            Place_of_Birth = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblBirthPlace"}).text
            Religion = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblReligionID"}).text
            Nationality = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblNationalityCountryID"}).text
            Father_Name = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblFatherName_XXXXX"}).text
            Mother_Name = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblMotherName"}).text
            Guardian_Name = soup.find("span",{"id":"ctl00_cphPageContent_ucStudentInfoAdmission_lblGuardianName"}).text
            return name, status, course, admin_no, div, admin_no, div, bach_no, roll_no, email, gender, Mother_Tongue, Date_of_Birth, AadharCard_No, Place_of_Birth, Religion, Nationality, Father_Name, Mother_Name, Guardian_Name

    def get_attendance(self):
        url = "https://ums.paruluniversity.ac.in/StudentPanel/TTM_Attendance/TTM_Attendance_StudentAttendance.aspx"
        req = requests.get(url, cookies=self.cookies)
        soup = BeautifulSoup(req.text, 'html.parser')
        name = soup.find("span",{"id":"ctl00_lblCurrentUsername"}).text
        total_slots = soup.find("span",{"id":"ctl00_cphPageContent_lblTotalLectureLabCount"}).text
        present_slots = soup.find("span",{"id":"ctl00_cphPageContent_lblPresentLectureLabCount"}).text
        image = soup.find("img",{"id":"ctl00_imgCurrentUserPhoto"})['src']
        image = image if image.startswith("data:image") else "https://ums.paruluniversity.ac.in/Images/Faculty_NoImg.jpeg"
        absent_slots = soup.find("span",{"id":"ctl00_cphPageContent_lblAbsentLectureLabCount"}).text
        percent_age = soup.find("span",{"id":"ctl00_cphPageContent_lblPresentPCTCount"}).text
        table = soup.find("table",{"id":"tblAttendance"})
        subjects = []
        for row in table.findAll("tr",{"class":"odd gradeX"}):
            tds = row.findAll("td")
            no = tds[0].text.strip()
            subject_code = tds[1].text.strip().split(" - ")[0]
            subject_name = tds[1].text.strip().split(" - ")[1]
            t_ype = tds[2].text.strip()
            total = int(tds[3].text.strip())
            present = int(tds[4].text.strip())
            absent = int(tds[5].text.strip())
            percent = present/total*100
            subjects.append({"no":no,"subject_code":subject_code,"subject_name":subject_name,"type":t_ype,"total":total,"present":present,"absent":absent,"percent":percent})
        
        return {"total_slots":total_slots,"image":image,"present_slots":present_slots,"absent_slots":absent_slots,"percent_age":percent_age,"name":name,"subjects":subjects}
    def get_timetable(self):
        pass
