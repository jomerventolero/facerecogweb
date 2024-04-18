
import threading
from flask import Flask, render_template, Response, request
import cv2
from simple_facerec import SimpleFacerec
import mysql.connector
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# Load Encoding Images
sfr = SimpleFacerec()
sfr.load_encoding_images("C:\\xampp2\\htdocs\\system\\pages\\student\\images\\")

# Initialize database connection
connection = mysql.connector.connect(
    host="projectisked.duckdns.org",
    user="admin",
    password="pass",
    database="u627005231_finalface"
)

directory_to_watch = "C:\\xampp2\\htdocs\\system\\pages\\student\\images\\"


# Watchdog event handler for file changes
class ImageChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type == 'created' or event.event_type == 'modified':
            print(f'Change detected in {event.src_path}')
            sfr.reload_encoding_images(directory_to_watch)


# Start watching the directory for changes
observer = Observer()
event_handler = ImageChangeHandler()
observer.schedule(event_handler, directory_to_watch, recursive=True)
observer.start()

def showname(name, subject, teacher, timeinout):
    try:
        cursor = connection.cursor()
        select_query = f"SELECT * FROM tblstudent WHERE fullname = '{name}'"
        cursor.execute(select_query)
        rows = cursor.fetchone()
        studentid = rows[0]

        cursor = connection.cursor()
        update_query = f"UPDATE tblstudentclass SET status = '1' WHERE studentid = '{studentid}' AND subjectid = '{subject}' AND teacherid = '{teacher}'"
        cursor.execute(update_query)
        connection.commit()
        cursor.close()

        current_date = datetime.now()
        date = current_date.strftime("%Y-%m-%d")

        current_time = datetime.now().strftime("%I:%M %p")


        if timeinout == 'Timein':
            cursor = connection.cursor()
            select_query = f"SELECT * FROM attendance WHERE studentid = '{studentid}' AND subjectid = '{subject}' AND teacherid = '{teacher}' AND date = '{date}'"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            if cursor.rowcount == 1:
                print(f"Successfully updated status for {name}{subject}{teacher}{timeinout}.")
            else:
                cursor = connection.cursor()
                update_query = f"INSERT INTO attendance (studentid, subjectid, teacherid, timein) VALUES ('{studentid}', '{subject}', '{teacher}', '{current_time}')"
                cursor.execute(update_query)
                connection.commit()
                cursor.close()
        
        else:
            print(f"Successfully updated status for {name}{subject}{teacher}{timeinout}.")
            cursor = connection.cursor()
            update_query = f"UPDATE attendance SET timeout = '{current_time}' WHERE studentid = '{studentid}' AND subjectid = '{subject}' AND teacherid = '{teacher}'  AND date = '{date}'"
            cursor.execute(update_query)
            connection.commit()
            cursor.close()



    except Exception as e:
        print(f"Error occurred: {e}")


    
def teacher_table():
    cursor = connection.cursor()
    select_query = f"SELECT * FROM tblteacher"
    cursor.execute(select_query)
    teachers = cursor.fetchall()
    return teachers

def subjects_table():
    cursor = connection.cursor()
    select_query = f"SELECT * FROM tblsubjects"
    cursor.execute(select_query)
    subjects = cursor.fetchall()
    return subjects


def get_id(name):
    subject = request.args.get('subject')
    teacher = request.args.get('teacher')
    timeinout = request.args.get('timeinout')
    showname(name,subject,teacher,timeinout)


def process_frame(frame, subject, teacher, timeinout):
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cursor = connection.cursor()
        select_query = f"SELECT * FROM tblstudent WHERE fullname = '{name}'"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        if cursor.rowcount == 1:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
            cv2.putText(frame, name, (x1, y1 - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 4)
            cv2.putText(frame, "Attendance Recorded", (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
            print("Success")
            showname(name, subject, teacher, timeinout)  
    
        else:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            print("Invalid.")

        cursor.close()

    return frame


def gen_frames(subject, teacher, timeinout):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't open camera.")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't read frame from camera.")
            break

        processed_frame = process_frame(frame, subject, teacher, timeinout)  # Pass subject and teacher to process_frame
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    subject = request.args.get('subject')
    teacher = request.args.get('teacher')
    timeinout = request.args.get('teacher')
    if subject:
        return render_template('index.php') + '' + subject + '' + teacher + '' + timeinout
    else:
        teachers = teacher_table()
        subjects = subjects_table()
        return render_template('selection.php', teachers=teachers, subjects=subjects)


@app.route('/video_feed')
def video_feed():
    subject = request.args.get('subject')
    teacher = request.args.get('teacher')
    timeinout = request.args.get('timeinout')
    return Response(gen_frames(subject, teacher, timeinout), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
