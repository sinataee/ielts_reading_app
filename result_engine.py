"""
Result Engine Module
Evaluate user's submitted answers and produce IELTS band score
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import List, Dict
from models import (
    ReadingPackage, AnswerRecord, EvaluationResult, FeedbackItem,
    IELTSScoringRules
)


class ResultEngineWindow:
    """Result Engine Window for displaying exam results"""
    
    def __init__(self, root, package: ReadingPackage, answer_records: List[AnswerRecord]):
        self.root = root
        self.root.title("IELTS Reading Exam Results")
        self.root.geometry("1000x700")
        
        self.package = package
        self.answer_records = answer_records
        self.evaluation_result: EvaluationResult = None
        
        # Evaluate answers
        self.evaluate()
        
        # Create UI
        self.create_ui()
    
    def evaluate(self):
        """Evaluate user's answers"""
        self.evaluation_result = EvaluationResult()
        
        # Get scoring rules
        scoring_rules = IELTSScoringRules.get_academic_rules()
        
        # Create answer lookup
        answer_lookup: Dict[str, AnswerRecord] = {
            ar.question_id: ar for ar in self.answer_records
        }
        
        # Collect all questions from package
        all_questions = []
        for qg in self.package.question_groups:
            all_questions.extend(qg.questions)
        
        self.evaluation_result.total_questions = len(all_questions)
        
        # Evaluate each question
        for question in all_questions:
            feedback = FeedbackItem(
                question_id=question.question_id,
                is_correct=False,
                correct_answer=question.answer,
                user_answer=None
            )
            
            # Get user's answer
            if question.question_id in answer_lookup:
                user_record = answer_lookup[question.question_id]
                user_answer = user_record.user_answer
                feedback.user_answer = user_answer
                
                if user_answer:
                    # Normalize answers for comparison
                    normalized_user = self.normalize_answer(user_answer)
                    normalized_correct = self.normalize_answer(question.answer)
                    
                    if normalized_user == normalized_correct:
                        feedback.is_correct = True
                        self.evaluation_result.correct_count += 1
                    else:
                        self.evaluation_result.incorrect_count += 1
                else:
                    self.evaluation_result.unanswered_count += 1
            else:
                self.evaluation_result.unanswered_count += 1
            
            self.evaluation_result.per_question_feedback.append(feedback)
        
        # Calculate band score
        correct_count = self.evaluation_result.correct_count
        if correct_count in scoring_rules.mapping:
            self.evaluation_result.band_score = scoring_rules.mapping[correct_count]
        else:
            # Handle edge cases
            max_score = max(scoring_rules.mapping.keys())
            if correct_count > max_score:
                self.evaluation_result.band_score = 9.0
            else:
                self.evaluation_result.band_score = 0.0
    
    def normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison"""
        if not answer:
            return ""
        
        # Convert to lowercase and strip whitespace
        normalized = answer.lower().strip()
        
        # Remove common punctuation
        for char in ['.', ',', '!', '?', ';', ':']:
            normalized = normalized.replace(char, '')
        
        return normalized
    
    def create_ui(self):
        """Create results UI"""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="IELTS Reading Test Results", 
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(pady=20)
        
        # Summary frame
        summary_frame = tk.Frame(self.root, bg='#ecf0f1', pady=20)
        summary_frame.pack(fill=tk.X)
        
        # Create summary cards
        card_frame = tk.Frame(summary_frame, bg='#ecf0f1')
        card_frame.pack()
        
        self.create_summary_card(card_frame, "Band Score", 
                                f"{self.evaluation_result.band_score}", 
                                '#27ae60', 0, 0)
        
        self.create_summary_card(card_frame, "Correct Answers", 
                                f"{self.evaluation_result.correct_count}", 
                                '#3498db', 0, 1)
        
        self.create_summary_card(card_frame, "Incorrect Answers", 
                                f"{self.evaluation_result.incorrect_count}", 
                                '#e74c3c', 0, 2)
        
        self.create_summary_card(card_frame, "Unanswered", 
                                f"{self.evaluation_result.unanswered_count}", 
                                '#95a5a6', 0, 3)
        
        self.create_summary_card(card_frame, "Total Questions", 
                                f"{self.evaluation_result.total_questions}", 
                                '#34495e', 1, 0, colspan=4)
        
        # Band score interpretation
        interpretation = self.get_band_interpretation(self.evaluation_result.band_score)
        tk.Label(summary_frame, text=interpretation, font=('Arial', 11, 'italic'),
                bg='#ecf0f1', fg='#34495e', wraplength=800).pack(pady=10)
        
        # Notebook for detailed results
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Question by Question
        self.create_detailed_tab(notebook)
        
        # Tab 2: Incorrect Answers
        self.create_incorrect_tab(notebook)
        
        # Tab 3: Statistics
        self.create_statistics_tab(notebook)
        
        # Bottom buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="Export Results", command=self.export_results,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'), 
                 width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Close", command=self.root.destroy,
                 bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'),
                 width=15).pack(side=tk.RIGHT, padx=10)
    
    def create_summary_card(self, parent, title, value, color, row, col, colspan=1):
        """Create a summary card widget"""
        card = tk.Frame(parent, bg=color, width=180, height=100, relief=tk.RAISED, bd=2)
        card.grid(row=row, column=col, padx=10, pady=10, columnspan=colspan, sticky='ew')
        card.grid_propagate(False)
        
        if colspan > 1:
            card.config(width=760)
        
        tk.Label(card, text=title, font=('Arial', 12), bg=color, fg='white').pack(pady=5)
        tk.Label(card, text=value, font=('Arial', 28, 'bold'), bg=color, fg='white').pack()
    
    def get_band_interpretation(self, band_score: float) -> str:
        """Get interpretation of band score"""
        interpretations = {
            9.0: "Expert user - You have fully operational command of the language.",
            8.5: "Very good user - You have fully operational command with occasional inaccuracies.",
            8.0: "Very good user - You handle complex detailed argumentation well.",
            7.5: "Good user - You have operational command with occasional inaccuracies.",
            7.0: "Good user - You have operational command of the language.",
            6.5: "Competent user - Generally effective command despite some inaccuracies.",
            6.0: "Competent user - You have an effective command despite inaccuracies.",
            5.5: "Modest user - You have partial command and can handle overall meaning.",
            5.0: "Modest user - You have partial command of the language.",
            4.5: "Limited user - Basic competence is limited to familiar situations.",
            4.0: "Limited user - You have basic competence in very familiar situations.",
            3.5: "Extremely limited user - You convey meaning in very familiar situations.",
            3.0: "Extremely limited user - You can understand general meaning in familiar contexts.",
            2.5: "Intermittent user - You have great difficulty understanding.",
            2.0: "Intermittent user - You struggle with real communication.",
            1.0: "Non-user - You have no ability to use the language.",
            0.0: "Did not attempt the test."
        }
        
        return interpretations.get(band_score, "Keep practicing to improve your score!")
    
    def create_detailed_tab(self, notebook):
        """Create detailed question-by-question results tab"""
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Detailed Results")
        
        # Create scrolled text
        text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=('Courier', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        question_num = 1
        for qg_idx, qg in enumerate(self.package.question_groups):
            text.insert("end", f"\n{'='*80}\n", 'header')
            text.insert("end", f"Question Group {qg_idx + 1} - {qg.type.value}\n", 'header')
            text.insert("end", f"{'='*80}\n\n", 'header')
            
            for q in qg.questions:
                # Find feedback for this question
                feedback = next((f for f in self.evaluation_result.per_question_feedback 
                               if f.question_id == q.question_id), None)
                
                if feedback:
                    # Question text
                    text.insert("end", f"Q{question_num}: {q.text}\n", 'question')
                    
                    # User's answer
                    user_ans = feedback.user_answer if feedback.user_answer else "[NOT ANSWERED]"
                    text.insert("end", f"Your Answer: {user_ans}\n", 'user_answer')
                    
                    # Correct answer
                    text.insert("end", f"Correct Answer: {feedback.correct_answer}\n", 'correct_answer')
                    
                    # Result
                    if feedback.is_correct:
                        text.insert("end", "✓ CORRECT\n\n", 'correct')
                    else:
                        text.insert("end", "✗ INCORRECT\n\n", 'incorrect')
                
                question_num += 1
        
        # Configure tags
        text.tag_configure('header', font=('Courier', 10, 'bold'))
        text.tag_configure('question', font=('Courier', 10, 'bold'))
        text.tag_configure('correct', foreground='#27ae60', font=('Courier', 10, 'bold'))
        text.tag_configure('incorrect', foreground='#e74c3c', font=('Courier', 10, 'bold'))
        
        text.config(state=tk.DISABLED)
    
    def create_incorrect_tab(self, notebook):
        """Create tab showing only incorrect answers"""
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Incorrect Answers")
        
        # Create scrolled text
        text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=('Courier', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add content
        incorrect_feedbacks = [f for f in self.evaluation_result.per_question_feedback if not f.is_correct]
        
        if not incorrect_feedbacks:
            text.insert("end", "Congratulations! You answered all questions correctly!\n", 'success')
            text.tag_configure('success', font=('Courier', 12, 'bold'), foreground='#27ae60')
        else:
            text.insert("end", f"Questions you answered incorrectly or left unanswered: {len(incorrect_feedbacks)}\n\n", 'header')
            text.tag_configure('header', font=('Courier', 11, 'bold'))
            
            question_num = 1
            total_questions = 0
            for qg in self.package.question_groups:
                for q in qg.questions:
                    total_questions += 1
                    feedback = next((f for f in incorrect_feedbacks if f.question_id == q.question_id), None)
                    
                    if feedback:
                        text.insert("end", f"\nQuestion {total_questions}:\n", 'question')
                        text.insert("end", f"{q.text}\n", 'question_text')
                        
                        user_ans = feedback.user_answer if feedback.user_answer else "[NOT ANSWERED]"
                        text.insert("end", f"Your Answer: {user_ans}\n", 'user')
                        text.insert("end", f"Correct Answer: {feedback.correct_answer}\n", 'correct')
                        text.insert("end", f"{'-'*60}\n", 'separator')
            
            text.tag_configure('question', font=('Courier', 10, 'bold'))
            text.tag_configure('user', foreground='#e74c3c')
            text.tag_configure('correct', foreground='#27ae60')
        
        text.config(state=tk.DISABLED)
    
    def create_statistics_tab(self, notebook):
        """Create statistics tab"""
        tab = tk.Frame(notebook)
        notebook.add(tab, text="Statistics")
        
        stats_frame = tk.Frame(tab)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Overall statistics
        tk.Label(stats_frame, text="Overall Performance", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        stats_text = f"""
