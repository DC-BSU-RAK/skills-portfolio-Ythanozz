import tkinter as tk
from tkinter import messagebox
import random
import time
import math

class CasinoArithmeticQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Casino Math Challenge")
        self.root.geometry("700x500")
        self.root.configure(bg='#2d2d2d')  # Grey background
        
        # Game variables
        self.score = 0
        self.current_question = 0
        self.difficulty = "easy"
        self.time_left = 20
        self.spins_available = 0
        self.timer_id = None  # Store timer ID to cancel it
        
        self.setup_welcome_screen()
    
    def generate_question(self, difficulty):
        """Generate a question based on difficulty"""
        if difficulty == "easy":
            a, b = random.randint(1, 20), random.randint(1, 20)
            if random.choice([True, False]):
                return f"{a} + {b} = ?", a + b
            else:
                return f"{a} - {b} = ?", a - b
        elif difficulty == "medium":
            a, b = random.randint(2, 12), random.randint(2, 12)
            return f"{a} × {b} = ?", a * b
        else:  # hard
            a, b = random.randint(2, 15), random.randint(2, 15)
            return f"{a * b} ÷ {a} = ?", b
    
    def generate_options(self, correct_answer):
        """Generate multiple choice options"""
        options = [correct_answer]
        while len(options) < 4:
            wrong = correct_answer + random.randint(1, 10) * random.choice([-1, 1])
            if wrong > 0 and wrong not in options:
                options.append(wrong)
        random.shuffle(options)
        return options
    
    def setup_welcome_screen(self):
        """Welcome screen"""
        self.clear_screen()
        
        tk.Label(self.root, text="🎰 Casino Math Challenge 🎰", 
                font=('Arial', 20, 'bold'), 
                fg='#ffd700',  # Yellow text
                bg='#2d2d2d').pack(pady=30)  # Grey background
        
        tk.Label(self.root, text="Answer math questions to earn spins!\n\n• 10 questions total\n• Timer gets faster\n• Wheel decides your fate!",
                font=('Arial', 12), 
                fg='#ffd700',  # Yellow text
                bg='#2d2d2d').pack(pady=20)  # Grey background
        
        tk.Button(self.root, text="Start Game", font=('Arial', 14), bg='red', fg='white',
                 command=self.setup_difficulty_selection, padx=20, pady=10).pack(pady=20)
    
    def setup_difficulty_selection(self):
        """Difficulty selection"""
        self.clear_screen()
        
        tk.Label(self.root, text="Choose Difficulty", 
                font=('Arial', 18, 'bold'), 
                fg='#ffd700',  # Yellow text
                bg='#2d2d2d').pack(pady=30)  # Grey background
        
        for text, difficulty, color in [
            ("🎯 Easy", "easy", 'green'),
            ("⚡ Medium", "medium", 'orange'),
            ("🔥 Hard", "hard", 'red')
        ]:
            tk.Button(self.root, text=text, font=('Arial', 12), bg=color, fg='white',
                     command=lambda d=difficulty: self.start_game(d), width=15).pack(pady=10)
    
    def start_game(self, difficulty):
        """Start the game"""
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.spins_available = 0
        self.show_question()
    
    def show_question(self):
        """Show current question"""
        try:
            self.clear_screen()
            self.current_question += 1
            
            # Determine actual difficulty
            if self.current_question <= 5 or self.current_question == 10:
                actual_difficulty = "easy"
            else:
                actual_difficulty = self.difficulty
            
            question_text, correct_answer = self.generate_question(actual_difficulty)
            options = self.generate_options(correct_answer)
            
            # Header
            tk.Label(self.root, text=f"Question {self.current_question}/10 | Score: {self.score}", 
                    font=('Arial', 14), 
                    fg='#ffd700',  # Yellow text
                    bg='#2d2d2d').pack(pady=10)  # Grey background
            
            # Timer
            self.time_left = max(5, 20 - (self.current_question - 1) * 2)
            self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}s", 
                                       font=('Arial', 12), 
                                       fg='red', 
                                       bg='#2d2d2d')  # Grey background
            self.timer_label.pack()
            
            # Question
            tk.Label(self.root, text=question_text, 
                    font=('Arial', 20, 'bold'), 
                    fg='#ffd700',  # Yellow text
                    bg='#2d2d2d').pack(pady=20)  # Grey background
            
            # Options
            for option in options:
                tk.Button(self.root, text=str(option), font=('Arial', 12), bg='darkblue', fg='white',
                         command=lambda opt=option: self.check_answer(opt, correct_answer), width=10).pack(pady=5)
            
            self.timer_running = True
            self.update_timer()
            
        except Exception as e:
            print(f"Error in show_question: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def update_timer(self):
        """Update timer"""
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.timer_running = False
            self.show_result(False, "Time's up!")
    
    def check_answer(self, selected, correct):
        """Check if answer is correct"""
        try:
            # Stop the timer
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            
            is_correct = selected == correct
            
            if is_correct:
                self.score += 1
                self.spins_available += 1
            
            self.show_result(is_correct, f"Correct answer: {correct}")
            
        except Exception as e:
            print(f"Error in check_answer: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def show_result(self, is_correct, message):
        """Show result popup"""
        try:
            if is_correct:
                messagebox.showinfo("Result", "✅ Correct!")
            else:
                messagebox.showinfo("Result", f"❌ Wrong!\n{message}")
            
            # Move to next question or wheel spin
            if self.current_question == 5:
                self.spin_wheel_midgame()
            elif self.current_question == 10:
                self.final_wheel_spin()
            else:
                self.show_question()
                
        except Exception as e:
            print(f"Error in show_result: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def spin_wheel_midgame(self):
        """Mid-game wheel spin"""
        try:
            self.clear_screen()
            self.spins_available = max(1, self.spins_available)
            
            tk.Label(self.root, text="🎰 SPIN THE WHEEL! 🎰", 
                    font=('Arial', 18, 'bold'), 
                    fg='#ffd700',  # Yellow text
                    bg='#2d2d2d').pack(pady=20)  # Grey background
            
            tk.Label(self.root, text=f"Spins: {self.spins_available}", 
                    font=('Arial', 14),
                    fg='#ffd700',  # Yellow text
                    bg='#2d2d2d').pack()  # Grey background
            
            self.wheel_canvas = tk.Canvas(self.root, width=300, height=300, bg='#2d2d2d')  # Grey background
            self.wheel_canvas.pack(pady=20)
            
            tk.Button(self.root, text="SPIN!", font=('Arial', 14), bg='red', fg='white',
                     command=self.do_midgame_spin).pack()
            
            self.draw_wheel_midgame()
            
        except Exception as e:
            print(f"Error in spin_wheel_midgame: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def draw_wheel_midgame(self):
        """Draw mid-game wheel"""
        try:
            self.wheel_canvas.delete("all")
            center_x, center_y, radius = 150, 150, 120
            
            segments = [("EASY", 'green'), ("MEDIUM", 'orange'), ("HARD", 'red')] * 4
            
            for i, (text, color) in enumerate(segments):
                start_angle = i * 30
                self.wheel_canvas.create_arc(center_x-radius, center_y-radius, center_x+radius, center_y+radius,
                                            start=start_angle, extent=30, fill=color, outline='gold')
            
            self.wheel_canvas.create_polygon(center_x, center_y-radius-15, center_x-10, center_y-radius, 
                                            center_x+10, center_y-radius, fill='gold')
            
        except Exception as e:
            print(f"Error in draw_wheel_midgame: {e}")
    
    def do_midgame_spin(self):
        """Simple spin without animation"""
        try:
            result = random.choice(["easy", "medium", "hard"])
            self.difficulty = result
            self.spins_available -= 1
            
            if self.spins_available > 0:
                messagebox.showinfo("Result", f"Difficulty: {result.upper()}!\n{self.spins_available} spin(s) left!")
                self.spin_wheel_midgame()
            else:
                messagebox.showinfo("Result", f"Next difficulty: {result.upper()}!")
                self.show_question()
                
        except Exception as e:
            print(f"Error in do_midgame_spin: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def final_wheel_spin(self):
        """Final wheel spin"""
        try:
            self.clear_screen()
            final_spins = max(1, self.score - 5)
            
            tk.Label(self.root, text="🎰 FINAL WHEEL! 🎰", 
                    font=('Arial', 18, 'bold'), 
                    fg='#ffd700',  # Yellow text
                    bg='#2d2d2d').pack(pady=20)  # Grey background
            
            tk.Label(self.root, text=f"Score: {self.score}/10 | Spins: {final_spins}", 
                    font=('Arial', 14),
                    fg='#ffd700',  # Yellow text
                    bg='#2d2d2d').pack()  # Grey background
            
            self.final_wheel_canvas = tk.Canvas(self.root, width=300, height=300, bg='#2d2d2d')  # Grey background
            self.final_wheel_canvas.pack(pady=20)
            
            tk.Button(self.root, text="SPIN!", font=('Arial', 14), bg='red', fg='white',
                     command=lambda: self.do_final_spin(final_spins)).pack()
            
            self.draw_final_wheel()
            self.final_results = []
            
        except Exception as e:
            print(f"Error in final_wheel_spin: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def draw_final_wheel(self):
        """Draw final wheel"""
        try:
            self.final_wheel_canvas.delete("all")
            center_x, center_y, radius = 150, 150, 120
            
            segments = [("WIN", 'green'), ("LOSE", 'red')] * 6
            
            for i, (text, color) in enumerate(segments):
                start_angle = i * 30
                self.final_wheel_canvas.create_arc(center_x-radius, center_y-radius, center_x+radius, center_y+radius,
                                                  start=start_angle, extent=30, fill=color, outline='gold')
            
            self.final_wheel_canvas.create_polygon(center_x, center_y-radius-15, center_x-10, center_y-radius, 
                                                  center_x+10, center_y-radius, fill='gold')
            
        except Exception as e:
            print(f"Error in draw_final_wheel: {e}")
    
    def do_final_spin(self, spins_left):
        """Simple final spin without animation"""
        try:
            result = random.choice(["WIN", "LOSE"])
            self.final_results.append(result)
            spins_left -= 1
            
            if spins_left > 0:
                messagebox.showinfo("Result", f"{result}!\n{spins_left} spin(s) left!")
                self.do_final_spin(spins_left)
            else:
                wins = self.final_results.count("WIN")
                if wins > len(self.final_results) // 2:
                    self.show_final_result("VICTORY! 🎉", 
                                         f"You won {wins} out of {len(self.final_results)} spins!\nCongratulations, high roller!",
                                         '#2ecc71')  # Green background
                else:
                    self.show_final_result("DEFEAT! 💀", 
                                         f"You won {wins} out of {len(self.final_results)} spins.\nBetter luck next time!",
                                         '#e74c3c')  # Red background
                
        except Exception as e:
            print(f"Error in do_final_spin: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def show_final_result(self, title, message, color):
        """Show final result with quit button"""
        try:
            self.clear_screen()
            
            # Main result frame
            result_frame = tk.Frame(self.root, bg=color)
            result_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Title
            tk.Label(result_frame, text=title, 
                    font=('Arial', 24, 'bold'), 
                    fg='white', 
                    bg=color).pack(pady=20)
            
            # Message
            tk.Label(result_frame, text=message, 
                    font=('Arial', 14), 
                    fg='white', 
                    bg=color,
                    justify='center').pack(pady=10)
            
            # Final score
            tk.Label(result_frame, text=f"Final Score: {self.score}/10", 
                    font=('Arial', 16, 'bold'), 
                    fg='white', 
                    bg=color).pack(pady=10)
            
            # Button frame
            button_frame = tk.Frame(result_frame, bg=color)
            button_frame.pack(pady=30)
            
            # Play Again button
            tk.Button(button_frame, text="Play Again", 
                     font=('Arial', 14, 'bold'),
                     bg='#f39c12',  # Orange
                     fg='black',
                     command=self.setup_welcome_screen,
                     padx=20, pady=10).pack(side='left', padx=10)
            
            # Quit button - properly closes the application
            tk.Button(button_frame, text="Quit Game", 
                     font=('Arial', 14, 'bold'),
                     bg='#e74c3c',  # Red
                     fg='white',
                     command=self.quit_game,
                     padx=20, pady=10).pack(side='left', padx=10)
            
        except Exception as e:
            print(f"Error in show_final_result: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def quit_game(self):
        """Properly quit the game"""
        try:
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error quitting game: {e}")
    
    def clear_screen(self):
        """Clear all widgets"""
        try:
            # Stop any running timer
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            
            # Clear all widgets
            for widget in self.root.winfo_children():
                widget.destroy()
                
        except Exception as e:
            print(f"Error in clear_screen: {e}")
    
    def run(self):
        """Start the game"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error in main loop: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

# Run the game
if __name__ == "__main__":
    try:
        game = CasinoArithmeticQuiz()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror("Error", f"A fatal error occurred: {e}")