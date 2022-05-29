# sayani-saha_criminal-identification_face-recognition
Microsoft Engage 2022 Project

Problem Statement chosen: Demonstration of Face Recognition in preventing crime . Criminal Identification WebApp.
Frontend Technologies used : HTML, CSS , JavaScript
Backend Technologies used : Python , MySQL , OpenCV and face-recognition libraries of Python.
Framework : FLASK

Brief explanation about the working:

1. The WebApp scans faces in real time and checks for a match from the images saved in faces folder.
2. If a match is found it fetches the id and runs a query in criminal_record table to fetch the details about the criminal , else it displays the face as Unknown.
3. After the face is scanned, if we click on the details button it will display all the details. The details button gets enabled once the image is scanned and data is fetched.
4. One can add the details and image of a new criminal to the database. The image uploaded gets saved in the faces folder and the details get inserted into criminal_record table.

Screenshots:

![image](https://user-images.githubusercontent.com/60982835/170873190-2aaff41b-f42b-41c3-86b2-8c7b23313b19.png)
![image](https://user-images.githubusercontent.com/60982835/170873914-a70ab290-7600-4173-9d92-76de7545f47b.png)
![image](https://user-images.githubusercontent.com/60982835/170873941-37377240-75a4-4da2-ad91-167c7d1d145b.png)
![image](https://user-images.githubusercontent.com/60982835/170873993-0bb61ffb-3b4e-4b75-8a01-c737bfc2b84e.png)
![image](https://user-images.githubusercontent.com/60982835/170873963-963298f9-02ac-464c-a7ae-92de892e6f16.png)
