from fastapi import FastAPI
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from database import students, attendance_records, food_orders

app = FastAPI(title="Smart University Campus Backend")

# ------------------------------------------------
# EMAIL NOTIFICATION HELPER
# ------------------------------------------------
def trigger_email(receiver_email, email_subject, email_body):
    mail_payload = Mail(
        from_email=os.getenv("DEVELOPER_EMAIL"),
        to_emails=receiver_email,
        subject=email_subject,
        plain_text_content=email_body
    )

    try:
        sg_client = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        result = sg_client.send(mail_payload)
        print("Mail status:", result.status_code)
    except Exception as err:
        print("Mail failed:", err)


# ------------------------------------------------
# STUDENT REGISTRATION
# ------------------------------------------------
@app.post("/add_student")
def add_student(student_name: str, roll_number: str, student_email: str):
    student_entry = {
        "name": student_name,
        "roll": roll_number,
        "email": student_email
    }
    students.append(student_entry)
    return {"message": "Student registration completed"}


# ------------------------------------------------
# ATTENDANCE HANDLING
# ------------------------------------------------
@app.post("/mark_attendance")
def mark_attendance(roll_number: str, status: str, student_email: str):
    attendance_entry = {
        "roll": roll_number,
        "status": status
    }
    attendance_records.append(attendance_entry)

    if status == "Absent":
        trigger_email(
            receiver_email=student_email,
            email_subject="Attendance Notification",
            email_body="You have been marked ABSENT today. Please reach out to your faculty."
        )

    return {"message": "Attendance updated successfully"}


@app.get("/attendance_history")
def attendance_history():
    return attendance_records


# ------------------------------------------------
# CAFETERIA PRE-ORDER
# ------------------------------------------------
@app.post("/order_food")
def order_food(student_name: str, food_item: str, break_time: str, student_email: str):
    food_entry = {
        "student": student_name,
        "food": food_item,
        "time": break_time
    }
    food_orders.append(food_entry)

    trigger_email(
        receiver_email=student_email,
        email_subject="Food Order Confirmation",
        email_body=f"Your order for {food_item} scheduled at {break_time} has been confirmed."
    )

    return {"message": "Food order saved successfully"}


@app.get("/food_order_history")
def food_order_history():
    return food_orders
