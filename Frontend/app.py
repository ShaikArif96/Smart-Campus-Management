import streamlit as st
import requests

API_BASE_URL = "https://smart-campus-management-vgl0.onrender.com/"

st.title("🎓 Smart University Campus Portal")

section = st.selectbox(
    "Choose Service",
    [
        "Register Student",
        "Submit Attendance",
        "View Attendance Logs",
        "Place Food Order",
        "View Food Orders"
    ]
)

# ------------------------------------
# REGISTER STUDENT
# ------------------------------------
if section == "Register Student":
    st.header("Student Registration")

    student_full_name = st.text_input("Full Name")
    student_roll_no = st.text_input("University Roll Number")
    student_mail = st.text_input("Email Address")

    if st.button("Register"):
        res = requests.post(
            f"{API_BASE_URL}/add_student",
            params={
                "student_name": student_full_name,
                "roll_number": student_roll_no,
                "student_email": student_mail
            }
        )
        st.success(res.json()["message"])


# ------------------------------------
# SUBMIT ATTENDANCE
# ------------------------------------
if section == "Submit Attendance":
    st.header("Attendance Entry")

    roll_input = st.text_input("Roll Number")
    email_input = st.text_input("Registered Email")
    attendance_choice = st.selectbox("Select Status", ["Present", "Absent"])

    if st.button("Mark"):
        res = requests.post(
            f"{API_BASE_URL}/mark_attendance",
            params={
                "roll_number": roll_input,
                "status": attendance_choice,
                "student_email": email_input
            }
        )
        st.success(res.json()["message"])


# ------------------------------------
# VIEW ATTENDANCE LOGS
# ------------------------------------
if section == "View Attendance Logs":
    st.header("Attendance Records")

    res = requests.get(f"{API_BASE_URL}/attendance_history")
    attendance_data = res.json()

    if attendance_data:
        for entry in attendance_data:
            st.write(f"Roll No: {entry['roll']} | Attendance: {entry['status']}")
    else:
        st.info("No attendance data available")


# ------------------------------------
# PLACE FOOD ORDER
# ------------------------------------
if section == "Place Food Order":
    st.header("Cafeteria Pre-Order")

    order_student_name = st.text_input("Student Name")
    order_email = st.text_input("Student Email")
    menu_item = st.text_input("Food Item Name")
    slot_time = st.selectbox("Select Break Slot", ["10:30 AM", "1:30 PM", "4:30 PM"])

    if st.button("Confirm Order"):
        res = requests.post(
            f"{API_BASE_URL}/order_food",
            params={
                "student_name": order_student_name,
                "food_item": menu_item,
                "break_time": slot_time,
                "student_email": order_email
            }
        )
        st.success(res.json()["message"])


# ------------------------------------
# VIEW FOOD ORDERS
# ------------------------------------
if section == "View Food Orders":
    st.header("Food Order Records")

    res = requests.get(f"{API_BASE_URL}/food_order_history")
    food_orders = res.json()

    if food_orders:
        for item in food_orders:
            st.write(
                f"Student: {item['student']} | Item: {item['food']} | Slot: {item['time']}"
            )
    else:
        st.info("No food orders found")
