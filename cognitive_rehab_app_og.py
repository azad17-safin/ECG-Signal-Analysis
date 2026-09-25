print("Program started")
import tkinter as tk
from tkinter import messagebox
import random,time,csv
from datetime import datetime
##tkinter is used to make the desktop app window.
##messagebox is used to show warning popups.
##random is used to randomly choose color words.
##time is used to calculate reaction time.
#csv is used to save patient data.
#datetime is used to save the date and time of the test#

# These variables store patient and test information
patient_id=""
patient_age=""
time_left=30
total_attempts=0
correct_answers=0
reaction_times=[]
current_ink_color=""
word_start_time=0
colors={"Red":"red","Blue":"blue","Green":"green","Yellow":"gold"}

#screen clearing function
# This function clears all widgets from the current screen
# It helps us move from login screen to game screen and result screen
def clear_screen():
   for widget in root.winfo_children():
        widget.destroy()

# This function shows the first screen of the app
def show_login_screen():
    clear_screen()
    tk.Label(root,text="Cognitive Rehabilitation App",font=("Arial",22,"bold")).pack(pady=25)
    tk.Label(root,text="Brain Fog cognitive Tracking",font=("Arial",14)).pack(pady=5)
    tk.Label(root,text="Patient ID / name:",font=("Arial",13)).pack(pady=5)
     # patient_entry is global because we need to use its value in start_test()
    global patient_entry
    patient_entry=tk.Entry(root,font=("Arial",13),width=30)
    patient_entry.pack(pady=5)

    tk.Label(root,text="Age:",font=("Arial",13),width=30).pack(pady=5)
    global age_entry
    age_entry=tk.Entry(root,font=("Arial",13),width=30)
    age_entry.pack(pady=5)
    # Start button moves the user to the Stroop test screen
    tk.Button(root,text="Start Cognitive Test",font=("Arial",14,"bold"),bg="blue",fg="white",command=start_test).pack(pady=25)
# This function starts the cognitive test
# It collects patient data and resets score/timer values
def start_test():
    global patient_id,patient_age,time_left,total_attempts,correct_answers,reaction_times
    patient_id=patient_entry.get().strip()
    patient_age=age_entry.get().strip()

    time_left=30
    total_attempts=0
    correct_answers=0
    reaction_times=[]
    show_game_screen()
def show_game_screen():
    clear_screen()
    global timer_Label,word_Label,score_Label
    timer_Label=tk.Label(root,text="Time Left:30",font=("Arial",50,"bold"))
    timer_Label.pack(pady=20)
    tk.Label(root,text="Click the INK color,not the word.",font=("Arial",13)).pack(pady=5)

    word_Label=tk.Label(root,text="",font=("Arial",50,"bold"))
    word_Label.pack(pady=50)
      # Frame is used to keep color buttons in one row
    button_frame=tk.Frame(root)
    button_frame.pack(pady=10)
 # Create one button for each color
    # lambda is used so each button sends its own color name to check_answer()
    for color_name in colors:
         tk.Button(button_frame,text=color_name,font=("Arial",13,"bold"),width=10,command=lambda c=color_name:check_answer(c)).pack(side="left",padx=8)

    score_Label=tk.Label(root,text="Attempts: 0 | correct: 0",font=("Arial",13))
    score_Label.pack(pady=20)
    new_word()
    update_timer()

#new Stroop word function

def new_word():
    global current_ink_color,word_start_time
    word=random.choice(list(colors.keys()))
    ink=random.choice(list(colors.keys()))

    while word==ink:
        ink=random.choice(list(colors.keys()))

    current_ink_color=ink
    word_Label.config(text=word.upper(),fg=colors[ink])
    word_start_time=time.time()
#Checking answer
def check_answer(selected_color):
    global total_attempts,correct_answers

    if time_left<=0:
        return

    end_time=time.time()
    reaction_time=round((end_time-word_start_time)*1000,2)
    reaction_times.append(reaction_time)

    total_attempts+=1

    if selected_color==current_ink_color:
        correct_answers+=1

    score_Label.config(text=f"Attempts: {total_attempts} | Correct: {correct_answers}")
    new_word()
#timer function
def update_timer():
    global time_left
    timer_Label.config(text=f"Time Left: {time_left}")

    if time_left>0:
        time_left-=1
        root.after(1000,update_timer)
    else:
        show_result_screen()
def show_result_screen():
      clear_screen()

      if len(reaction_times)>0:
        avg_reaction_time=round(sum(reaction_times)/len(reaction_times),2)
      else:
        avg_reaction_time=0

      save_to_csv(avg_reaction_time)

      tk.Label(root,text="Test Complete",font=("Arial",25,"bold"),fg="green").pack(pady=25)
      tk.Label(root,text=f"Patient ID / Name: {patient_id}",font=("Arial",14)).pack(pady=5)
      tk.Label(root,text=f"Age: {patient_age}",font=("Arial",14)).pack(pady=5)
      tk.Label(root,text=f"Total Attempts: {total_attempts}",font=("Arial",14)).pack(pady=5)
      tk.Label(root,text=f"Correct Answers: {correct_answers}",font=("Arial",14)).pack(pady=5)
      tk.Label(root,text=f"Average Reaction Time: {avg_reaction_time} ms",font=("Arial",14)).pack(pady=5)
      tk.Label(root,text='Data saved to "patient_cognitive_data_og.csv"',font=("Arial",11),fg="gray").pack(pady=15)
      tk.Button(root,text="Run Again",font=("Arial",13,"bold"),command=show_login_screen).pack(pady=8)
      tk.Button(root,text="Exit",font=("Arial",13,"bold"),command=root.quit).pack(pady=5)

def save_to_csv(avg_reaction_time):
    file_name="patient_cognitive_data_og.csv"
    headers=["Patient_ID","Age","Date","Total_Attempts","Correct_Answers","Avg_Reaction_Time_ms"]

    row=[
        patient_id,
        patient_age,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_attempts,
        correct_answers,
        avg_reaction_time
    ]

    try:
        file_exists=False

        try:
            with open(file_name,"r",newline="") as file:
                file_exists=True
        except FileNotFoundError:
            file_exists=False

        with open(file_name,"a",newline="") as file:
            writer=csv.writer(file)

            if not file_exists:
                writer.writerow(headers)

            writer.writerow(row)

    except:
        messagebox.showerror("Error","Could not save data to CSV file.")

root=tk.Tk()
root.title("Cognitive Rehabilitation App")
root.geometry("700x500")
root.resizable(False,False)
show_login_screen()
root.mainloop()