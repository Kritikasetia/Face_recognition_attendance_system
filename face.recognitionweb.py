from flask import Flask, render_template, Response, request
import cv2
import datetime , time
import os , sys
import numpy as np
import face_recognition
from datetime import datetime

# initiate flask app
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

global capture, rec_frame,  switch, face, rec, out, student_name
capture = 0
face = 0
switch = 1
rec = 0


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


def record(out):
   global rec_frame
   while (rec):
       time.sleep(0.05)
       out.write(rec_frame)


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
           f.writelines(f'"\n"{name},{tStr},{dStr}')


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
   global out, capture, rec_frame, student_name
   while True:
       success, frame = camera.read()
       if success:
           if (face):
               # pass
               frame, name = detect_face(frame)
               student_name = name

           if (capture):
               capture = 0
               frame, name = detect_face(frame)
               if name is not None and name != 'NO MATCH':
                   attendance(name)
                   student_name = name
               else:
                   print("Match not found")
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
   return render_template('index.html')


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

       elif request.form.get('face') == 'Face Only':
           global face
           face = not face
           if (face):
               time.sleep(4)
       elif request.form.get('stop') == 'Stop/Start':

           if (switch == 1):
               switch = 0
               camera.release()
               cv2.destroyAllWindows()

           else:
               camera = cv2.VideoCapture(0)
               switch = 1
       elif request.form.get('rec') == 'Start/Stop Recording':
           global rec, out
           rec = not rec
           if (rec):
               now = datetime.datetime.now()
               fourcc = cv2.VideoWriter_fourcc(*'XVID')
               out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":", '')), fourcc, 20.0, (640, 480))
               # Start new thread for recording the video
               thread = Thread(target=record, args=[out, ])
               thread.start()
           elif (rec == False):
               out.release()


   elif request.method == 'GET':
       return render_template('index.html')
   if student_name:
       print(student_name)
       return render_template('index.html', student_name=student_name)
   else:
       return render_template('index.html')
@app.route('/veiw')
def veiw():
    nameList = []
    entryList = []
    with open('attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        for line in myDataList:
            entry = line.split(',')
           # nameList.append(entry[0])
            entryList.append(entry)
            print(entryList)
    return  render_template('view.html',names =entryList)

if __name__ == '__main__':
   app.run()

camera.release()
cv2.destroyAllWindows()
