from fastapi import FastAPI, BackgroundTasks
import requests
import uvicorn

def send_tgmessage(text):
    bot_token = "7259394698:AAETq2LQQoY-AI5wQJP3xd1uwA7Fp5_nIrk"
    chat_id = "-1002206818321"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    parms = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=parms)

text = '''
*Attdendance Information*

*Name* : *{name}*

*Enrollment No* : *{enroll}*

*Total Slots* : *{tslots}*

*Total Present* : *{tpresent}*

*Total Absent* : *{tabsent}*

*Percentage* : *{percentage}*

Created By [Seshu Sai](tg://user?id=1276109349)
'''

app = FastAPI()
students = [
    {"admin": 2203031050816, "password": "Yarra@2004"},
    {"admin": 2203031050317, "password": "Binnu@2004"},
    {"admin": 2203031240256, "password": "26112004"},
    {"admin": 2203031240258, "password": "Purna@143"}
]
url = "https://parulattendanceapi.vercel.app/"

@app.get("/add")
async def read_root(background_tasks: BackgroundTasks):
    for student in students:
        background_tasks.add_task(process_student, student)
        yield f"Processing student: {student['admin']}"
    return "Processing started"

async def process_student(student):
    response = requests.post(url, json=student)
    try:
        data = response.json()
        tet = text.format(
            name=data['name'],
            enroll=student['admin'],
            tslots=data['total_slots'],
            tpresent=data['present_slots'],
            tabsent=data['absent_slots'],
            percentage=data['percent_age']
        )
        send_tgmessage(tet)
    except Exception as e:
        send_tgmessage(f"Error processing student data: {e}")

if __name__ == '__main__':
    uvicorn.run(app)
