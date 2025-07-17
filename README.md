# 🚀 คู่มือการตั้งค่าโปรเจกต์ Django Quiz

เอกสารสรุปขั้นตอนการตั้งค่าโปรเจกต์และการทดสอบคำสั่งต่างๆ สำหรับงาน HW-03-04 (Django Model) และ Wk02 (HttpRequest/HttpResponse) ร่วมกัน

---

## 📝 สิ่งที่ควรรู้และข้อควรระวัง

- **การรวมงาน**: โปรเจกต์นี้เป็นการทำงานควบคู่กันระหว่าง 2 Assignment
- **ขอบเขตงาน**: การทำงานทั้งหมด เช่น การสร้าง `models`, `migrations`, และ `fixtures` จะทำอยู่ภายในแอป `quiz` เท่านั้น ส่วนของแอปหลัก `mysite` จะไม่มีการแก้ไขใดๆ
- **`.gitignore`**: **สำคัญมาก!** หลังจาก `clone` โปรเจกต์จาก Github แล้ว ให้ลบไฟล์ `.gitignore` ทิ้งทันที เพราะไฟล์นี้ถูกตั้งค่าให้ละเว้นไฟล์สำคัญบางอย่างสำหรับการส่งงาน
- **`.venv`**: โฟลเดอร์ `.venv` จะไม่ถูกเก็บใน Github เพื่อประหยัดพื้นที่และทำให้โปรเจกต์เบาลง เนื่องจากเราสามารถสร้างขึ้นมาใหม่และติดตั้งไลบรารีทั้งหมดได้จากไฟล์ `requirements.txt`

---

## 🏗️ โครงสร้างโปรเจกต์ (Project Structure)

```
mysite/
├── .venv/
├── mysite/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── quiz/
│   ├── __pycache__/
│   ├── fixtures/
│   │   └── quizzes-1-68.json
│   ├── migrations/
│   │   ├── __pycache__/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
└── requirements.txt
```


```
---

## ⚙️ 1. การตั้งค่าสภาพแวดล้อม (Environment Setup)

### 1.1 สร้างและเปิดใช้งาน Virtual Environment
**สร้างสภาพแวดล้อม (ทำครั้งแรก)**
```powershell
py -m venv .venv
```

**เปิดใช้งาน (ทำทุกครั้งที่เปิด Terminal ใหม่)**
```powershell
.\venv\Scripts\activate
```

### 1.2 ติดตั้งไลบรารีที่จำเป็น
```powershell
pip install -r requirements.txt
```

---

## 🗃️ 2. การเตรียมโปรเจกต์และฐานข้อมูล
### 2.1 เข้าไปยังโฟลเดอร์โปรเจกต์
```powershell
cd mysite
```

### 2.2 สร้างโมเดล (Models)
กำหนดโครงสร้างฐานข้อมูลในไฟล์ `quiz/models.py`
```python
from django.db import models

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)
    published_date = models.DateTimeField('date published')

    def __str__(self):
        return self.text

class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
```

### 2.3 สร้างและอัปเดตฐานข้อมูล (Migrations)
**Makemigratons คือ สร้าง "พิมพ์เขียว" หรือชุดคำสั่งสำหรับการเปลี่ยนแปลงโครงสร้างฐานข้อมูล ตามที่คุณได้กำหนดไว้ใน models.py**
```powershell
py manage.py makemigrations
```

**Migrate คือ การสร้างตารางในฐานข้อมูลและนำ "พิมพ์เขียว" จาก Make ไปสร้างหรือปรับปรุงตารางจริงๆ ในไฟล์ฐานข้อมูล (db.sqlite3)**
```powershell
py manage.py migrate
```

### 2.4 โหลดข้อมูลเริ่มต้น (Fixtures)
**คือ "ที่เก็บข้อมูลสำเร็จรูป" ที่เป็นมาตรฐานของ Django สำหรับใช้โหลดเข้าฐานข้อมูล และเป็นการเตรียมข้อมูลเริ่มต้นสำหรับโปรเจกต์**
1. สร้างโฟลเดอร์ `fixtures` ภายในแอป `quiz`
2. นำไฟล์ข้อมูล [quizzes-1-68.json](https://drive.google.com/file/d/14RlkC3Lwbmp2LE27p7dQPyFWQDF_3cZ2/view) ไปไว้ในโฟลเดอร์นั้น
3. รันคำสั่งเพื่อโหลดข้อมูล
```powershell
py manage.py loaddata quizzes-1-68.json
```

---

## 🧪 3. การทดสอบด้วย Django Shell

### 3.1 เข้าสู่ Shell และ Import
**Django Shell**
```powershell
py manage.py shell
```

**จะทำเข้าหน้าต่าง Shell ให้เรา Import สิ่งที่จำเป็น (ทำครั้งเดียวต่อ 1 session)**
```python
from quiz.models import Question, Choice
from django.utils import timezone
from datetime import datetime
```

### 3.2 รันคำสั่ง Query ตามโจทย์
**1. ค้นหาคำถามทั้งหมด**
```python
all_questions = Question.objects.all()
for index, q in enumerate(all_questions, 1):
    print(f"{index}. {q}")
```

**2. ค้นหาคำถามที่มีคำว่า "AI"**
```python
ai_questions = Question.objects.filter(text__icontains='AI')
for index, q in enumerate(ai_questions, 1):
    print(f"{index}. {q}")
```

**3. ค้นหาคำถามที่เปิดหลังวันที่ 1 ก.ค. 2565**
```python
aware_date = timezone.make_aware(datetime(2022, 7, 1))
questions = Question.objects.filter(published_date__gt=aware_date)
for index, q in enumerate(questions, 1):
    print(f"{index}. {q}")
```

**4. ค้นหาคำถามที่มี id เป็น 13**
```python
question_13 = Question.objects.get(id=13)
print(question_13)
```

**5. ค้นหาตัวเลือกทั้งหมดของคำถาม id 16**
```python
choices_for_question_16 = Choice.objects.filter(question__id=16)
for index, q in enumerate(choices_for_question_16, 1):
    print(f"{index}. {q}")
```

**6. แสดงคำถามและตัวเลือกที่มีคำว่า "Tailwind"**
```python
tailwind_questions = Question.objects.filter(text__icontains='Tailwind')
for index, q in enumerate(tailwind_questions, 1):
    print(f"{index}. Question: {q.text}")
    for choice in q.choice_set.all():
        print(f"   - {choice.text}")
