import tkinter as tk
import random
import pygame
from pygame import mixer
import os

class JokeTellingAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Assistant")
        self.root.geometry("300x250")
        self.root.configure(bg='#E6E6FA')
        
        mixer.init()
        self.jokes = self.load_jokes()
        self.create_main_window()
    
    def load_jokes(self):
        try:
            file_path = r"C:\Users\ythan\OneDrive\Documents\GitHub\skills-portfolio-Ythanozz\Assessment 1 - Skills Portfolio\A1 - Resources\randomJokes.txt"
            with open(file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except:
            return []
    
    def create_main_window(self):
        tk.Label(self.root, text="Alexa, tell me a joke.", font=('Arial', 12), 
                bg='#E6E6FA', fg='#4B0082').pack(pady=20)
        
        tk.Button(self.root, text="TELL JOKE", font=('Arial', 12, 'bold'), 
                 bg='#FF6B6B', fg='white', width=12, command=self.tell_joke).pack(pady=15)
        
        tk.Button(self.root, text="QUIT", font=('Arial', 10), bg='#9370DB', fg='white',
                 command=self.root.quit).pack(side=tk.BOTTOM, pady=15)
    
    def tell_joke(self):
        if not self.jokes:
            return
        
        joke = random.choice(self.jokes)
        if '?' in joke:
            self.setup, self.punchline = joke.split('?', 1)
            self.setup += '?'  # Keep the question mark with the setup
        else:
            self.setup = joke
            self.punchline = "No punchline found"
        
        self.show_joke_window()
    
    def show_joke_window(self):
        window = tk.Toplevel(self.root)
        window.title("Joke Time!")
        window.geometry("400x300")
        window.configure(bg='#E6E6FA')
        
        bubble = tk.Frame(window, bg='white', relief='solid', bd=1)
        bubble.pack(pady=20, padx=20, fill='both', expand=True)
        
        tk.Label(bubble, text=self.setup, font=('Arial', 11), 
                bg='white', wraplength=300).pack(pady=30)
        
        button_frame = tk.Frame(window, bg='#E6E6FA')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Show Punchline", command=lambda: self.show_punchline(pl_label), 
                 bg='#6BCF7F', fg='white').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Next Joke", command=window.destroy, 
                 bg='#6BA3CF', fg='white').pack(side=tk.LEFT, padx=5)
        
        pl_label = tk.Label(window, text="", font=('Arial', 11, 'bold'), 
                           bg='#E6E6FA', fg='#FF8C42', wraplength=350)
        pl_label.pack(pady=10)
    
    def show_punchline(self, label):
        label.config(text=self.punchline)
        self.play_laugh()
    
    def play_laugh(self):
        try:
            audio_path = r"C:\Users\ythan\OneDrive\Documents\GitHub\skills-portfolio-Ythanozz\Assessment 1 - Skills Portfolio\A1 - Resources\SitcomLaugh.mp3"
            mixer.music.load(audio_path)
            mixer.music.play()
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTellingAssistant(root)
    root.mainloop()