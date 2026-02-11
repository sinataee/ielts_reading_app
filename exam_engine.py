"""
Exam Engine Module
Load a saved reading package and present it in an interactive exam environment
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import threading
import re
import os
from models import (
    ReadingPackage, AnswerRecord, HighlightRecord, QuestionType
)


class HighlightToolbar(tk.Frame):
    """Toolbar for text highlighting"""
    
    def __init__(self, parent, callback):
        super().__init__(parent, bg='lightgray', relief=tk.RAISED, bd=2)
        self.callback = callback
        
        colors = [
            ('Yellow', '#FFFF00'),
            ('Green', '#90EE90'),
            ('Blue', '#ADD8E6'),
            ('Pink', '#FFB6C1')
        ]
        
        for color_name, color_code in colors:
            btn = tk.Button(self, text=color_name, bg=color_code, 
                          command=lambda c=color_code: self.callback(c))
            btn.pack(side=tk.LEFT, padx=2)
        
        tk.Button(self, text="Remove", command=lambda: self.callback(None)).pack(side=tk.LEFT, padx=2)


class ExamEngineWindow:
    """Main Exam Engine Window"""
    
    def __init__(self, root, package_path: Optional[str] = None):
        self.root = root
        self.root.title("IELTS Reading Exam")
        
        # Make fullscreen
        self.root.state('zoomed')  # Windows/Linux
        try:
            self.root.attributes('-zoomed', True)  # Alternative for some systems
        except:
            pass
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Set minimum size
        self.root.minsize(1024, 768)
        
        self.package: Optional[ReadingPackage] = None
        self.answer_records: Dict[str, AnswerRecord] = {}
        self.highlight_records: List[HighlightRecord] = []
        
        # Timer variables
        self.exam_duration = 60 * 60  # 60 minutes in seconds
        self.time_remaining = self.exam_duration
        self.timer_running = False
        self.exam_started = False
        
        # Answer widgets
        self.answer_widgets: Dict[str, tk.Widget] = {}
        self._diagram_images: List[tk.PhotoImage] = []
        
        if package_path:
            self.load_package(package_path)
        else:
            self.prompt_load_package()
    
    def prompt_load_package(self):
        """Prompt user to load a package"""
        filepath = filedialog.askopenfilename(
            title="Select Reading Package",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            self.load_package(filepath)
        else:
            messagebox.showwarning("No Package", "No package selected. Please load a package.")
            self.root.after(100, self.prompt_load_package)
    
    def load_package(self, filepath: str):
        """Load reading package from file"""
        try:
            self.package = ReadingPackage.load_from_file(filepath)
            self.create_ui()
            messagebox.showinfo("Package Loaded", 
                              f"Package loaded successfully!\n\n"
                              f"Title: {self.package.reading_content.title}\n"
                              f"Question Groups: {len(self.package.question_groups)}\n"
                              f"Total Questions: {sum(len(qg.questions) for qg in self.package.question_groups)}\n\n"
                              f"Click 'Start Exam' to begin.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load package:\n{str(e)}")
            self.root.quit()
    
    def create_ui(self):
        """Create the exam UI"""
        # Top bar
        top_bar = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        # Timer display
        timer_frame = tk.Frame(top_bar, bg='#2c3e50')
        timer_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(timer_frame, text="Time Remaining:", bg='#2c3e50', 
                fg='white', font=('Arial', 12)).pack()
        self.timer_label = tk.Label(timer_frame, text="60:00", bg='#2c3e50',
                                    fg='#e74c3c', font=('Arial', 24, 'bold'))
        self.timer_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(top_bar, bg='#2c3e50')
        button_frame.pack(side=tk.RIGHT, padx=20)
        
        self.start_btn = tk.Button(button_frame, text="Start Exam", 
                                   command=self.start_exam, bg='#27ae60', fg='white',
                                   font=('Arial', 12, 'bold'), width=12)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(button_frame, text="Pause", 
                                   command=self.pause_exam, bg='#f39c12', fg='white',
                                   font=('Arial', 12, 'bold'), width=12, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.end_btn = tk.Button(button_frame, text="End Exam", 
                                command=self.end_exam, bg='#e74c3c', fg='white',
                                font=('Arial', 12, 'bold'), width=12, state=tk.DISABLED)
        self.end_btn.pack(side=tk.LEFT, padx=5)
        
        # Main split screen
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True)
        self.root.update_idletasks()
        
        # Left pane - Reading content
        left_frame = tk.Frame(paned)
        right_frame = tk.Frame(paned)
        half_width = max(500, self.root.winfo_width() // 2)
        paned.add(left_frame, minsize=450, width=half_width, stretch='always')
        
        tk.Label(left_frame, text="Reading Passage", font=('Arial', 14, 'bold'),
                bg='#34495e', fg='white').pack(fill=tk.X)
        
        self.reading_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, 
                                                      font=('Arial', 12), padx=20, pady=15,
                                                      spacing1=3, spacing2=2, spacing3=3)
        self.reading_text.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event for highlighting
        self.reading_text.bind("<<Selection>>", self.on_text_selection)
        self.reading_text.bind("<ButtonRelease-1>", self.on_text_selection)
        self.reading_text.bind('<Key>', lambda e: 'break')
        
        # Configure highlight tags
        self.reading_text.tag_configure('highlight_yellow', background='#FFFF00')
        self.reading_text.tag_configure('highlight_green', background='#90EE90')
        self.reading_text.tag_configure('highlight_blue', background='#ADD8E6')
        self.reading_text.tag_configure('highlight_pink', background='#FFB6C1')
        
        # Right pane - Questions
        paned.add(right_frame, minsize=450, width=half_width, stretch='always')

        def keep_balanced_panes():
            try:
                total = max(900, self.root.winfo_width())
                if abs(total - self._last_pane_width) < 8:
                    return
                self._last_pane_width = total
                paned.sash_place(0, total // 2, 1)
            except tk.TclError:
                pass

        def schedule_balance(event=None):
            if event is not None and event.widget is not self.root:
                return
            if self._pane_balance_job:
                self.root.after_cancel(self._pane_balance_job)
            self._pane_balance_job = self.root.after(80, keep_balanced_panes)

        self.root.after_idle(keep_balanced_panes)
        self.root.bind('<Configure>', schedule_balance, add='+')
        
        tk.Label(right_frame, text="Questions", font=('Arial', 14, 'bold'),
                bg='#34495e', fg='white').pack(fill=tk.X)
        
        # Canvas with scrollbar for questions
        canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        self.questions_frame = tk.Frame(canvas)
        
        self.questions_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        self.questions_window = canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def fit_questions_to_canvas(event):
            canvas.itemconfigure(self.questions_window, width=event.width)

        canvas.bind('<Configure>', fit_questions_to_canvas)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling in the question panel
        self.bind_mousewheel_scrolling(canvas)
        
        # Load content
        self.load_reading_content()
        self.load_questions()
        
        # Highlight toolbar (initially hidden)
        self.highlight_toolbar = None
        self._pane_balance_job = None
        self._last_pane_width = 0

    def bind_mousewheel_scrolling(self, widget):
        """Enable cross-platform mouse-wheel scrolling for canvas/text widgets."""
        def _on_mousewheel(event):
            if hasattr(event, "delta") and event.delta:
                widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif event.num == 4:
                widget.yview_scroll(-1, "units")
            elif event.num == 5:
                widget.yview_scroll(1, "units")

        widget.bind_all("<MouseWheel>", _on_mousewheel, add="+")
        widget.bind_all("<Button-4>", _on_mousewheel, add="+")
        widget.bind_all("<Button-5>", _on_mousewheel, add="+")
    
    def _make_selectable_text(self, parent, text: str, font=('Arial', 10), wraplength=600,
                              justify=tk.LEFT, padding=(0, 0), bold=False):
        # Render selectable, read-only text with highlight support.
        bg_color = parent.cget('bg')
        char_width = max(30, int(wraplength / 7))
        lines_estimate = max(1, min(8, (len(text) // char_width) + text.count('\n') + 1))
        widget = tk.Text(parent, wrap=tk.WORD, height=lines_estimate, relief=tk.FLAT,
                         bg=bg_color, font=font, padx=0, pady=0, borderwidth=0,
                         highlightthickness=0, cursor='arrow')
        widget.tag_configure('highlight_yellow', background='#FFFF00')
        widget.tag_configure('highlight_green', background='#90EE90')
        widget.tag_configure('highlight_blue', background='#ADD8E6')
        widget.tag_configure('highlight_pink', background='#FFB6C1')
        if bold:
            widget.tag_configure('content', font=(font[0], font[1], 'bold'))
            widget.insert('1.0', text, 'content')
        else:
            widget.insert('1.0', text)
        # Keep widget selectable but read-only
        widget.bind('<Key>', lambda e: 'break')
        widget.bind('<<Selection>>', lambda e, w=widget: self.show_highlight_menu(e, w))
        widget.bind('<ButtonRelease-1>', lambda e, w=widget: self.show_highlight_menu(e, w))
        widget.pack(anchor=tk.W, fill=tk.X, pady=padding[1])
        return widget

    def load_reading_content(self):
        """Load reading content into left pane"""
        self.reading_text.config(state=tk.NORMAL)
        self.reading_text.delete("1.0", "end")
        
        rc = self.package.reading_content
        
        # Explanation
        if rc.explanation:
            self.reading_text.insert("end", rc.explanation + "\n\n", 'explanation')
            self.reading_text.tag_configure('explanation', font=('Arial', 11, 'italic'), 
                                           foreground='#555555')
        
        # Title
        if rc.title:
            self.reading_text.insert("end", rc.title + "\n\n", 'title')
            self.reading_text.tag_configure('title', font=('Arial', 18, 'bold'), 
                                           justify='center', spacing3=10)
        
        # Paragraphs
        for i, para in enumerate(rc.paragraphs):
            if para.title:
                self.reading_text.insert("end", f"{para.title}\n", f'para_title_{i}')
                self.reading_text.tag_configure(f'para_title_{i}', font=('Arial', 14, 'bold'),
                                               spacing1=10, spacing3=5)
            
            if para.body:
                self.reading_text.insert("end", f"{para.body}\n\n", f'para_body_{i}')
                self.reading_text.tag_configure(f'para_body_{i}', font=('Arial', 12),
                                               spacing1=2, spacing2=2, spacing3=5)
        
    
    def load_questions(self):
        """Load questions into right pane"""
        question_number = 1
        
        for group_idx, qg in enumerate(self.package.question_groups):
            # Group frame
            group_frame = tk.LabelFrame(self.questions_frame, 
                                       text=f"Questions {question_number}-{question_number + len(qg.questions) - 1}",
                                       font=('Arial', 12, 'bold'), padx=10, pady=10)
            group_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Explanation
            if qg.explanation:
                self._make_selectable_text(
                    group_frame,
                    qg.explanation,
                    font=('Arial', 10, 'italic'),
                    wraplength=620,
                    justify=tk.LEFT,
                    padding=(0, 5)
                )
            
            # Type indicator
            tk.Label(group_frame, text=f"Type: {qg.type.value}", 
                    font=('Arial', 10), fg='blue').pack(anchor=tk.W, pady=5)
            
            # Additional inputs (if any) - display and collect options for dropdowns
            matching_options = []
            if qg.additional_inputs:
                matching_options = self.render_additional_inputs(group_frame, qg.additional_inputs)
            
            # Questions
            for q in qg.questions:
                q_frame = tk.Frame(group_frame)
                q_frame.pack(fill=tk.X, pady=5)
                
                # Extract question text (without choices for Type 1)
                question_display = q.text
                if qg.type == QuestionType.TYPE1 and '\n' in q.text:
                    question_display = q.text.split('\n')[0]
                
                self._make_selectable_text(
                    q_frame,
                    f"{question_number}. {question_display}",
                    font=('Arial', 10),
                    wraplength=620,
                    justify=tk.LEFT
                )
                
                # Answer input based on question type
                answer_widget = self.create_answer_input(q_frame, qg.type, q.question_id, q.text)
                
                # For matching types, populate dropdown with options
                if qg.type in [QuestionType.TYPE4, QuestionType.TYPE5, 
                              QuestionType.TYPE6, QuestionType.TYPE7] and matching_options:
                    if isinstance(answer_widget, tk.StringVar):
                        # Find the combobox widget
                        for widget in q_frame.winfo_children():
                            if isinstance(widget, ttk.Combobox):
                                widget['values'] = matching_options
                                break
                
                self.answer_widgets[q.question_id] = answer_widget
                
                # Initialize answer record
                self.answer_records[q.question_id] = AnswerRecord(question_id=q.question_id)
                
                question_number += 1
    
    def create_answer_input(self, parent, question_type: QuestionType, question_id: str, question_text: str = "") -> tk.Widget:
        """Create appropriate answer input widget based on question type"""
        if question_type == QuestionType.TYPE1:  # Multiple choice
            var = tk.StringVar()
            frame = tk.Frame(parent)
            frame.pack(anchor=tk.W, padx=20, pady=5)
            
            # Extract choices from question text if embedded
            choices = ['A', 'B', 'C', 'D']  # Default
            if '\n' in question_text:
                lines = question_text.split('\n')
                choice_lines = [line for line in lines[1:] if line.strip() and (line.strip()[0] in ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd'])]
                if choice_lines:
                    for line in choice_lines:
                        parts = line.split('.', 1)
                        if len(parts) >= 2:
                            option = parts[0].strip().upper()
                            text = parts[1].strip()
                            tk.Radiobutton(frame, text=f"{option}. {text}", variable=var, value=option,
                                         command=lambda: self.record_answer(question_id, var.get()),
                                         wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, pady=2)
                else:
                    # Fallback to default options
                    for option in choices:
                        tk.Radiobutton(frame, text=option, variable=var, value=option,
                                     command=lambda: self.record_answer(question_id, var.get())).pack(anchor=tk.W)
            else:
                for option in choices:
                    tk.Radiobutton(frame, text=option, variable=var, value=option,
                                 command=lambda: self.record_answer(question_id, var.get())).pack(anchor=tk.W)
            return var
        
        elif question_type in [QuestionType.TYPE2, QuestionType.TYPE3]:  # True/False/Not Given or Yes/No/Not Given
            var = tk.StringVar()
            frame = tk.Frame(parent)
            frame.pack(anchor=tk.W, padx=20, pady=5)
            
            options = ['TRUE', 'FALSE', 'NOT GIVEN'] if question_type == QuestionType.TYPE2 else ['YES', 'NO', 'NOT GIVEN']
            for option in options:
                tk.Radiobutton(frame, text=option, variable=var, value=option,
                             command=lambda: self.record_answer(question_id, var.get())).pack(anchor=tk.W)
            return var
        
        elif question_type in [QuestionType.TYPE4, QuestionType.TYPE5, 
                              QuestionType.TYPE6, QuestionType.TYPE7]:  # Matching types
            var = tk.StringVar()
            combo = ttk.Combobox(parent, textvariable=var, width=30, state='readonly')
            combo.pack(anchor=tk.W, padx=20, pady=5)
            combo.bind('<<ComboboxSelected>>', lambda e: self.record_answer(question_id, var.get()))
            return var
        
        else:  # Text input for other types (8, 9, 10, 11)
            var = tk.StringVar()
            entry = tk.Entry(parent, textvariable=var, width=40)
            entry.pack(anchor=tk.W, padx=20, pady=5)
            entry.bind('<KeyRelease>', lambda e: self.record_answer(question_id, var.get()))
            return var
    
    def render_additional_inputs(self, parent, additional_inputs):
        """Render additional inputs like lists, tables, etc. and return options for dropdowns"""
        frame = tk.LabelFrame(parent, text="📋 ADDITIONAL INFORMATION - READ CAREFULLY", 
                             padx=15, pady=15, font=('Arial', 11, 'bold'),
                             bg='#fff9e6', relief=tk.SOLID, bd=2)
        frame.pack(fill=tk.X, pady=10)
        
        data = additional_inputs.data
        options = []
        
        # Render based on data type
        if 'infoList' in data:
            tk.Label(frame, text="Match the information to the correct option:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6').pack(anchor=tk.W, pady=5)
            
            list_frame = tk.Frame(frame, bg='white', relief=tk.RIDGE, bd=2)
            list_frame.pack(fill=tk.X, padx=5, pady=5)
            
            for item in data['infoList']:
                tk.Label(list_frame, text=f"  {item}", justify=tk.LEFT, 
                        wraplength=600, font=('Arial', 10), bg='white',
                        pady=3).pack(anchor=tk.W, padx=10, pady=2)
                options.append(item.split('.')[0].strip() if '.' in item else item[:10])
        
        elif 'headingList' in data:
            tk.Label(frame, text="Choose the correct heading:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6').pack(anchor=tk.W, pady=5)
            
            list_frame = tk.Frame(frame, bg='white', relief=tk.RIDGE, bd=2)
            list_frame.pack(fill=tk.X, padx=5, pady=5)
            
            for i, heading in enumerate(data['headingList']):
                tk.Label(list_frame, text=f"  {heading}", justify=tk.LEFT, 
                        wraplength=600, font=('Arial', 10), bg='white',
                        pady=3).pack(anchor=tk.W, padx=10, pady=2)
                options.append(heading.split('.')[0].strip() if '.' in heading else heading[:20])
        
        elif 'featureList' in data:
            tk.Label(frame, text="Match features to the options:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6').pack(anchor=tk.W, pady=5)
            
            list_frame = tk.Frame(frame, bg='white', relief=tk.RIDGE, bd=2)
            list_frame.pack(fill=tk.X, padx=5, pady=5)
            
            for item in data['featureList']:
                tk.Label(list_frame, text=f"  {item}", justify=tk.LEFT, 
                        wraplength=600, font=('Arial', 10), bg='white',
                        pady=3).pack(anchor=tk.W, padx=10, pady=2)
                options.append(item.split('.')[0].strip() if '.' in item else item[:15])
        
        elif 'sentenceEndingList' in data:
            tk.Label(frame, text="Complete the sentences with the correct ending:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6').pack(anchor=tk.W, pady=5)
            
            list_frame = tk.Frame(frame, bg='white', relief=tk.RIDGE, bd=2)
            list_frame.pack(fill=tk.X, padx=5, pady=5)
            
            for i, ending in enumerate(data['sentenceEndingList']):
                tk.Label(list_frame, text=f"  {ending}", justify=tk.LEFT, 
                        wraplength=600, font=('Arial', 10), bg='white',
                        pady=3).pack(anchor=tk.W, padx=10, pady=2)
                options.append(ending.split('.')[0].strip() if '.' in ending else chr(65+i))
        
        elif 'summaryData' in data:
            tk.Label(frame, text="📝 SUMMARY - Complete the gaps below:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6', fg='#d35400').pack(anchor=tk.W, pady=5)
            
            summary_frame = tk.Frame(frame, bg='white', relief=tk.SOLID, bd=2)
            summary_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            text_widget = scrolledtext.ScrolledText(summary_frame, height=8, width=70, 
                                                   wrap=tk.WORD, font=('Arial', 11),
                                                   bg='#fffef0', relief=tk.FLAT, padx=10, pady=10)
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert("1.0", data['summaryData'])
            
            # Configure highlight tags
            text_widget.tag_configure('highlight_yellow', background='#FFFF00')
            text_widget.tag_configure('highlight_green', background='#90EE90')
            text_widget.tag_configure('highlight_blue', background='#ADD8E6')
            text_widget.tag_configure('highlight_pink', background='#FFB6C1')
            text_widget.tag_configure('blank', background='#ffeb3b', font=('Arial', 11, 'bold'))
            
            # Highlight blanks
            content = data['summaryData']
            for match in re.finditer(r'\[\d+\]|\[BLANK\]', content):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                text_widget.tag_add('blank', start_idx, end_idx)
            
            # Enable text selection and bind highlighting
            text_widget.bind("<<Selection>>", lambda e: self.show_highlight_menu(e, text_widget))
            text_widget.bind("<ButtonRelease-1>", lambda e: self.show_highlight_menu(e, text_widget))
            text_widget.bind('<Key>', lambda e: 'break')
            self.bind_mousewheel_scrolling(text_widget)
        
        elif 'tableData' in data:
            tk.Label(frame, text="📊 TABLE - Complete the gaps below:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6', fg='#d35400').pack(anchor=tk.W, pady=5)
            
            # Create a canvas for the table with selection capability
            table_container = tk.Frame(frame, bg='white', relief=tk.SOLID, bd=2)
            table_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            table_canvas = tk.Canvas(table_container, bg='white', height=460)
            table_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=table_canvas.yview)
            table_scrollbar_x = ttk.Scrollbar(table_container, orient="horizontal", command=table_canvas.xview)
            table_inner = tk.Frame(table_canvas, bg='white')
            
            table_inner.bind("<Configure>", lambda e: table_canvas.configure(scrollregion=table_canvas.bbox("all")))
            table_canvas.create_window((0, 0), window=table_inner, anchor="nw")
            table_canvas.configure(yscrollcommand=table_scrollbar.set, xscrollcommand=table_scrollbar_x.set)
            
            # Display table with Text widgets for highlighting support
            table_data = data['tableData']
            rows = table_data['rows']
            cols = table_data['cols']
            content = table_data['content']
            
            for r in range(rows):
                for c in range(cols):
                    cell_text = content[r][c] if r < len(content) and c < len(content[r]) else ""
                    
                    # Only mark full-cell blanks (not normal text that happens to include [1], [2], etc.)
                    normalized_text = cell_text.strip()
                    is_blank = normalized_text in {'[BLANK]'} or bool(re.fullmatch(r'\[\d+\]', normalized_text))
                    is_header = (r == 0)
                    
                    # Use Text widget instead of Label to support highlighting
                    cell_widget = tk.Text(table_inner, width=24, height=4, 
                                         relief=tk.SOLID, bd=1, wrap=tk.WORD,
                                         font=('Arial', 11, 'bold' if is_header else 'normal'),
                                         padx=5, pady=5)
                    
                    # Set background color
                    if is_blank:
                        cell_widget.configure(bg='#ffeb3b')
                    elif is_header:
                        cell_widget.configure(bg='#e8e8e8')
                    else:
                        cell_widget.configure(bg='white')
                    
                    cell_widget.insert("1.0", cell_text)

                    # Highlight inline blank tokens without coloring whole cell
                    for match in re.finditer(r'\[BLANK\]|\[\d+\]', cell_text):
                        start_idx = f"1.0+{match.start()}c"
                        end_idx = f"1.0+{match.end()}c"
                        cell_widget.tag_add('blank_inline', start_idx, end_idx)
                    
                    # Configure highlight tags
                    cell_widget.tag_configure('highlight_yellow', background='#FFFF00')
                    cell_widget.tag_configure('highlight_green', background='#90EE90')
                    cell_widget.tag_configure('highlight_blue', background='#ADD8E6')
                    cell_widget.tag_configure('highlight_pink', background='#FFB6C1')
                    cell_widget.tag_configure('blank_inline', background='#ffeb3b')
                    
                    # Enable highlighting and keep read-only
                    cell_widget.bind('<Key>', lambda e: 'break')
                    cell_widget.bind("<<Selection>>", lambda e, w=cell_widget: self.show_highlight_menu(e, w))
                    cell_widget.bind("<ButtonRelease-1>", lambda e, w=cell_widget: self.show_highlight_menu(e, w))
                    
                    cell_widget.grid(row=r, column=c, sticky='nsew', padx=1, pady=1)
            
            # Configure column weights
            for c in range(cols):
                table_inner.columnconfigure(c, weight=1)
            
            table_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            table_scrollbar.pack(side="right", fill="y")
            table_scrollbar_x.pack(side="bottom", fill="x")
            self.bind_mousewheel_scrolling(table_canvas)
        
        elif 'flowchartData' in data:
            tk.Label(frame, text="🔄 FLOW-CHART - Complete the gaps below:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6', fg='#d35400').pack(anchor=tk.W, pady=5)
            
            # Create canvas for graphical flowchart
            flowchart_container = tk.Frame(frame, bg='white', relief=tk.SOLID, bd=2)
            flowchart_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Use canvas to draw flowchart graphically
            canvas = tk.Canvas(flowchart_container, bg='white', height=520, width=900)
            scrollbar_y = ttk.Scrollbar(flowchart_container, orient="vertical", command=canvas.yview)
            scrollbar_x = ttk.Scrollbar(flowchart_container, orient="horizontal", command=canvas.xview)
            
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            # Parse flowchart data and render graphically
            flowchart_text = data['flowchartData']
            self.render_flowchart_graphically(canvas, flowchart_text)
            
            canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            self.bind_mousewheel_scrolling(canvas)
            
            # Enable canvas selection for highlighting
            canvas.bind("<Button-1>", lambda e: self.canvas_click_handler(e, canvas))
        
        elif 'diagramImage' in data:
            tk.Label(frame, text="📐 DIAGRAM:", 
                    font=('Arial', 10, 'bold'), bg='#fff9e6', fg='#d35400').pack(anchor=tk.W, pady=5)
            
            diagram_frame = tk.Frame(frame, bg='white', relief=tk.SOLID, bd=2)
            diagram_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            diagram_data = str(data['diagramImage']).strip()

            # If this is an image path, render the image. Otherwise render rich text.
            lower_value = diagram_data.lower()
            is_image_path = (
                os.path.exists(diagram_data)
                and lower_value.endswith((".png", ".gif", ".ppm", ".pgm"))
            )

            if is_image_path:
                image_widget = tk.Label(diagram_frame, bg='white')
                image_widget.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
                try:
                    image = tk.PhotoImage(file=diagram_data)
                    self._diagram_images.append(image)
                    image_widget.config(image=image)
                except tk.TclError:
                    image_widget.config(text=f"Unable to load image: {diagram_data}", font=('Arial', 10), anchor='w')

                tk.Label(
                    diagram_frame,
                    text=f"Image source: {diagram_data}",
                    bg='white',
                    fg='#555555',
                    font=('Arial', 9, 'italic')
                ).pack(anchor=tk.W, padx=10, pady=(0, 8))
            else:
                diagram_text = tk.Text(diagram_frame, height=8, width=70, wrap=tk.WORD,
                                       font=('Arial', 10), bg='white', padx=10, pady=10)
                diagram_text.insert("1.0", diagram_data)
                diagram_text.bind('<Key>', lambda e: 'break')

                # Configure highlight tags
                diagram_text.tag_configure('highlight_yellow', background='#FFFF00')
                diagram_text.tag_configure('highlight_green', background='#90EE90')
                diagram_text.tag_configure('highlight_blue', background='#ADD8E6')
                diagram_text.tag_configure('highlight_pink', background='#FFB6C1')

                # Enable highlighting
                diagram_text.bind("<<Selection>>", lambda e: self.show_highlight_menu(e, diagram_text))
                diagram_text.bind("<ButtonRelease-1>", lambda e: self.show_highlight_menu(e, diagram_text))
                diagram_text.pack(fill=tk.BOTH, expand=True)
                self.bind_mousewheel_scrolling(diagram_text)
        
        return options
    
    def record_answer(self, question_id: str, answer: str):
        """Record user's answer"""
        if question_id in self.answer_records:
            self.answer_records[question_id].user_answer = answer
            self.answer_records[question_id].timestamp = datetime.now()
    
    def on_text_selection(self, event):
        """Handle text selection for highlighting"""
        try:
            selection = self.reading_text.get("sel.first", "sel.last")
            if selection and len(selection.strip()) > 0:
                # Show highlight toolbar
                if self.highlight_toolbar:
                    self.highlight_toolbar.destroy()
                
                # Get selection coordinates
                x = getattr(event, 'x_root', self.root.winfo_pointerx())
                y = getattr(event, 'y_root', self.root.winfo_pointery())
                
                self.highlight_toolbar = tk.Toplevel(self.root)
                self.highlight_toolbar.wm_overrideredirect(True)
                self.highlight_toolbar.geometry(f"+{x}+{y-30}")
                
                HighlightToolbar(self.highlight_toolbar, self.apply_highlight)
        except tk.TclError:
            pass
    
    def apply_highlight(self, color: Optional[str]):
        """Apply or remove highlight"""
        try:
            start = self.reading_text.index("sel.first")
            end = self.reading_text.index("sel.last")
            
            # Remove existing highlights in range
            for tag in ['highlight_yellow', 'highlight_green', 'highlight_blue', 'highlight_pink']:
                self.reading_text.tag_remove(tag, start, end)
            
            # Apply new highlight
            if color:
                tag_name = f'highlight_{self._color_to_name(color)}'
                self.reading_text.tag_add(tag_name, start, end)
                
                # Record highlight
                record = HighlightRecord(
                    selection_range=f"{start}:{end}",
                    highlight_color=color
                )
                self.highlight_records.append(record)
            
            if self.highlight_toolbar:
                self.highlight_toolbar.destroy()
                self.highlight_toolbar = None
        
        except tk.TclError:
            pass
    
    def _color_to_name(self, color: str) -> str:
        """Convert color code to name"""
        color_map = {
            '#FFFF00': 'yellow',
            '#90EE90': 'green',
            '#ADD8E6': 'blue',
            '#FFB6C1': 'pink'
        }
        return color_map.get(color, 'yellow')
    
    def start_exam(self):
        """Start the exam and timer"""
        if not self.exam_started:
            self.exam_started = True
            self.timer_running = True
            
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.end_btn.config(state=tk.NORMAL)
            
            # Start timer thread
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
            
            messagebox.showinfo("Exam Started", "The exam has started. Good luck!")
    
    def run_timer(self):
        """Timer countdown"""
        while self.timer_running and self.time_remaining > 0:
            mins, secs = divmod(self.time_remaining, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            
            # Change color when time is low
            if self.time_remaining <= 300:  # 5 minutes
                self.timer_label.config(fg='#e74c3c')
            elif self.time_remaining <= 600:  # 10 minutes
                self.timer_label.config(fg='#f39c12')
            
            threading.Event().wait(1)
            if self.timer_running:
                self.time_remaining -= 1
        
        if self.time_remaining <= 0:
            self.root.after(0, self.time_up)
    
    def pause_exam(self):
        """Pause/Resume the exam"""
        if self.timer_running:
            self.timer_running = False
            self.pause_btn.config(text="Resume")
            messagebox.showinfo("Paused", "Exam paused")
        else:
            self.timer_running = True
            self.pause_btn.config(text="Pause")
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def show_highlight_menu(self, event, text_widget):
        """Show highlighting menu for text widgets in tables/flowcharts"""
        try:
            selection_ranges = text_widget.tag_ranges("sel")
            if not selection_ranges:
                return

            if self.highlight_toolbar:
                self.highlight_toolbar.destroy()

            x = getattr(event, 'x_root', self.root.winfo_pointerx())
            y = getattr(event, 'y_root', self.root.winfo_pointery())

            self.highlight_toolbar = tk.Toplevel(self.root)
            self.highlight_toolbar.wm_overrideredirect(True)
            self.highlight_toolbar.geometry(f"+{x}+{y-30}")

            HighlightToolbar(self.highlight_toolbar, lambda color: self.apply_text_highlight(text_widget, color))
        except tk.TclError:
            pass

    def apply_text_highlight(self, text_widget, color: Optional[str]):
        """Apply highlight to selected text in a Text widget"""
        try:
            start = text_widget.index("sel.first")
            end = text_widget.index("sel.last")
            
            # Remove existing highlights in range
            for tag in ['highlight_yellow', 'highlight_green', 'highlight_blue', 'highlight_pink']:
                text_widget.tag_remove(tag, start, end)
            
            # Apply new highlight
            if color:
                tag_name = f'highlight_{self._color_to_name(color)}'
                text_widget.tag_add(tag_name, start, end)
            
            if self.highlight_toolbar:
                self.highlight_toolbar.destroy()
                self.highlight_toolbar = None
        except tk.TclError:
            pass
    
    def render_flowchart_graphically(self, canvas, flowchart_text):
        """Render flowchart as graphical elements on canvas."""
        lines = [line.strip() for line in flowchart_text.split('\n')]

        y_position = 30
        x_center = 450
        default_box_width = 260
        box_height = 66
        arrow_gap = 22

        def is_blank_text(value: str) -> bool:
            return '[BLANK]' in value or bool(re.search(r'\[\d+\]', value))

        def draw_box(x: int, y: int, label: str, width: int = default_box_width):
            blank = is_blank_text(label)
            fill_color = '#ffeb3b' if blank else '#e8f4f8'
            canvas.create_rectangle(
                x - width // 2,
                y,
                x + width // 2,
                y + box_height,
                fill=fill_color,
                outline='#2c3e50',
                width=2
            )
            canvas.create_text(
                x,
                y + box_height // 2,
                text=label,
                font=('Arial', 11, 'bold' if blank else 'normal'),
                width=width - 24
            )

        def draw_vertical_arrow(x: int, y_start: int, y_end: int):
            if y_end <= y_start:
                return
            canvas.create_line(x, y_start, x, y_end, arrow=tk.LAST, width=2, fill='#34495e')

        def parse_horizontal_parts(line: str):
            return [part.strip() for part in re.split(r'\s*(?:→|->)\s*', line) if part.strip()]

        for line in lines:
            if not line:
                y_position += 18
                continue

            if line in {'↓', 'v', 'V'}:
                draw_vertical_arrow(x_center, y_position, y_position + 28)
                y_position += 36
                continue

            if re.search(r'(→|->)', line):
                parts = parse_horizontal_parts(line)
                if not parts:
                    continue

                spacing = 290
                total_width = spacing * (len(parts) - 1)
                start_x = max(180, x_center - total_width // 2)

                previous_x = None
                for idx, part in enumerate(parts):
                    x_pos = start_x + idx * spacing
                    draw_box(x_pos, y_position, part)

                    if previous_x is not None:
                        canvas.create_line(
                            previous_x + default_box_width // 2,
                            y_position + box_height // 2,
                            x_pos - default_box_width // 2,
                            y_position + box_height // 2,
                            arrow=tk.LAST,
                            width=2,
                            fill='#34495e'
                        )
                    previous_x = x_pos

                y_position += box_height + arrow_gap
                continue

            if line.startswith('Step') or line.startswith('step'):
                draw_box(x_center, y_position, line)
                draw_vertical_arrow(x_center, y_position + box_height, y_position + box_height + 26)
                y_position += box_height + 34
                continue

            if any(ch in line for ch in ['┌', '└', '│', '─', '╱', '╲', '◆', '◇']):
                canvas.create_text(x_center, y_position, text=line, font=('Courier', 11), anchor='n')
                y_position += 20
                continue

            draw_box(x_center, y_position, line)
            y_position += box_height + 18

        canvas.configure(scrollregion=canvas.bbox("all"))

    def canvas_click_handler(self, event, canvas):
        """Handle clicks on canvas for potential future highlighting"""
        # Placeholder for canvas text highlighting if needed
        pass
    
    def time_up(self):
        """Handle time up"""
        self.timer_running = False
        messagebox.showwarning("Time's Up!", "The exam time has ended. Submitting your answers...")
        self.submit_exam()
    
    def end_exam(self):
        """End exam early"""
        if messagebox.askyesno("End Exam", "Are you sure you want to end the exam and submit your answers?"):
            self.timer_running = False
            self.submit_exam()
    
    def submit_exam(self):
        """Submit exam and show results"""
        self.timer_running = False
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.DISABLED)
        self.end_btn.config(state=tk.DISABLED)
        
        # Lock UI
        for widget in self.answer_widgets.values():
            if isinstance(widget, tk.Entry):
                widget.config(state=tk.DISABLED)
            elif isinstance(widget, ttk.Combobox):
                widget.config(state=tk.DISABLED)
        
        # Open result window
        from result_engine import ResultEngineWindow
        result_window = tk.Toplevel(self.root)
        ResultEngineWindow(result_window, self.package, list(self.answer_records.values()))


def main():
    root = tk.Tk()
    app = ExamEngineWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
