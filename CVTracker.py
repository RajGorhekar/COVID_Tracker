import requests
import bs4
from tkinter import *
import time
import plyer
import threading
from datetime import datetime

def getTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y \nat  %H:%M:%S")
    return dt_string

def getHtml(url):
    data  = requests.get(url)
    return data

def getIndianDetails():
    url = "https://www.mohfw.gov.in"
    Html_data = getHtml(url)
    bs = bs4.BeautifulSoup(Html_data.text,'html.parser')
    figures = bs.find("div",class_ = "site-stats-count").find_all("strong")
    titles = bs.find("div",class_ = "site-stats-count").find_all("span")
    heading = bs.find("div",class_ ="site-stats-count").find("div",class_ ="status-update").find('span').get_text()
    heading = "COVID-19 STATS " + str(heading)
    i=0
    stats = [heading]
    for f in figures:
        stats.append(titles[i].get_text())
        stats.append(f.get_text()) 
        if(i==1):
            i+=2
        i+=1
    return stats

def getStateWiseDetails():
    url = "https://www.mohfw.gov.in"
    Html_data = getHtml(url)
    bs = bs4.BeautifulSoup(Html_data.text,'html.parser')
    info = bs.find("div",class_ ="data-table table-responsive").find_all('tr')
    b = []
    for row in info[1:] : 
        ele = row.find_all('td')
        c=[]
        for e in ele : 
            c.append(e.get_text())
        b.append(c) 
    return b[:32]
    
def makeHeader(root):
    h1 =Label(root, text=getIndianDetails()[1] + ' : ', fg="black", font="Verdana 18 bold")
    h1.place(x=20, y=10)
    f1 =Label(root, text=getIndianDetails()[2], fg="red", font="Verdana 18 ")
    f1.place(x=215, y=10)
    h2 =Label(root, text=getIndianDetails()[3][8:] + ' : ', fg="black", font="Verdana 18 bold")
    h2.place(x=315, y=10)
    f2 =Label(root, text=getIndianDetails()[4], fg="blue", font="Verdana 18 ")
    f2.place(x=500, y=10)
    h3 =Label(root, text=getIndianDetails()[5] + ' : ', fg="black", font="Verdana 18 bold")
    h3.place(x=585, y=10)
    f3 =Label(root, text=getIndianDetails()[6], fg="red", font="Verdana 18 ")
    f3.place(x=707, y=10)
    h4 =Label(root, text=getIndianDetails()[7] + ' : ', fg="black", font="Verdana 18 bold")
    h4.place(x=795, y=10)
    f4 =Label(root, text=getIndianDetails()[8], fg="red", font="Verdana 18 ")
    f4.place(x=961, y=10)
    f5 =Label(root, text='                                                 Statewise Analysis                                                          ', fg="white", bg = 'black' ,font="Verdana 18 ")
    f5.place(x=0, y=48)

def widget(root,x,y,list):
    h1=Label(root, text=str(list[0])+". "+list[1], fg="black", font="Times 10 bold")
    h1.place(x=x, y=y)
    a1=Label(root, text="  Cases : " + str(list[2]), fg="#00bbff", font="Times 10 ")
    a1.place(x=x, y=y+20)
    a2=Label(root, text= "  Cured : " + str(list[3]), fg="#02bf21", font="Times 10 ")
    a2.place(x=x, y=y+40)
    a3=Label(root, text="  Deaths : " + str(list[4]), fg="red", font="Times 10 ")
    a3.place(x=x, y=y+60)

def refresh(root,label):
    makeHeader(root)
    makeStates(root)
    label['text'] = "Last\nRefreshed on :\n" + str(getTime())

def makeStates(root):
    x = 20
    y = 90
    for list in getStateWiseDetails():
        widget(root,x,y,list)
        y += 90
        if(y>=720):
            y=90
            x+=200
        
def createTable(canvas):
    x = 5
    y1 = 81
    y2 = 715
    for i in range(6):
        canvas.create_line(x,y1,x,y2,width=4)
        x+= 200
    x1 = 3
    x2 = 991
    y = 175
    for i in range(7):
        canvas.create_line(x1,y,x2,y,width=4)
        y += 90
        if(i == 3):
            x2 = 805
    canvas.create_line(990,81,990,445,width = 4)

def notify_me():
    stats = getIndianDetails()
    mess = ''
    for i in [1,3,5,7]:
        mess = mess + stats[i] + " : "+stats[i+1] +'\n'
    while True :
        plyer.notification.notify(
            title = "COVID-19 STATS : ",
            message = mess,
            timeout = 10,
            app_icon = "icon.ico"
        )
        time.sleep(20)

def main():
    root = Tk()
    root.title(getIndianDetails()[0])
    root.iconbitmap("icon.ico")
    canvas = Canvas(root, height=717, width =992)
    time  = Label(root, text="Last\nRefreshed on :\n" + str(getTime()), fg="black", font="Verdana 15 ")
    time.place(x=815, y=500)
    button= Button(root, text="Refresh", justify='right',bg = '#38dcf5' , font="Verdana 15 bold",command = lambda: refresh(root,time))
    button.place(x=845, y=640, height=40, width=100)
    createTable(canvas)
    makeHeader(root)
    makeStates(root)
    canvas.pack()
    th = threading.Thread(target= notify_me)
    th.setDaemon(TRUE)
    th.start()
    root.mainloop()


if __name__ == "__main__":
    getTime()
    main()