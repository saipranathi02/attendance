import pandas
import mysql.connector
from datetime import datetime
from PIL import Image
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import cv2
import face_recognition

#connection to mysql database
mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="photos")
mycursor = mydb.cursor()

#function to view student records
def view_data():
    mycursor.execute("SELECT name FROM images")
    data = mycursor.fetchall()
    return data

#function to view attendance of students
def view_attendance():
    mycursor.execute("SELECT * FROM images1")
    data = mycursor.fetchall()
    return data



#storing the details of registered students in the database
def capture_register(un,img):
    filename = "C:/Users/DELL/Desktop/project/Resources/{0}.jpg".format(un)
    cv2.imwrite(filename,img)
    s1 = "INSERT into images(name,img_dir) VALUES(%s,%s)"
    mycursor.execute(s1,(un,filename))
    mydb.commit()

#marking the attendance for students
def attendance(name):
    dateyear = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mycursor.execute("INSERT INTO images1(name,attendance) VALUES(%s,%s)",(name,dateyear))
    mydb.commit()

#comparing the captured image with registered images to check if they are a match 
def capture_recognize(img):
    known_faces=[]
    known_names=[]
    sqlst = "SELECT name,img_dir FROM images WHERE img_dir IS NOT NULL"
    mycursor.execute(sqlst)
    #appending the encodings and names of images present in the databsae
    for imgrecord in mycursor:      
        timg = face_recognition.load_image_file(imgrecord[1])
        known_faces.append(face_recognition.face_encodings(timg)[0])
        known_names.append(imgrecord[0])
    #saving the image captured from web cam in this path
    name = 'C:/Users/DELL/Desktop/project/opencv/image1.jpg' 
    cv2.imwrite(name,img)

    #collecting the encodings and location of the face in the captured image
    test_img = face_recognition.load_image_file(name)
    facelocations = face_recognition.face_locations(test_img)
    faceencodings = face_recognition.face_encodings(test_img,facelocations)
    for encoding in faceencodings:
        user_name = "Unknown"
        #comparing the captured image with registered(known) images
        match = face_recognition.compare_faces(known_faces,encoding,tolerance=0.5)
        #if the encoding of unknown image matches with any of the encoding of known images fetch its details
        if True in match:
            match_ind = match.index(True)
            user_name = known_names[match_ind]
            attendance(user_name)
    return user_name


hide_menu ="""<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>"""
i = Image.open('face_scan_adobe.jpg')
st.set_page_config(page_title="Attendance",page_icon=i,layout="centered")
st.markdown(hide_menu,unsafe_allow_html=True)
col1,col2,col3 = st.columns(3)
with col3:
    st.image(i,width=200)
with col1:
    st.title("Show your Face..")

with st.sidebar:
    selected = option_menu(menu_title="Menu",options=["Home page","Login","Register","View Student Records"],)

if selected == "Home page":
    
    st.write("    ")
    st.write("    ")
    st.write("This web application uses face recognition technology to recognize the user and mark attendance.Choose the action you want to perform by going through the below given information.")
    st.write("    ")
    st.write("    ")
    components.html("<html><style>h3 {color:black;font-family:Goudy Old Style;}</style><body><i><h3>Please go to the login page if you have already registered</h3><h3>Please register if you are a new user</h3><h3>Click on View Student Records if you want to view the student records</h3></i></body></html>")
    


if selected == "View Student Records":
    result1 = view_data()
    result2 = view_attendance()
    with st.expander("Registered Students"):
        df = pandas.DataFrame(result1,columns=["Name"])
        st.dataframe(df)
    with st.expander("Attendance"):
        df = pandas.DataFrame(result2,columns=["Name","Attendance"])
        st.dataframe(df)

elif selected == "Register":
    placeholder = st.empty()
    admin = st.sidebar.text_input("Username")
    adminpassword = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Register"):
        if adminpassword == "12345":
            new_user = placeholder.text_input("Enter your name")
            if st.button("Click to capture"):
                img = None
                capture = cv2.VideoCapture(0)
                img_display = st.empty()
                for i in range(60):
                    ret, img = capture.read()
                    img_display.image(img, channels='BGR')
                capture.release()
                capture_register(new_user,img)
                placeholder.empty()
                img_display.empty()
                st.success("Registered successfully")
        else:
            st.error("Username/Password is incorrect")

elif selected == "Login":
    if st.button("Click to capture"):
            img = None
            capture = cv2.VideoCapture(0)
            img_display = st.empty()
            for i in range(60):
                ret, img = capture.read()
                img_display.image(img, channels='BGR')
            capture.release()
            value = capture_recognize(img)
            if value == "Unknown":
                st.warning("Please register to login")
                img_display.empty()
            else:
                st.success('{0} Logged in successfully'.format(value))
                img_display.empty()

