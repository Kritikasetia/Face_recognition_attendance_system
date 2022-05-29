from flask import Flask, render_template, Response, request, session, redirect, url_for, g
import cv2
from datetime import datetime
import time
import os
import numpy as np
import face_recognition
import adminuser

# initiate flask app
app = Flask(__name__, template_folder='./templates',  static_url_path='/static')

camera = cv2.VideoCapture(0)

global capture, switch, face, student_name
capture = 0
face = 0
switch = 1

path = 'images'
images = []
personName = []
myList = os.listdir(path)
print(myList)

for cu_img in myList:
   current_Img = cv2.imread(f'{path}/{cu_img}')
   images.append(current_Img)
   personName.append(os.path.splitext(cu_img)[0])
print(personName)

def faceEncodings(images):
   encodeList = []
   for img in images:
       img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       encode = face_recognition.face_encodings(img)[0]
       encodeList.append(encode)
   return encodeList

encodeListknown = faceEncodings(images)
print("All encodings complete")

def attendance(name):
   with open('attendance.csv', 'a+') as f:
       myDataList = f.readlines()
       nameList = []
       for line in myDataList:
           entry = line.split(',')
           nameList.append(entry[0])

       if name not in nameList:
           time_now = datetime.now()
           tStr = time_now.strftime('%H:%M:%S')
           dStr = time_now.strftime('%d/%m/%Y')
           f.writelines(f'\n{name},{tStr},{dStr}')

def detect_face(frame):
   faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
   faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
   facesCurrentFrame = face_recognition.face_locations(faces)
   encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)
   name = "NO MATCH"
   for encodeFace, faceloc in zip(encodesCurrentFrame, facesCurrentFrame):
       matches = face_recognition.compare_faces(encodeListknown, encodeFace)
       facDis = face_recognition.face_distance(encodeListknown, encodeFace)

       matchIndex = np.argmin(facDis)
       print(matchIndex)
       if matches[matchIndex]:
           name = personName[matchIndex].upper()
           print(name)
       y1, x2, y2, x1 = faceloc
       y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
       cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
       cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
       cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
   return frame, name

def gen_frames():  # generate frame by frame from camera
   global  capture, student_name
   while True:
       success, frame = camera.read()
       if success:
           if (face):
               # pass
               frame, name = detect_face(frame)
               student_name = name

           if (capture):

               frame, name = detect_face(frame)
               student_name = name

               if name is not None and name != 'NO MATCH':
                   attendance(name)
               else:
                   print("Match not found")
               capture = 0
           try:
               ret, buffer = cv2.imencode('.jpg', frame)
               frame = buffer.tobytes()
               yield (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
           except Exception as e:
               pass

       else:
           pass

@app.route('/')
def index():
   return render_template('home.html')

@app.route('/video_feed')
def video_feed():
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST', 'GET'])
def tasks():
   global switch, camera, student_name

   if request.method == 'POST':

       if request.form.get('click') == 'Capture':
           global capture
           capture = 1
           while capture == 1:
              time.sleep(1)
           #return render_template('Mark_Attendance.html', student_name=student_name)
       elif request.form.get('face') == 'Face Only':
           global face
           face = not face
           if face:
               time.sleep(4)
       elif request.form.get('stop') == 'Stop/Start':
           if switch == 1:
               switch = 0
               camera.release()
               cv2.destroyAllWindows()

           else:
               camera = cv2.VideoCapture(0)
               switch = 1
       #return render_template('Mark_Attendance.html')
       if student_name:
           print(student_name)
           return render_template('Mark_Attendance.html', student_name=student_name)
       else:
           return render_template('Mark_Attendance.html')
   elif request.method == 'GET':
       return render_template('Mark_Attendance.html')

app.secret_key = 'somesecretkeythatonlyishouldknow'
users = []
users.append(adminuser.AdminUser(id=1, username='Admin', password='password'))

def before_request():
   g.user = None

   if 'user_id' in session:
       user = [x for x in users if x.id == session['user_id']][0]
       g.user = user

@app.route('/login', methods=['GET', 'POST'])

def login():
   if request.method == 'POST':
       session.pop('user_id', None)

       username = request.form['username']
       password = request.form['password']

       matched_users = [x for x in users if x.username == username]
       if len(matched_users) == 0:
           return redirect(url_for('login'))

       user = matched_users[0]
       if user and user.password == password:
           session['user_id'] = user.id
           return redirect(url_for('veiw'))
       return redirect(url_for('login'))
   return render_template('login.html')
   if not g.user:
       return redirect(url_for('login'))

@app.route('/veiw')

def veiw():
   entryList = []
   with open('attendance.csv', 'r+') as f:
       myDataList = f.readlines()
       for line in myDataList:
           entry = line.split(',')
           entryList.append(entry)
           print(entryList)

   return render_template('view.html', names=entryList)

if __name__ == '__main__':
   app.run()

camera.release()
cv2.destroyAllWindows()
