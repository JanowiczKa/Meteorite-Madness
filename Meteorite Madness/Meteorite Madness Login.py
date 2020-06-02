from tkinter import *
import MeteoriteMadnessPrototype

root = Tk()
root.resizable(width=False, height=False)
root.geometry("{}x{}".format(800, 600))
root.title("Meteorite Madness Login")

namecre = StringVar()
passwordcre = StringVar()
namevar = StringVar()
passwordvar = StringVar()

space = "#030e25"

def LogScreen():
    
    #Background
    background = PhotoImage(file="./UI/SpaceBackground.png")
    background_label = Label(root, image=background)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background

    logo = PhotoImage(file="./UI/MeteoriteMadnessLogo.png")
    logo_label = Label(root, image=logo, bg=space)
    logo_label.place(x=275, y=0)
    logo_label.image = logo

    message("")

    #LOGIN
    #Username
    username = Label(root, text="Username", bg=space,
                 fg="white", font=("freesansbold", 16))
    username.config(height=1,width=10)
    username.place(x=350, y=270)

    username_enter = Entry(root, textvariable=namevar,
                       font=("freesansbold", 10))
    username_enter.place(x=340, y=310)
    
    #Password
    password = Label(root, text="Password", bg=space,
                     fg="white", font=("freesansbold", 16))
    password.config(height=1,width=10)
    password.place(x=350, y=350)
    
    password_enter = Entry(root, textvariable=passwordvar,show="*",
                           font=("freesansbold", 10))
    password_enter.place(x=340, y=390)

    #Login Button
    button = Button(root, text="Log in!", height = 1, command=lambda:logIn(),
                    width = 15, font=("", 12))
    button.place(x=340, y=430)

    #ACCOUNT CREATION
    #Username
    create_username = Label(root, text="New Username", bg=space,
                        fg="white", font=("freesansbold", 16))
    create_username.config(height=1, width=12)
    create_username.place(x=627, y=390)

    create_name_enter = Entry(root, textvariable=namecre,
                              font=("freesansbold", 10))
    create_name_enter.place(x=630, y=430)
    
    #Password
    create_password = Label(root, text="New Password", bg=space,
                            fg="white", font=("freesansbold", 16))
    create_password.config(height=1,width=12)
    create_password.place(x=627, y=470)

    create_password_enter = Entry(root, textvariable=passwordcre,
                                  font=("freesansbold", 10))
    create_password_enter.place(x=627, y=510)
    
    create_button = Button(root, text="Create an account!", command=lambda:createLog(),
                           height = 1, width = 15, font=("freesansbold", 12)).place(x=627, y=550)

def createLog():
        
    file_users = open("userdata.txt")
    lines_users = file_users.readlines()
    length = (len(lines_users))

    nam = namecre.get()    
    pas = passwordcre.get()

    already_taken = False

    for x in range(length):

        if nam == lines_users[x].rstrip():
            already_taken = True
            message("This username already exists!")

    if already_taken == False:
        
        print(lines_users)
        print(length)

        if (not nam or not pas):            
            message("You cannot leave the boxes empty!")            
        elif (" " in nam or " " in pas):            
            message("You cannot have spaces in your username or password!")            
        else:
            
            string = "\n" + nam + "-" + pas + "-0"
            
            if length == 0:

                string = nam + "-" + pas + "-0"
            
                
            with open("userdata.txt", "a") as db:
                db.write(string)
                db.close()
              
            message("Account created!")

def logIn():
    
    file_users = open("userdata.txt")
    lines_users = file_users.readlines()    
    length = len(lines_users)
    
    n = namevar.get()
    p = passwordvar.get()

    #print(n + "  " + p)

    for x in range(length):

        name, password, score = lines_users[x].split("-")
        #print(name + "  " + password)

        if n == name:
            if p == password:
                loggedIn(x)
            else:
                message("Incorrect password")
                break
        else:  
            message("Username doesn't exist")
        

def loggedIn(index):

    root.destroy()

    MeteoriteMadnessPrototype.Load_Player_Stats(index)

def message(textsent):
    
    status = Label(root, text=str(textsent), bg=space,
                   fg="white", font=("freesansbold", 16), width=42,
                   height=2, anchor=CENTER).place(x=100, y=500)

LogScreen()
