"""
IELTS Reading Application - Main Launcher
Provides a menu to launch different modules
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
import os


class MainLauncher:
    """Main application launcher window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("IELTS Reading Test Application")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.create_ui()
    
    def create_ui(self):
        """Create the launcher UI"""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="IELTS Reading Test", 
                font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)
        tk.Label(header, text="Comprehensive Test Preparation System", 
                font=('Arial', 12), bg='#2c3e50', fg='#ecf0f1').pack()
        
        # Main content
        content = tk.Frame(self.root, bg='#ecf0f1')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(content, text="Select a Module:", font=('Arial', 14, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        # Module buttons
        buttons_frame = tk.Frame(content, bg='#ecf0f1')
        buttons_frame.pack(expand=True)
        
        # Content Editor button
        editor_btn = tk.Button(buttons_frame, text="Content Editor",
                              command=self.launch_content_editor,
                              bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                              width=25, height=2, cursor='hand2')
        editor_btn.pack(pady=10)
        
        tk.Label(buttons_frame, text="Create and edit reading packages",
                font=('Arial', 10, 'italic'), bg='#ecf0f1', fg='#7f8c8d').pack()
        
        # Exam Engine button
        exam_btn = tk.Button(buttons_frame, text="Take Exam",
                            command=self.launch_exam_engine,
                            bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                            width=25, height=2, cursor='hand2')
        exam_btn.pack(pady=10)
        
        tk.Label(buttons_frame, text="Take a reading test with timing and scoring",
                font=('Arial', 10, 'italic'), bg='#ecf0f1', fg='#7f8c8d').pack()

        # Full IELTS (3 passages) button
        full_exam_btn = tk.Button(buttons_frame, text="Take Full IELTS Reading (3 Packages)",
                                  command=self.launch_full_reading_exam,
                                  bg='#16a085', fg='white', font=('Arial', 13, 'bold'),
                                  width=30, height=2, cursor='hand2')
        full_exam_btn.pack(pady=10)

        tk.Label(buttons_frame, text="Load exactly 3 package files and open each passage in its own screen",
                font=('Arial', 10, 'italic'), bg='#ecf0f1', fg='#7f8c8d').pack()
        
        # Sample Package button
        sample_btn = tk.Button(buttons_frame, text="Create Sample Package",
                              command=self.create_sample_package,
                              bg='#f39c12', fg='white', font=('Arial', 14, 'bold'),
                              width=25, height=2, cursor='hand2')
        sample_btn.pack(pady=10)
        
        tk.Label(buttons_frame, text="Generate a sample reading package for testing",
                font=('Arial', 10, 'italic'), bg='#ecf0f1', fg='#7f8c8d').pack()
        
        # Footer
        footer = tk.Frame(self.root, bg='#34495e', height=60)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        tk.Label(footer, text="© 2025 IELTS Reading Test Application", 
                font=('Arial', 10), bg='#34495e', fg='white').pack(pady=5)
        
        tk.Button(footer, text="Exit", command=self.root.quit,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 width=10).pack(pady=5)
    
    def launch_content_editor(self):
        """Launch the Content Editor module"""
        try:
            import content_editor
            editor_window = tk.Toplevel(self.root)
            content_editor.ContentEditorWindow(editor_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Content Editor:\n{str(e)}")
    
    def launch_exam_engine(self):
        """Launch the Exam Engine module"""
        try:
            import exam_engine
            exam_window = tk.Toplevel(self.root)
            exam_engine.ExamEngineWindow(exam_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Exam Engine:\n{str(e)}")
    
    def launch_full_reading_exam(self):
        """Launch one combined screen with 3 passages (questions left, reading right)."""
        filepaths = filedialog.askopenfilenames(
            title="Select exactly 3 Reading Package files",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not filepaths:
            return

        if len(filepaths) != 3:
            messagebox.showerror("Selection Error", "Please select exactly 3 package files.")
            return

        try:
            import exam_engine
            import uuid
            from models import ReadingPackage, ReadingContent, Paragraph

            packages = [ReadingPackage.load_from_file(path) for path in filepaths]

            merged_package = ReadingPackage()
            merged_package.package_id = str(uuid.uuid4())
            merged_package.reading_content = ReadingContent(
                explanation="You should spend about 20 minutes on each passage. Scroll to move between Passage 1, 2, and 3.",
                title="Full IELTS Reading Test (3 Passages)",
                paragraphs=[]
            )

            for i, pkg in enumerate(packages, start=1):
                merged_package.reading_content.paragraphs.append(
                    Paragraph(title=f"READING PASSAGE {i}: {pkg.reading_content.title}", body="")
                )
                for para in pkg.reading_content.paragraphs:
                    merged_package.reading_content.paragraphs.append(para)

                for qg in pkg.question_groups:
                    if qg.explanation:
                        qg.explanation = f"[Passage {i}]\n" + qg.explanation
                    else:
                        qg.explanation = f"[Passage {i}]"
                    merged_package.question_groups.append(qg)

            exam_window = tk.Toplevel(self.root)
            exam_window.title("IELTS Reading Exam - Full Test")
            exam_engine.ExamEngineWindow(exam_window, package=merged_package, questions_left=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch full reading exam:\n{str(e)}")

    def create_sample_package(self):
        """Create a sample reading package"""
        from tkinter import filedialog
        from models import (
            ReadingPackage, ReadingContent, Paragraph, 
            QuestionGroup, Question, QuestionType
        )
        import uuid
        
        # Create sample package
        package = ReadingPackage()
        package.package_id = str(uuid.uuid4())
        
        # Reading content
        rc = ReadingContent()
        rc.explanation = "You should spend about 20 minutes on Questions 1-13, which are based on the reading passage below."
        rc.title = "The History of the Bicycle"
        
        # Add paragraphs
        para1 = Paragraph()
        para1.title = "Early Developments"
        para1.body = """The bicycle has a long and fascinating history. The first verifiable claim for a 
practically used bicycle belongs to German inventor Karl von Drais. In 1817, he created a two-wheeled 
vehicle which was propelled by pushing one's feet against the ground. This early bicycle, known as the 
'running machine' or 'hobby horse', was made entirely of wood and had no pedals."""
        
        para2 = Paragraph()
        para2.title = "The Penny-Farthing Era"
        para2.body = """By the 1870s, bicycles had evolved significantly. The penny-farthing, with its 
large front wheel and small rear wheel, became popular among young men. The large wheel allowed for 
greater speed, but made the bicycle difficult and dangerous to ride. Mounting and dismounting required 
considerable skill, and falls were common."""
        
        para3 = Paragraph()
        para3.title = "The Safety Bicycle"
        para3.body = """The 1890s saw the introduction of the 'safety bicycle', which had two equal-sized 
wheels and a chain drive. This design, which is still used in modern bicycles, was much safer and easier 
to ride than the penny-farthing. The invention of pneumatic tires by John Boyd Dunlop in 1888 further 
improved comfort and performance."""
        
        rc.paragraphs = [para1, para2, para3]
        package.reading_content = rc
        
        # Question Group 1: Multiple Choice
        qg1 = QuestionGroup()
        qg1.type = QuestionType.TYPE1
        qg1.explanation = "Choose the correct letter, A, B, C or D."
        
        q1 = Question()
        q1.question_id = f"{package.package_id}_qg1_q1"
        q1.text = """Who invented the first practical bicycle?
A. Karl von Drais
B. John Boyd Dunlop
C. Pierre Lallement
D. Ernest Michaux"""
        q1.answer = "A"
        
        q2 = Question()
        q2.question_id = f"{package.package_id}_qg1_q2"
        q2.text = """What was the penny-farthing's main disadvantage?
A. It was too expensive
B. It was dangerous to ride
C. It was too heavy
D. It was too slow"""
        q2.answer = "B"
        
        qg1.questions = [q1, q2]
        
        # Question Group 2: True/False/Not Given
        qg2 = QuestionGroup()
        qg2.type = QuestionType.TYPE2
        qg2.explanation = "Do the following statements agree with the information in the passage? Write TRUE, FALSE, or NOT GIVEN."
        
        q3 = Question()
        q3.question_id = f"{package.package_id}_qg2_q1"
        q3.text = "The running machine had pedals"
        q3.answer = "FALSE"
        
        q4 = Question()
        q4.question_id = f"{package.package_id}_qg2_q2"
        q4.text = "The penny-farthing was popular among young men"
        q4.answer = "TRUE"
        
        q5 = Question()
        q5.question_id = f"{package.package_id}_qg2_q3"
        q5.text = "The safety bicycle was invented in France"
        q5.answer = "NOT GIVEN"
        
        qg2.questions = [q3, q4, q5]
        
        # Question Group 3: Short Answer
        qg3 = QuestionGroup()
        qg3.type = QuestionType.TYPE11
        qg3.explanation = "Answer the questions below using NO MORE THAN THREE WORDS from the passage."
        
        q6 = Question()
        q6.question_id = f"{package.package_id}_qg3_q1"
        q6.text = "What material was the running machine made from?"
        q6.answer = "wood"
        
        q7 = Question()
        q7.question_id = f"{package.package_id}_qg3_q2"
        q7.text = "Who invented pneumatic tires?"
        q7.answer = "John Boyd Dunlop"
        
        q8 = Question()
        q8.question_id = f"{package.package_id}_qg3_q3"
        q8.text = "In which decade was the safety bicycle introduced?"
        q8.answer = "1890s"
        
        qg3.questions = [q6, q7, q8]
        
        # Question Group 4: Matching Information (example)
        qg4 = QuestionGroup()
        qg4.type = QuestionType.TYPE4
        qg4.explanation = "Match each statement with the correct paragraph (A, B, or C)."
        
        # Create additional inputs for matching
        from models import AdditionalInput
        qg4.additional_inputs = AdditionalInput(
            input_type=QuestionType.TYPE4.value,
            data={
                'infoList': [
                    'A. Early Developments',
                    'B. The Penny-Farthing Era', 
                    'C. The Safety Bicycle'
                ]
            }
        )
        
        q9 = Question()
        q9.question_id = f"{package.package_id}_qg4_q1"
        q9.text = "Which paragraph mentions the invention of pneumatic tires?"
        q9.answer = "C"
        
        q10 = Question()
        q10.question_id = f"{package.package_id}_qg4_q2"
        q10.text = "Which paragraph describes a bicycle made entirely of wood?"
        q10.answer = "A"
        
        qg4.questions = [q9, q10]
        
        package.question_groups = [qg1, qg2, qg3, qg4]
        
        # Save package
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="sample_bicycle_history.json"
        )
        
        if filepath:
            try:
                package.save_to_file(filepath)
                messagebox.showinfo("Success", 
                                  f"Sample package created successfully!\n\n"
                                  f"Package: The History of the Bicycle\n"
                                  f"Questions: 8\n"
                                  f"File: {filepath}\n\n"
                                  f"You can now open this package in the Exam Engine to take the test.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create sample package:\n{str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MainLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
