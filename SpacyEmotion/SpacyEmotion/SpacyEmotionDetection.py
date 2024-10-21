import re
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
import matplotlib.pyplot as plt

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import numpy as np
import os
import pandas as pd

import spacy #importing SPACY text processing tool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

main = tkinter.Tk()
main.title("Emotion Detection using Twitter Datasets and Spacy Algorithm") #designing main screen
main.geometry("1300x1200")

spacy_model = spacy.load('en_core_web_sm') #loading SPACY with english language model and dictionary


global emotion_model, dataset, tweets
global neutral, positive, negative

def uploadDataset(): 
    global dataset
    filename = filedialog.askopenfilename(initialdir="TweetsDataset")
    dataset = pd.read_csv(filename, encoding='utf-8',nrows=200)
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n\n")
    text.insert(END,str(dataset.head()))

def Preprocessing():
    text.delete('1.0', END)
    global tweets, dataset
    tweets = []
    dataset = dataset.values
    for i in range(len(dataset)):
        msg = dataset[i,1]
        msg = re.sub('[^A-Za-z]+', ' ', msg)
        msg = msg.strip("\n").strip()
        msg = spacy_model(msg)
        msg = msg.text
        tweets.append(msg)
        text.insert(END,msg+"\n\n")
        text.update_idletasks()
    messagebox.showinfo("Preprocessing Task Completed", "Preprocessing Task Completed")        

def loadModel():
    global emotion_model
    text.delete('1.0', END)
    emotion_model = SentimentIntensityAnalyzer()
    text.insert(END,"Emotion Detection Model Loaded")


def detectEmotion():
    text.delete('1.0', END)
    global neutral, positive, negative, tweets, emotion_model
    neutral = 0
    positive = 0
    negative = 0
    for i in range(len(tweets)):
        sentiment_dict = emotion_model.polarity_scores(tweets[i].strip())
        compound = sentiment_dict['compound']
        if compound >= 0.05 : 
            result = 'Positive'
            positive = positive + 1
        elif compound <= - 0.05 : 
            result = 'Negative'
            negative = negative + 1
        else : 
            result = 'Neutral'
            neutral = neutral + 1
        text.insert(END,str(tweets[i])+" ====> EMOTION DETECTED AS : "+result+"\n\n")    

def emotionGraph():
    global neutral, positive, negative
    text.delete('1.0', END)

    plt.pie([positive, negative, neutral],labels=['Positive Tweets','Negative Tweets', 'Neutral Tweets'],autopct='%1.1f%%')
    plt.title('Tweets Emotion Graph')
    plt.axis('equal')
    plt.show()

def close():
    main.destroy()

font = ('times', 16, 'bold')
title = Label(main, text='Emotion Detection using Twitter Datasets and Spacy Algorithm')
title.config(bg='deep sky blue', fg='white')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=50,y=120)
text.config(font=font1)


font1 = ('times', 13, 'bold')
uploadButton = Button(main, text="Upload Tweets Dataset", command=uploadDataset)
uploadButton.place(x=50,y=550)
uploadButton.config(font=font1)  

processButton = Button(main, text="Preprocess Dataset using Spacy", command=Preprocessing)
processButton.place(x=400,y=550)
processButton.config(font=font1) 

emotionModelButton = Button(main, text="Load Emotion Detection Model", command=loadModel)
emotionModelButton.place(x=750,y=550)
emotionModelButton.config(font=font1) 

emotionDetectionButton = Button(main, text="Emotion Detection from Processed Tweets", command=detectEmotion)
emotionDetectionButton.place(x=50,y=600)
emotionDetectionButton.config(font=font1) 

graphButton = Button(main, text="Emotion Graph", command=emotionGraph)
graphButton.place(x=400,y=600)
graphButton.config(font=font1)

exitButton = Button(main, text="Exit", command=close)
exitButton.place(x=750,y=600)
exitButton.config(font=font1) 

main.config(bg='LightSteelBlue3')
main.mainloop()