Total Questions: {self.evaluation_result.total_questions}
Correct Answers: {self.evaluation_result.correct_count}
Incorrect Answers: {self.evaluation_result.incorrect_count}
Unanswered: {self.evaluation_result.unanswered_count}

Accuracy: {(self.evaluation_result.correct_count / self.evaluation_result.total_questions * 100):.1f}%
Completion Rate: {((self.evaluation_result.correct_count + self.evaluation_result.incorrect_count) / self.evaluation_result.total_questions * 100):.1f}%

Band Score: {self.evaluation_result.band_score}
        """
        
        tk.Label(stats_frame, text=stats_text, font=('Courier', 12), 
                justify=tk.LEFT).pack(pady=10)
        
        # Performance by question type
        tk.Label(stats_frame, text="Performance by Question Type", 
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        type_stats = self.calculate_type_statistics()
        
        # Create table
        table_frame = tk.Frame(stats_frame)
        table_frame.pack(pady=10)
        
        headers = ['Question Type', 'Total', 'Correct', 'Accuracy']
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Arial', 11, 'bold'), 
                    width=20, relief=tk.RAISED).grid(row=0, column=col, padx=2, pady=2)
        
        row = 1
        for type_name, stats in type_stats.items():
            tk.Label(table_frame, text=type_name, width=20, 
                    relief=tk.RIDGE).grid(row=row, column=0, padx=2, pady=2)
            tk.Label(table_frame, text=str(stats['total']), width=20, 
                    relief=tk.RIDGE).grid(row=row, column=1, padx=2, pady=2)
            tk.Label(table_frame, text=str(stats['correct']), width=20, 
                    relief=tk.RIDGE).grid(row=row, column=2, padx=2, pady=2)
            
            accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            tk.Label(table_frame, text=f"{accuracy:.1f}%", width=20, 
                    relief=tk.RIDGE).grid(row=row, column=3, padx=2, pady=2)
            row += 1
    
    def calculate_type_statistics(self) -> Dict:
        """Calculate statistics by question type"""
        stats = {}
        
        for qg in self.package.question_groups:
            type_name = qg.type.value
            if type_name not in stats:
                stats[type_name] = {'total': 0, 'correct': 0}
            
            for q in qg.questions:
                stats[type_name]['total'] += 1
                
                feedback = next((f for f in self.evaluation_result.per_question_feedback 
                               if f.question_id == q.question_id), None)
                
                if feedback and feedback.is_correct:
                    stats[type_name]['correct'] += 1
        
        return stats
    
    def export_results(self):
        """Export results to JSON file"""
        from tkinter import filedialog
        import json
        from datetime import datetime
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.evaluation_result.to_dict(), f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Results exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results:\n{str(e)}")


def main():
    """For testing purposes"""
    root = tk.Tk()
    # This would normally be called from exam_engine
    messagebox.showinfo("Info", "This module should be called from the Exam Engine")
    root.destroy()


if __name__ == "__main__":
    main()
