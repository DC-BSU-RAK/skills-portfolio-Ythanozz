import tkinter as tk
from tkinter import ttk, messagebox
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("600x400")
        self.root.configure(bg='black')
        
        #Used Same structure of loading data with exercise 2
        self.students = self.load_student_data()
        
        #Create main menu
        self.create_main_menu()
    
    def load_student_data(self):
        """Load student data from the text file using the same path as your joke app"""
        try:
            file_path = r"C:\Users\ythan\OneDrive\Documents\GitHub\skills-portfolio-Ythanozz\Assessment 1 - Skills Portfolio\A1 - Resources\studentMarks.txt"
            
            #Show the path being used for debugging
            print(f"Looking for file at: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            students = []
            num_students = int(lines[0].strip())
            
            for i in range(1, num_students + 1):
                data = lines[i].strip().split(',')
                student_code = int(data[0])
                student_name = data[1]
                course_marks = [int(data[2]), int(data[3]), int(data[4])]
                exam_mark = int(data[5])
                
                #Calculate total coursework mark (sum of 3 course marks)
                total_coursework = sum(course_marks)
                
                #Calculate overall percentage (out of 160 total marks)
                overall_percentage = (total_coursework + exam_mark) / 160 * 100
                
                #Determine grade
                if overall_percentage >= 70:
                    grade = 'A'
                elif overall_percentage >= 60:
                    grade = 'B'
                elif overall_percentage >= 50:
                    grade = 'C'
                elif overall_percentage >= 40:
                    grade = 'D'
                else:
                    grade = 'F'
                
                student = {
                    'code': student_code,
                    'name': student_name,
                    'course_marks': course_marks,
                    'exam_mark': exam_mark,
                    'total_coursework': total_coursework,
                    'overall_percentage': overall_percentage,
                    'grade': grade
                }
                students.append(student)
            
            messagebox.showinfo("Success", f"Successfully loaded {len(students)} students from file!")
            return students
            
        except FileNotFoundError:
            messagebox.showerror("File Not Found", 
                                 f"File not found at:\n{file_path}\n\nPlease make sure the studentMarks.txt file exists in the correct location.")
            return []
        except Exception as e:
            messagebox.showerror("File Error", 
                                 f"Error reading file:\n{str(e)}\n\nPlease check the file format and try again.")
            return []
    
    def create_main_menu(self):
        """Create the main menu with buttons"""
        #Title
        title_label = tk.Label(self.root, text="Student Manager", 
                              font=('Arial', 20, 'bold'),
                              fg='cyan', bg='black')
        title_label.pack(pady=20)
        
        #Status label
        if self.students:
            status_text = f"Loaded {len(self.students)} students"
            status_color = 'yellow'
        else:
            status_text = "No data loaded - file not found"
            status_color = 'red'
            
        status_label = tk.Label(self.root, text=status_text,
                               font=('Arial', 12),
                               fg=status_color,
                               bg='black')
        status_label.pack(pady=5)
        
        #Buttons frame
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(expand=True)
        
        #Button styles
        button_style = {
            'font': ('Arial', 14),
            'width': 25,
            'height': 2,
            'bg': 'black',
            'fg': 'cyan',
            'relief': 'raised',
            'bd': 3
        }
        
        #Create buttons
        btn1 = tk.Button(button_frame, text="View All Student Records", 
                        command=self.view_all_records, **button_style)
        btn1.pack(pady=10)
        
        btn2 = tk.Button(button_frame, text="View Individual Student Record", 
                        command=self.view_individual_record, **button_style)
        btn2.pack(pady=10)
        
        btn3 = tk.Button(button_frame, text="Show Student with Highest Score", 
                        command=self.show_highest_score, **button_style)
        btn3.pack(pady=10)
        
        btn4 = tk.Button(button_frame, text="Show Student with Lowest Score", 
                        command=self.show_lowest_score, **button_style)
        btn4.pack(pady=10)
    
    def create_window(self, title):
        """Create a new window with consistent styling"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("800x600")
        window.configure(bg='black')
        return window
    
    def view_all_records(self):
        """Display all student records in a table"""
        if not self.students:
            messagebox.showwarning("No Data", "No student data available! Please make sure the studentMarks.txt file exists.")
            return
        
        window = self.create_window("All Student Records")
        
        #Create frame for table
        table_frame = tk.Frame(window, bg='black')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        #Create treeview widget
        columns = ('Name', 'Number', 'Coursework', 'Exam', 'Percentage', 'Grade')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        #Define headings
        tree.heading('Name', text='Student Name')
        tree.heading('Number', text='Student Number')
        tree.heading('Coursework', text='Total Coursework')
        tree.heading('Exam', text='Exam Mark')
        tree.heading('Percentage', text='Overall Percentage')
        tree.heading('Grade', text='Grade')
        
        #Configure column widths
        tree.column('Name', width=120)
        tree.column('Number', width=100)
        tree.column('Coursework', width=100)
        tree.column('Exam', width=80)
        tree.column('Percentage', width=120)
        tree.column('Grade', width=80)
        
        #Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        #Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        #Insert data
        total_percentage = 0
        for student in self.students:
            tree.insert('', tk.END, values=(
                student['name'],
                student['code'],
                student['total_coursework'],
                student['exam_mark'],
                f"{student['overall_percentage']:.2f}%",
                student['grade']
            ))
            total_percentage += student['overall_percentage']
        
        #Calculate average
        avg_percentage = total_percentage / len(self.students)
        
        #Summary frame
        summary_frame = tk.Frame(window, bg='black', relief='raised', bd=2)
        summary_frame.pack(fill='x', padx=10, pady=10)
        
        summary_text = f"Number of students: {len(self.students)} | Average percentage: {avg_percentage:.2f}%"
        summary_label = tk.Label(summary_frame, text=summary_text, 
                                font=('Arial', 12, 'bold'),
                                fg='yellow', bg='black')
        summary_label.pack(pady=10)
    
    def view_individual_record(self):
        """Display individual student record based on search"""
        if not self.students:
            messagebox.showwarning("No Data", "No student data available! Please make sure the studentMarks.txt file exists.")
            return
        
        window = self.create_window("Individual Student Record")
        
        #Main container frame to center everything
        main_container = tk.Frame(window, bg='black')
        main_container.pack(expand=True, fill='both')
        
        #Search frame - centered
        search_frame = tk.Frame(main_container, bg='black', relief='raised', bd=2)
        search_frame.pack(expand=True, pady=50)
        
        #Label centered
        tk.Label(search_frame, text="Enter Student Name or Number:", 
                font=('Arial', 14), fg='cyan', bg='black').pack(pady=20)
        
        #Entry centered
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, 
                               font=('Arial', 12), width=30, bg='white', fg='black',
                               insertbackground='black', relief='solid', bd=1)
        search_entry.pack(pady=10)
        
        #Search button centered
        search_btn = tk.Button(search_frame, text="Search", 
                              command=lambda: self.perform_search(search_var.get().strip(), result_frame, window),
                              font=('Arial', 12), bg='black', fg='cyan',
                              relief='raised', bd=3, width=15)
        search_btn.pack(pady=20)
        
        #Result frame at bottom
        result_frame = tk.Frame(window, bg='black')
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        #Bind Enter key to search
        search_entry.bind('<Return>', lambda event: self.perform_search(search_var.get().strip(), result_frame, window))
    
    def perform_search(self, search_term, result_frame, window):
        """Perform the student search and display results"""
        #Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()
        
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a student name or number!")
            return
        
        found_students = []
        
        #Search by name or code
        for student in self.students:
            if (search_term.lower() in student['name'].lower() or 
                search_term == str(student['code'])):
                found_students.append(student)
        
        if not found_students:
            #Center the "No student found" message
            no_result_frame = tk.Frame(result_frame, bg='black')
            no_result_frame.pack(expand=True, fill='both')
            tk.Label(no_result_frame, text="No student found!", 
                    font=('Arial', 16), fg='red', bg='black').pack(expand=True)
            return
        
        #Display results centered
        for student in found_students:
            student_frame = tk.Frame(result_frame, bg='black', relief='raised', bd=2)
            student_frame.pack(fill='x', pady=5, padx=50)
            
            info_text = (
                f"Name: {student['name']}\n"
                f"Student Number: {student['code']}\n"
                f"Coursework Marks: {student['course_marks']} (Total: {student['total_coursework']})\n"
                f"Exam Mark: {student['exam_mark']}\n"
                f"Overall Percentage: {student['overall_percentage']:.2f}%\n"
                f"Grade: {student['grade']}"
            )
            
            #Center the student info
            info_label = tk.Label(student_frame, text=info_text, font=('Arial', 12),
                                justify=tk.CENTER, fg='white', bg='black')
            info_label.pack(padx=20, pady=15)
    
    def show_highest_score(self):
        """Display student with highest overall score"""
        if not self.students:
            messagebox.showwarning("No Data", "No student data available! Please make sure the studentMarks.txt file exists.")
            return
        
        window = self.create_window("Highest Scoring Student")
        
        #Find student with highest percentage
        highest_student = max(self.students, key=lambda x: x['overall_percentage'])
        
        self.display_student_result(window, highest_student, "HIGHEST")
    
    def show_lowest_score(self):
        """Display student with lowest overall score"""
        if not self.students:
            messagebox.showwarning("No Data", "No student data available! Please make sure the studentMarks.txt file exists.")
            return
        
        window = self.create_window("Lowest Scoring Student")
        
        #Find student with lowest percentage
        lowest_student = min(self.students, key=lambda x: x['overall_percentage'])
        
        self.display_student_result(window, lowest_student, "LOWEST")
    
    def display_student_result(self, window, student, score_type):
        """Display student information in a formatted way"""
        #Title
        title_color = 'green' if score_type == "HIGHEST" else 'red'
        title_text = f"Student with {score_type.lower()} overall mark:"
        
        tk.Label(window, text=title_text, font=('Arial', 16, 'bold'),
                fg=title_color, bg='black').pack(pady=20)
        
        #Student info frame
        info_frame = tk.Frame(window, bg='black', relief='raised', bd=3)
        info_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        #Student details
        details = [
            f"Name: {student['name']}",
            f"Student Number: {student['code']}",
            f"Coursework Marks: {student['course_marks']}",
            f"Total Coursework: {student['total_coursework']}/60",
            f"Exam Mark: {student['exam_mark']}/100",
            f"Overall Percentage: {student['overall_percentage']:.2f}%",
            f"Grade: {student['grade']}"
        ]
        
        for detail in details:
            tk.Label(info_frame, text=detail, font=('Arial', 14),
                    fg='white', bg='black', justify=tk.LEFT).pack(anchor='w', padx=20, pady=8)

def main():
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()