# attendance
This web application is used to mark attendance using face recognition.
This web application is developed uslng streamlit which is an open source framework.Hence this app works well in the local system.The database used here is mysql.The library I used to link mysql database is mysql.connector.Here host is the "localhost" ,username is "root" and password is "".The name of the database is photos.To rut this app on the local system go the folder where the main code is there and give this command in the command prompt for which the command is 'streamlit run main.py'.
The face recognition library and opencv is also used.Here an image is captured and then its encodings are taken and compared with the list of encodings of known images.If a match is foud then the name of the user is printed.
