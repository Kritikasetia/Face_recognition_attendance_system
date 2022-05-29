# Face Recognition Attendance System

# Introduction
This is a face recognition based attendance system application built using python's flask framework and face_recognition library. It supports following feature:
- Mark Attendance: Students can visit the mark attendance page and use that to mark their attendance
- Teacher/Admin login to view attendance: Teachers or Admins can login into the application to view the attendance of the students.

For demo visit [here](https://youtu.be/4udEX259KXs)

# Steps to run the application using Docker
1. Clone the repository using `git clone git clone https://github.com/Kritikasetia/Face_recognition_attendance_system.git`.
2. Add your image in `images` directory in `your_name.jpg` format.
3. Run `xhost +local:docker`
4. Build the docker image: `sudo docker build --tag face_recognition_attendance_system .`
5. Run the docker image: `sudo docker run --rm  -d --name face_recognition_attendance_system --device /dev/video0 -p 5000:5000 face_recognition_attendance_system`
6. Check the logs using: `sudo docker logs -f face_recognition_attendance_system`
7. Once server is up, use this link to visit the webpage: http://127.0.0.1:5000/ and test the application.
8. To stop the docker container run `sudo docker stop face_recognition_attendance_system`

# Steps to run the application using venv
1. Clone the repository using `git clone git clone https://github.com/Kritikasetia/Face_recognition_attendance_system.git`.
2. Add your image in `images` directory in `your_name.jpg` format.
3. Download python 3.8.3 from python's official website
4. Download the venv from [here](https://drive.google.com/file/d/18lFGWVcuj6Q8d3HXW1qOOGDKSH8KSb-p/view?usp=sharing)
5. Extract the zip file in same directory.
6. Run `source venv/Scripts/activate` to activate the virtual environment on linux and just `venv/Scripts/activate` on windows.
7. Run `python face_recognition_web.py` to start the application.
8. Once server is up, use this link to visit the webpage: http://127.0.0.1:5000/ and test the application.

Note: Running application using Docker is tested in Ubuntu 20.04. It may not work on windows or mac because of opencv not able to access laptop's camera when run inside docker container.

Note: For any issue in installation of face_recognition library refer to the installtion section [here](https://virtualenv.pypa.io/en/legacy/index.html)

# Breif about technologies used.
- Project is written in python programming language.
- It uses flask which is a light weight web framework in python.
- I have used html to write frontend code and css for styling it.
- I have used csv file to store the attendance of the students.
- You can add data for more students by adding image for each of them in images directory in `your_name.jpg` format.

# References:
1. [Face Recognition library](https://github.com/ageitgey/face_recognition)
2. [Face Recognition libary docker setup](https://github.com/ageitgey/face_recognition/blob/master/docker/cpu/Dockerfile)
3. [Flask framework](https://flask.palletsprojects.com/en/2.1.x/)

