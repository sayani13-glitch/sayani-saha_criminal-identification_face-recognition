from glob import glob
from flask import Flask, after_this_request, render_template, Response , request,redirect,url_for
import cv2
import os
import face_recognition
import numpy as np
from werkzeug.utils import secure_filename
import mysql.connector
from datetime import date
import time


app=Flask(__name__)



#-------------------------------DATABASE CONNECTION---------------------------------------------
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="criminal_db"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE criminal_record (id VARCHAR(255),fname VARCHAR(255),lname VARCHAR(255),gender VARCHAR(255) ,crime VARCHAR(255),location VARCHAR(255))")
mycursor.execute("CREATE TABLE current_record (id VARCHAR(255),fname VARCHAR(255),lname VARCHAR(255),gender VARCHAR(255) ,crime VARCHAR(255),location VARCHAR(255))")
#----------------------------INSERTING SAMPLE DATA----------------------------------------------

mycursor.execute("INSERT INTO criminal_record VALUES('cr03','sayani','saha','female','robbery','west bengal')")
mycursor.execute("INSERT INTO criminal_record VALUES('cr02','joker','','male','theft','california')")
mycursor.execute("INSERT INTO criminal_record VALUES('cr01','loki','','male','robbery','new york')")


#----------------------------FACE RECOGNITION PART-------------------------------------------------


    
def gen_frames(camera):
    encoded = {}
    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = face_recognition.load_image_file("faces/" + f)
                encoding = face_recognition.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding



    known_face_names = list(encoded.keys())
    known_face_encodings=list(encoded.values())
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    res=[]
    name="Unknown"
    start_time = time.time()
    seconds = 10  
    while True:

        #timed-loop
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            camera.release()
            cv2.destroyAllWindows()
            break



        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                #A SECOND TABLE current_record IS USED TO STORE AND DISPLAY THE DATA OF CRIMINAL IF A MATCH IS FOUND

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    query="SELECT * FROM criminal_record where id='"+name+"'"
                    mycursor.execute(query)
                    if(mycursor):
                        res=mycursor.fetchall()
                        query="TRUNCATE TABLE current_record"
                        mycursor.execute(query)
                        query="INSERT INTO current_record VALUES( '"+res[0][0]+"','"+res[0][1]+"','"+res[0][2]+"','"+res[0][3]+"','"+res[0][4]+"','"+res[0][5]+"')"
                        mycursor.execute(query)
                        print("match found")
                        details=res[0][1] +" "+ res[0][2]
                else:
                    details=name
                    query="TRUNCATE TABLE current_record"
                    mycursor.execute(query)
                    mycursor.execute("INSERT INTO current_record (fname) VALUES ('UNIDENTIFIED FACE')")
                    print("match not found")
                face_names.append(name)
        # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

        # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 6)

        # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                
                cv2.putText(frame, details, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
#------------------------------------FACE RECOGNITION ENDS-----------------------------------------------





#------------------------------------APP ROUTES----------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tohome')
def tohome():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
#_______________________________________________________________________________________


@app.route('/scan')
def scan():
    return render_template('facescan.html')

#_______________________________________________________________________________________



@app.route('/addnew')
def addnew():
    return render_template('addnew.html')

#_______________________________________________________________________________________



@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


#_______________________________________________________________________________________


@app.route("/new_criminal",methods=['GET','POST'])
def new_criminal():
    fname=request.form.get('fname')
    lname=request.form.get('lname')
    gen=request.form.get('gen')
    crime=request.form.get('crime')
    loc=request.form.get('loc')
    pic=request.files['pic']
    fn1=secure_filename(pic.filename)
    pic.save(os.path.join('./faces',fn1))
    cid=fn1.split(".")[0]
    print(cid)
    query="INSERT INTO criminal_record VALUES('"+cid+"','"+fname+"','"+lname+"','"+gen+"','"+crime+"','"+loc+"')"
    mycursor.execute(query)
    if(mycursor):
        print("yes")
        query="SELECT * FROM criminal_record WHERE id='"+cid+"'"
        mycursor.execute(query)
        print(mycursor.fetchall())
    else:
        print("no")
    
    return render_template('home.html')


#_________________________________________________________________________________________



@app.route('/success')
def success():
    query="SELECT * FROM current_record"
    mycursor.execute(query)
    if(mycursor):
        print("inside success")
        res=mycursor.fetchall()
    return render_template('criminal_record.html',result=res)



#__________________________________________________________________________________________



if __name__=='__main__':
    app.run(debug=True)