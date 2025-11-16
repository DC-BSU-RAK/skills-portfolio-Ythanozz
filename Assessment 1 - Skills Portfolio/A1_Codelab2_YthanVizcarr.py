import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import math

class CasinoArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Arithmetic Challenge")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        #Game variables
        self.difficulty = "easy"
        self.current_question = 0
        self.score = 0
        self.spins = 0
        self.total_questions = 10
        self.time_left = 20
        self.timer_running = False
        self.selected_difficulty = None
        self.questions = []
        self.user_answer = tk.StringVar()
        self.timer_id = None
        
        #Color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'red': '#dc3545',
            'black': '#2d2d2d',
            'gold': '#ffd700',
            'text': 'white',
            'button_bg': '#dc3545',
            'button_fg': 'white'
        }
        
        #Font definitions
        self.title_font = ('Dank Mono', 24, 'bold')
        self.subtitle_font = ('Punk Mono', 14)
        self.difficulty_font = ('Punk Mono', 16, 'bold')
        self.button_font = ('Punk Mono', 12, 'bold')
        self.question_font = ('Punk Mono', 28, 'bold')
        self.timer_font = ('Punk Mono', 20, 'bold')
        self.score_font = ('Punk Mono', 16, 'bold')
        self.option_font = ('Punk Mono', 18, 'bold')
        self.result_font = ('Punk Mono', 20, 'bold')
        self.wheel_font = ('Punk Mono', 12, 'bold')
        self.final_wheel_font = ('Punk Mono', 14, 'bold')
        
        self.create_main_menu()
    
    def create_main_menu(self):
        self.clear_screen()
        
        title = tk.Label(self.root, text="🎰 CASINO ARITHMETIC CHALLENGE 🎰", 
                        font=self.title_font, 
                        fg=self.colors['gold'], 
                        bg=self.colors['bg'])
        title.pack(pady=50)
        
        subtitle = tk.Label(self.root, text="Test your math skills in this high-stakes casino game!", 
                           font=self.subtitle_font, 
                           fg=self.colors['text'], 
                           bg=self.colors['bg'])
        subtitle.pack(pady=10)
        
        #Difficulty selection
        diff_frame = tk.Frame(self.root, bg=self.colors['bg'])
        diff_frame.pack(pady=30)
        
        tk.Label(diff_frame, text="Choose Your Difficulty:", 
                font=self.difficulty_font, 
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(pady=10)
        
        difficulties = [("Easy 🎯", "easy"), ("Medium ⚡", "medium"), ("Hard 💀", "hard")]
        
        for text, difficulty in difficulties:
            btn = tk.Button(diff_frame, text=text, 
                          font=self.button_font,
                          bg=self.colors['button_bg'],
                          fg=self.colors['button_fg'],
                          width=15, height=2,
                          command=lambda d=difficulty: self.start_game(d))
            btn.pack(pady=5)
    
    def start_game(self, difficulty):
        self.selected_difficulty = difficulty
        self.difficulty = "easy"  # First 5 questions are always easy
        self.current_question = 0
        self.score = 0
        self.spins = 0
        self.time_left = 20
        self.generate_questions()
        self.show_question()
    
    def generate_questions(self):
        self.questions = []
        
        #First 5 questions (always easy)
        for i in range(5):
            self.questions.append(self.generate_question("easy"))
        
        #Next 4 questions based on selected difficulty
        for i in range(4):
            self.questions.append(self.generate_question(self.selected_difficulty))
        
        #Last question (always easy)
        self.questions.append(self.generate_question("easy"))
    
    def generate_question(self, difficulty):
        if difficulty == "easy":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            operation = random.choice(['+', '-'])
        elif difficulty == "medium":
            a = random.randint(10, 50)
            b = random.randint(10, 50)
            operation = random.choice(['+', '-', '*'])
        else:  # hard
            a = random.randint(20, 100)
            b = random.randint(1, 20)
            operation = random.choice(['*', '/'])
        
        if operation == '+':
            answer = a + b
            question = f"{a} + {b} = ?"
        elif operation == '-':
            answer = a - b
            question = f"{a} - {b} = ?"
        elif operation == '*':
            answer = a * b
            question = f"{a} × {b} = ?"
        else:  # division
            answer = a
            question = f"{a * b} ÷ {b} = ?"
        
        #Generate wrong answers
        wrong_answers = []
        while len(wrong_answers) < 3:
            wrong = answer + random.choice([-5, -3, -2, 2, 3, 5])
            if wrong != answer and wrong not in wrong_answers and wrong > 0:
                wrong_answers.append(wrong)
        
        all_answers = wrong_answers + [answer]
        random.shuffle(all_answers)
        
        return {
            'question': question,
            'answer': answer,
            'options': all_answers,
            'difficulty': difficulty
        }
    
    def show_question(self):
        self.clear_screen()
        
        if self.current_question >= len(self.questions):
            self.show_final_wheel()
            return
        
        #Check if it's time for the wheel spin
        if self.current_question == 5:
            self.show_wheel_spin()
            return
        
        question_data = self.questions[self.current_question]
        
        #Header
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=10)
        
        tk.Label(header_frame, text=f"Question {self.current_question + 1}/10", 
                font=self.score_font, 
                fg=self.colors['gold'], 
                bg=self.colors['bg']).pack(side='left', padx=20)
        
        tk.Label(header_frame, text=f"Score: {self.score}", 
                font=self.score_font, 
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(side='right', padx=20)
        
        #Timer
        self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}s", 
                                   font=self.timer_font, 
                                   fg=self.colors['red'], 
                                   bg=self.colors['bg'])
        self.timer_label.pack(pady=10)
        
        #Question
        question_label = tk.Label(self.root, text=question_data['question'], 
                                 font=self.question_font, 
                                 fg=self.colors['text'], 
                                 bg=self.colors['bg'])
        question_label.pack(pady=30)
        
        #Answer buttons
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        colors = ['#dc3545', '#28a745', '#007bff', '#ffc107']
        
        for i, option in enumerate(question_data['options']):
            btn = tk.Button(button_frame, text=str(option), 
                          font=self.option_font,
                          bg=colors[i],
                          fg='white',
                          width=8, height=2,
                          command=lambda opt=option: self.check_answer(opt))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
        
        self.start_timer()
    
    def start_timer(self):
        self.time_left = max(20 - (self.current_question * 2), 5)  # Decrease by 2 seconds per question
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}s")
            
            if self.time_left <= 0:
                self.timer_running = False
                self.show_result(False)
            else:
                self.timer_id = self.root.after(1000, self.update_timer)
    
    def check_answer(self, selected_answer):
        if self.timer_running:
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            
            correct_answer = self.questions[self.current_question]['answer']
            is_correct = (selected_answer == correct_answer)
            
            if is_correct:
                self.score += 1
                self.spins += 1
            else:
                self.spins = max(0, self.spins - 1)
            
            self.show_result(is_correct)
    
    def show_result(self, is_correct):
        result_window = tk.Toplevel(self.root)
        result_window.title("Result")
        result_window.geometry("300x200")
        result_window.configure(bg=self.colors['bg'])
        
        if is_correct:
            text = "🎉 CORRECT! 🎉"
            color = '#28a745'
            spin_text = f"+1 Spin! Total spins: {self.spins}"
        else:
            text = "❌ WRONG! ❌"
            color = '#dc3545'
            correct_answer = self.questions[self.current_question]['answer']
            spin_text = f"-1 Spin! Total spins: {max(0, self.spins)}"
        
        tk.Label(result_window, text=text, 
                font=self.result_font, 
                fg=color, 
                bg=self.colors['bg']).pack(pady=20)
        
        tk.Label(result_window, text=spin_text, 
                font=self.subtitle_font, 
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(pady=10)
        
        tk.Button(result_window, text="Continue", 
                 font=self.button_font,
                 bg=self.colors['button_bg'],
                 fg=self.colors['button_fg'],
                 command=lambda: self.next_question(result_window)).pack(pady=20)
    
    def next_question(self, window):
        window.destroy()
        self.current_question += 1
        self.show_question()
    
    def show_wheel_spin(self):
        self.clear_screen()
        
        #Ensure at least 1 spin
        self.spins = max(1, self.spins)
        
        header = tk.Label(self.root, text="🎰 SPIN THE WHEEL! 🎰", 
                         font=self.title_font, 
                         fg=self.colors['gold'], 
                         bg=self.colors['bg'])
        header.pack(pady=20)
        
        spins_label = tk.Label(self.root, text=f"You have {self.spins} spin(s)!", 
                              font=self.score_font, 
                              fg=self.colors['text'], 
                              bg=self.colors['bg'])
        spins_label.pack(pady=10)
        
        #Create wheel canvas
        self.wheel_canvas = tk.Canvas(self.root, width=400, height=400, bg=self.colors['bg'], highlightthickness=0)
        self.wheel_canvas.pack(pady=20)
        
        self.draw_wheel()
        
        spin_button = tk.Button(self.root, text="SPIN! 🎰", 
                               font=self.button_font,
                               bg=self.colors['red'],
                               fg='white',
                               width=15, height=2,
                               command=self.animate_wheel)
        spin_button.pack(pady=20)
    
    def draw_wheel(self, angle=0):
        self.wheel_canvas.delete("all")
        
        center_x, center_y, radius = 200, 200, 150
        
        #Draw wheel
        segments = 8
        colors = ['#dc3545', '#2d2d2d'] * 4
        labels = ['MEDIUM', 'HARD'] * 4
        
        for i in range(segments):
            start_angle = angle + (i * 360/segments)
            end_angle = angle + ((i + 1) * 360/segments)
            
            # Draw segment
            self.wheel_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=360/segments,
                fill=colors[i], outline='gold', width=3
            )
            
            #Draw label
            mid_angle = math.radians(start_angle + 360/(segments*2))
            label_radius = radius * 0.7
            label_x = center_x + label_radius * math.cos(mid_angle)
            label_y = center_y + label_radius * math.sin(mid_angle)
            
            self.wheel_canvas.create_text(
                label_x, label_y,
                text=labels[i],
                fill='white',
                font=self.wheel_font,
                angle=start_angle + 360/(segments*2)
            )
        
        #Draw center
        self.wheel_canvas.create_oval(center_x-10, center_y-10, center_x+10, center_y+10, fill='gold', outline='gold')
        
        #Draw pointer
        self.wheel_canvas.create_polygon(
            center_x + radius + 10, center_y - 10,
            center_x + radius + 10, center_y + 10,
            center_x + radius + 30, center_y,
            fill='gold', outline='black'
        )
    
    def animate_wheel(self):
        self.spins -= 1
        spins = random.randint(5, 10)  # Number of full rotations
        
        def spin(remaining_spins, current_angle):
            if remaining_spins > 0:
                new_angle = (current_angle + 30) % 360
                self.draw_wheel(new_angle)
                self.root.after(50, lambda: spin(remaining_spins - 1, new_angle))
            else:
                # Determine result
                final_angle = current_angle % 360
                segment = int(final_angle / 45) % 8
                
                if segment % 2 == 0:
                    result = "MEDIUM"
                else:
                    result = "HARD"
                
                self.show_wheel_result(result)
        
        spin(spins * 12, 0)  # Start animation
    
    def show_wheel_result(self, result):
        result_window = tk.Toplevel(self.root)
        result_window.title("Wheel Result")
        result_window.geometry("400x200")
        result_window.configure(bg=self.colors['bg'])
        
        tk.Label(result_window, text=f"The wheel landed on: {result}!", 
                font=self.result_font, 
                fg=self.colors['gold'], 
                bg=self.colors['bg']).pack(pady=30)
        
        if self.spins > 0:
            tk.Label(result_window, text=f"You have {self.spins} spin(s) remaining!", 
                    font=self.subtitle_font, 
                    fg=self.colors['text'], 
                    bg=self.colors['bg']).pack(pady=10)
        
        tk.Button(result_window, text="Continue to Questions", 
                 font=self.button_font,
                 bg=self.colors['button_bg'],
                 fg=self.colors['button_fg'],
                 command=lambda: self.continue_after_wheel(result, result_window)).pack(pady=20)
    
    def continue_after_wheel(self, result, window):
        window.destroy()
        
        #Continue with questions
        self.current_question += 1
        self.show_question()
    
    def show_final_wheel(self):
        self.clear_screen()
        
        header = tk.Label(self.root, text="🎰 FINAL WHEEL - ALL OR NOTHING! 🎰", 
                         font=self.title_font, 
                         fg=self.colors['gold'], 
                         bg=self.colors['bg'])
        header.pack(pady=20)
        
        score_label = tk.Label(self.root, text=f"Final Score: {self.score}/10", 
                              font=self.score_font, 
                              fg=self.colors['text'], 
                              bg=self.colors['bg'])
        score_label.pack(pady=10)
        
        #Create final wheel canvas
        self.final_wheel_canvas = tk.Canvas(self.root, width=400, height=400, bg=self.colors['bg'], highlightthickness=0)
        self.final_wheel_canvas.pack(pady=20)
        
        self.draw_final_wheel()
        
        spin_button = tk.Button(self.root, text="FINAL SPIN! 🎲", 
                               font=self.button_font,
                               bg=self.colors['red'],
                               fg='white',
                               width=15, height=2,
                               command=self.animate_final_wheel)
        spin_button.pack(pady=20)
    
    def draw_final_wheel(self, angle=0):
        self.final_wheel_canvas.delete("all")
        
        center_x, center_y, radius = 200, 200, 150
        
        #Draw wheel with 50/50 chance
        segments = 2
        colors = ['#28a745', '#dc3545']  # Green for win, red for lose
        labels = ['YOU WIN!', 'YOU LOSE!']
        
        for i in range(segments):
            start_angle = angle + (i * 360/segments)
            end_angle = angle + ((i + 1) * 360/segments)
            
            self.final_wheel_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=360/segments,
                fill=colors[i], outline='gold', width=3
            )
            
            #Draw label
            mid_angle = math.radians(start_angle + 360/(segments*2))
            label_radius = radius * 0.7
            label_x = center_x + label_radius * math.cos(mid_angle)
            label_y = center_y + label_radius * math.sin(mid_angle)
            
            self.final_wheel_canvas.create_text(
                label_x, label_y,
                text=labels[i],
                fill='white',
                font=self.final_wheel_font,
                angle=start_angle + 360/(segments*2)
            )
        
        #Draw center
        self.final_wheel_canvas.create_oval(center_x-10, center_y-10, center_x+10, center_y+10, fill='gold', outline='gold')
        
        #Draw pointer
        self.final_wheel_canvas.create_polygon(
            center_x + radius + 10, center_y - 10,
            center_x + radius + 10, center_y + 10,
            center_x + radius + 30, center_y,
            fill='gold', outline='black'
        )
    
    def animate_final_wheel(self):
        spins = random.randint(5, 10)
        
        def spin(remaining_spins, current_angle):
            if remaining_spins > 0:
                new_angle = (current_angle + 30) % 360
                self.draw_final_wheel(new_angle)
                self.root.after(50, lambda: spin(remaining_spins - 1, new_angle))
            else:
                # 50% chance to win
                wins = random.random() < 0.5
                result = "YOU WIN!" if wins else "YOU LOSE!"
                self.show_final_result(result)
        
        spin(spins * 12, 0)
    
    def show_final_result(self, result):
        result_window = tk.Toplevel(self.root)
        result_window.title("Final Result")
        result_window.geometry("500x300")
        result_window.configure(bg=self.colors['bg'])
        
        if result == "YOU WIN!":
            text = "🎉 CONGRATULATIONS! YOU WIN! 🎉"
            color = '#28a745'
            message = f"You scored {self.score}/10 and beat the casino!"
        else:
            text = "💸 SORRY! YOU LOSE! 💸"
            color = '#dc3545'
            message = f"You scored {self.score}/10. Better luck next time!"
        
        tk.Label(result_window, text=text, 
                font=self.result_font, 
                fg=color, 
                bg=self.colors['bg']).pack(pady=30)
        
        tk.Label(result_window, text=message, 
                font=self.subtitle_font, 
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(pady=10)
        
        tk.Button(result_window, text="Play Again", 
                 font=self.button_font,
                 bg=self.colors['button_bg'],
                 fg=self.colors['button_fg'],
                 command=lambda: self.restart_game(result_window)).pack(pady=20)
    
    def restart_game(self, window):
        window.destroy()
        self.create_main_menu()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoArithmeticQuiz(root)
    root.mainloop()
