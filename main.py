import os
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def password_prompt():
    password_file = 'Pass_Train/pass.txt'
    assure_path_exists("Pass_Train/")
    
    exists1 = os.path.isfile(password_file)
    if exists1:
        with open(password_file, "r") as tf:
            correct_password = tf.read().strip()
    else:
        new_pas = tsd.askstring('Password not set', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess.showerror('Null Password Entered', 'Password not set. Please try again!')
            return password_prompt()  # Retry if no password is set
        else:
            with open(password_file, "w") as tf:
                tf.write(new_pas)
            mess.showinfo('Password Registered!', 'New password was registered successfully!')
            correct_password = new_pas

    def verify_password():
        if password_entry.get() == correct_password:
            prompt.destroy()
            initialize_main_window()
        else:
            mess.showerror("Error", "Incorrect Password")

    prompt = tk.Tk()
    prompt.title("Enter Password")
    prompt.geometry("300x150")
    prompt.configure(background='#355454')

    label = tk.Label(prompt, text="Enter Password", bg='#355454', fg="white", font=('times', 12, 'bold'))
    label.pack(pady=20)

    password_entry = tk.Entry(prompt, show='*', font=('times', 12, 'bold'))
    password_entry.pack(pady=5)

    submit_button = tk.Button(prompt, text="Submit", command=verify_password, bg="#13059c", fg="white", font=('times', 12, 'bold'))
    submit_button.pack(pady=10)

    prompt.mainloop()

def initialize_main_window():
    import os
    import cv2
    import numpy as np
    from PIL import Image
    import datetime
    import time
    import mysql.connector
    import tkinter

    def connect_to_db():
        return mysql.connector.connect(
            host="localhost",
            user="attendance_user",
            password="attendance_password",
            database="attendance_db"
        )

    # Functions===========================================================

    # Ask for QUIT
    def on_closing():
        if mess.askyesno("Quit", "You are exiting window. Do you want to quit?"):
            window.destroy()

    # Contact
    def contact():
        mess._show(title="Contact Me", message="If you need any help, contact me at 'harisalibaig11@gmail.com'")

    # About
    def about():
        mess._show(title="About", message="This Attendance System is designed by Abdul Hadi")

    # Clear button
    def clear():
        txt.delete(0, 'end')
        txt2.delete(0, 'end')
        res = "1) Take Images  ===> 2) Save Profile"
        message1.configure(text=res)

    # Check for haarcascade file
    def check_haarcascadefile():
        if not os.path.isfile("haarcascade_frontalface_default.xml"):
            mess._show(title='File missing', message='Haarcascade file is missing. Please contact support.')
            window.destroy()


    def populate_treeview(subject=None):
        tb.delete(*tb.get_children())  # Clear existing data in the Treeview
        attendance_data = fetch_attendance_data(subject)
        for row in attendance_data:
            tb.insert('', 'end', text=row[0], values=(row[1], row[2], row[3],row[4]))



    #change password
    def change_pass():
        global master
        master = tkinter.Tk()
        master.geometry("400x160")
        master.resizable(False,False)
        master.title("Change Admin Password")
        master.configure(background="white")
        lbl4 = tkinter.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
        lbl4.place(x=10,y=10)
        global old
        old=tkinter.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
        old.place(x=180,y=10)
        lbl5 = tkinter.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
        lbl5.place(x=10, y=45)
        global new
        new = tkinter.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
        new.place(x=180, y=45)
        lbl6 = tkinter.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
        lbl6.place(x=10, y=80)
        global nnew
        nnew = tkinter.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
        nnew.place(x=180, y=80)
        cancel=tkinter.Button(master,text="Cancel", command=master.destroy, fg="white" , bg="#13059c", height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
        cancel.place(x=200, y=120)
        save1 = tkinter.Button(master, text="Save", command=save_pass, fg="black", bg="#00aeff", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
        save1.place(x=10, y=120)
        master.mainloop()
    #check the password for change the password
    def save_pass():
        assure_path_exists("Pass_Train/")
        exists1 = os.path.isfile("Pass_Train\pass.txt")
        if exists1:
            tf = open("Pass_Train\pass.txt", "r")
            str = tf.read()
        else:
            master.destroy()
            new_pas = tsd.askstring('Password not set', 'Please enter a new password below', show='*')
            if new_pas == None:
                mess._show(title='Null Password Entered', message='Password not set.Please try again!')
            else:
                tf = open("Pass_Train\pass.txt", "w")
                tf.write(new_pas)
                mess._show(title='Password Registered!', message='New password was registered successfully!')
                return
        op = (old.get())
        newp= (new.get())
        nnewp = (nnew.get())
        if (op == str):
            if(newp == nnewp):
                txf = open("Pass_Train\pass.txt", "w")
                txf.write(newp)
            else:
                mess._show(title='Error', message='Confirm new password again!!!')
                return
        else:
            mess._show(title='Wrong Password', message='Please enter correct old password.')
            return
        mess._show(title='Password Changed', message='Password changed successfully!!')
        master.destroy()

    #ask for password
    def psw():
        assure_path_exists("Pass_Train/")
        exists1 = os.path.isfile("Pass_Train\pass.txt")
        if exists1:
            tf = open("Pass_Train\pass.txt", "r")
            str_pass = tf.read()
        else:
            new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
            if new_pas == None:
                mess._show(title='No Password Entered', message='Password not set!! Please try again')
            else:
                tf = open("Pass_Train\pass.txt", "w")
                tf.write(new_pas)
                mess._show(title='Password Registered', message='New password was registered successfully!!')
                return
        password = tsd.askstring('Password', 'Enter Password', show='*')
        if (password == str_pass):
            TrainImages()

        elif (password == None):
            pass
        else:
            mess._show(title='Wrong Password', message='You have entered wrong password')

    #Check for correct Path
    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    # Function to take images
    def TakeImages():
        assure_path_exists("TrainingImage/")
        check_haarcascadefile()
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS students (serial INT AUTO_INCREMENT PRIMARY KEY, student_id VARCHAR(255), name VARCHAR(255))")
        
        Id = txt.get()
        name = txt2.get()
        
        if name.isalpha() or ' ' in name:
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            
            cursor.execute("SELECT MAX(serial) FROM students")
            result = cursor.fetchone()
            serial = result[0] + 1 if result[0] else 1
            
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.05, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    sampleNum += 1
                    cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('Taking Images', img)
                
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 100:
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            
            res = f"Images Taken for ID : {Id}"
            cursor.execute("INSERT INTO students (student_id, name) VALUES (%s, %s)", (Id, name))
            db.commit()
            message1.configure(text=res)
        else:
            message.configure(text="Enter Correct name")
        db.close()

    # Function to train images
    def TrainImages():
        check_haarcascadefile()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, IDs = getImagesAndLabels("TrainingImage")
        
        if len(faces) == 0:
            mess._show(title='No Registrations', message='Please register someone first!')
            return
        
        try:
            recognizer.train(faces, np.array(IDs))
            recognizer.save("Pass_Train/Trainner.yml")
            res = "Profile Saved Successfully"
            message1.configure(text=res)
            message.configure(text='Total Registrations till now: '+str(fetch_total_registrations()))
        except Exception as e:
            print(f"Training error: {e}")
            mess._show(title='Training Error', message='Error in training images.')

    # Function to get images and labels
    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            if imagePath.endswith('.jpg'):
                pilImage = Image.open(imagePath).convert('L')
                imageNp = np.array(pilImage, 'uint8')
                ID = int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(imageNp)
                IDs.append(ID)
        return faces, IDs



    def TrackImages():
        check_haarcascadefile()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Pass_Train/Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        
        db = connect_to_db()
        cursor = db.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS attendance (student_id VARCHAR(255), name VARCHAR(255), date DATE, time TIME, subject VARCHAR(255))")
        
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        inserted_ids = set()  # flag to track inserted attendance
        
        while True:
            ret, im = cam.read()
            if not ret or im is None:
                print("Failed to grab frame")
                continue

            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                
                print(f"Recognized Id: {Id}, Confidence: {conf}")
                
                if conf < 80:
                    cursor.execute("SELECT name FROM students WHERE serial=%s", (str(Id),))
                    result = cursor.fetchone()
                    if result:
                        name = result[0]
                        print(f"Name found: {name}")
                    else:
                        print(f"No name found for student_id {Id}")
                        name = 'Unknown'
                else:
                    name = 'Unknown'
                
                cv2.putText(im, str(name), (x, y + h), font, 1, (255, 255, 255), 2)
                
                if name != 'Unknown' and Id not in inserted_ids:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    
                    # Prompt user to enter subject name     
                    subject = tsd.askstring("Subject", "Enter Subject Name:")
                    if subject:
                        cursor.execute("INSERT INTO attendance (student_id, name, date, time, subject) VALUES (%s, %s, %s, %s, %s)",
                                    (str(Id), name, date, timeStamp, subject))
                        db.commit()
                        print(f"Inserted attendance for {name} ({Id}) for subject {subject}")
                        inserted_ids.add(Id)  # mark attendance as inserted
                        
                        # Display the recognized frame for 5 seconds before closing
                        cv2.imshow('Tracking', im)
                        cv2.waitKey(5000)  # 5000 ms = 5 seconds
                        
                        # Break out of both loops
                        cam.release()
                        cv2.destroyAllWindows()
                        db.close()
                        populate_treeview()
                        return
            
            cv2.imshow('Tracking', im)
            
            if cv2.waitKey(1) == ord('q'):
                break
        
        cam.release()
        cv2.destroyAllWindows()
        db.close()


    window = tkinter.Tk()
    window.title("Face Recognition Based Attendance System")
    window.geometry("1280x720")
    window.resizable(True,True)
    window.configure(background='#325454')
    
    #Help menubar----------------------------------------------
    menubar=Menu(window)
    help=Menu(menubar,tearoff=0)
    help.add_command(label="Change Password!",command=change_pass)
    help.add_command(label="Contact Us",command=contact)
    help.add_separator()
    help.add_command(label="Exit",command=on_closing)
    menubar.add_cascade(label="Help",menu=help)

    # add ABOUT label to menubar-------------------------------
    menubar.add_command(label="About",command=about)

    #This line will attach our menu to window
    window.config(menu=menubar)

    #main window------------------------------------------------
    message3 = tkinter.Label(window, text="Face Recognition Based Attendance System" ,fg="white",bg="#355454" ,width=60 ,height=1,font=('times', 29, ' bold '))
    message3.place(x=10, y=10,relwidth=1)
    message3 = tkinter.Label(window, text="Using OpenCV & MySQL" ,fg="white",bg="#355454" ,width=60 ,height=1,font=('times', 17, ' bold '))
    message3.place(x=10, y=46,relwidth=1)

    #frames-------------------------------------------------
    frame1 = tkinter.Frame(window, bg="white")
    frame1.place(relx=0.11, rely=0.15, relwidth=0.39, relheight=0.80)

    frame2 = tkinter.Frame(window, bg="white")
    frame2.place(relx=0.51, rely=0.15, relwidth=0.40, relheight=0.80)

    #frame_headder
    fr_head1 = tkinter.Label(frame1, text="Register New Student", fg="white",bg="black" ,font=('times', 17, ' bold ') )
    fr_head1.place(x=0,y=0,relwidth=1)

    fr_head2 = tkinter.Label(frame2, text="Mark Student's attendance", fg="white",bg="black" ,font=('times', 17, ' bold ') )
    fr_head2.place(x=0,y=0,relwidth=8)

    #registretion frame
    lbl = tkinter.Label(frame1, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold ') )
    lbl.place(x=0, y=55)

    txt = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold '))
    txt.place(x=55, y=88,relwidth=0.75)

    lbl2 = tkinter.Label(frame1, text="Enter Name",width=20  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold '))
    lbl2.place(x=0, y=140)

    txt2 = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
    txt2.place(x=55, y=173,relwidth=0.75)

    message0=tkinter.Label(frame1,text="Follow the steps...",bg="white" ,fg="black"  ,width=39 ,height=1,font=('times', 16, ' bold '))
    message0.place(x=7,y=275)

    message1 = tkinter.Label(frame1, text="1)Take Images  ===> 2)Save Profile" ,bg="white" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
    message1.place(x=7, y=300)

    message = tkinter.Label(frame1, text="" ,bg="white" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
    message.place(x=7, y=500)
    #Attendance frame
    lbl3 = tkinter.Label(frame2, text="Attendance Table",width=20  ,fg="black"  ,bg="white"  ,height=1 ,font=('times', 17, ' bold '))
    lbl3.place(x=100, y=115)
    
    def fetch_total_registrations():
        db = connect_to_db()
        cursor = db.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM students")
            total_registrations = cursor.fetchone()[0]
            return total_registrations
        except mysql.connector.Error as err:
            print(f"Error fetching total registrations: {err}")
            return 0
        finally:
            cursor.close()
            db.close()

    message.configure(text='Total Registrations : '+str(fetch_total_registrations()))


    #BUTTONS----------------------------------------------

    clearButton = tkinter.Button(frame1, text="Clear", command=clear, fg="white", bg="#13059c", width=11, activebackground = "white", font=('times', 12, ' bold '))
    clearButton.place(x=55, y=230,relwidth=0.29)

    takeImg = tkinter.Button(frame1, text="Take Images", command=TakeImages, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
    takeImg.place(x=30, y=350,relwidth=0.89)

    trainImg = tkinter.Button(frame1, text="Save Profile", command=psw, fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
    trainImg.place(x=30, y=430,relwidth=0.89)

    trackImg = tkinter.Button(frame2, text="Take Attendance", command=TrackImages, fg="black", bg="#00aeff", height=1, activebackground = "white" ,font=('times', 16, ' bold '))
    trackImg.place(x=30,y=60,relwidth=0.89)

    quitWindow = tkinter.Button(frame2, text="Quit", command=window.destroy, fg="white", bg="#13059c", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
    quitWindow.place(x=30, y=450,relwidth=0.89)


    #Attandance table----------------------------


    # Function to fetch attendance data from MySQL
    def fetch_attendance_data(subject=None):
        db = connect_to_db()
        cursor = db.cursor()

        try:
            if subject:
                cursor.execute("SELECT student_id, name, date, time,subject FROM attendance WHERE subject = %s", (subject,))
            else:
                cursor.execute("SELECT student_id, name, date, time, subject FROM attendance")
            attendance_data = cursor.fetchall()
            return attendance_data
        except mysql.connector.Error as err:
            print(f"Error fetching attendance data: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    from tkinter import ttk
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('times', 13, 'bold')) # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

    tb = ttk.Treeview(frame2, height=13, columns=('name', 'date', 'time','subject'), style="mystyle.Treeview")
    tb.column('#0', width=82)
    tb.column('name', width=130)
    tb.column('date', width=133)
    tb.column('time', width=133)
    tb.column('subject', width=133)
    tb.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4)
    tb.heading('#0', text='ID')
    tb.heading('name', text='NAME')
    tb.heading('date', text='DATE')
    tb.heading('time', text='TIME')
    tb.heading('subject', text='SUBJECT')

    # Populate the Treeview with attendance data
    populate_treeview()

    #SCROLLBAR--------------------------------------------------

    scroll=ttk.Scrollbar(frame2,orient='vertical',command=tb.yview)
    scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
    tb.configure(yscrollcommand=scroll.set)

    #closing lines------------------------------------------------
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

# Call the password prompt function before initializing the main window
password_prompt()
