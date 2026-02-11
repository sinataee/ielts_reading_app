"""
Content Editor Module
Provides tools for creating, editing, and storing complete IELTS reading packages
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font as tkfont
from typing import Optional
import uuid
from models import (
    ReadingPackage, ReadingContent, Paragraph, QuestionGroup,
    Question, QuestionType, AdditionalInput
)


class RichTextEditor(tk.Frame):
    """Rich text editor with formatting toolbar"""
    
    def __init__(self, parent, height=10):
        super().__init__(parent)
        
        # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Bold button
        self.bold_btn = tk.Button(toolbar, text="B", font=('Arial', 10, 'bold'),
                                   width=3, command=self.toggle_bold)
        self.bold_btn.pack(side=tk.LEFT, padx=2)
        
        # Italic button
        self.italic_btn = tk.Button(toolbar, text="I", font=('Arial', 10, 'italic'),
                                     width=3, command=self.toggle_italic)
        self.italic_btn.pack(side=tk.LEFT, padx=2)
        
        # Font size
        tk.Label(toolbar, text="Size:").pack(side=tk.LEFT, padx=2)
        self.size_var = tk.StringVar(value="12")
        size_combo = ttk.Combobox(toolbar, textvariable=self.size_var, 
                                   values=['10', '12', '14', '16', '18', '20'], width=5)
        size_combo.pack(side=tk.LEFT, padx=2)
        size_combo.bind('<<ComboboxSelected>>', self.change_size)
        
        # Header styles
        tk.Button(toolbar, text="H1", command=lambda: self.apply_header(1)).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="H2", command=lambda: self.apply_header(2)).pack(side=tk.LEFT, padx=2)
        
        # Alignment
        tk.Button(toolbar, text="Left", command=lambda: self.set_align('left')).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Center", command=lambda: self.set_align('center')).pack(side=tk.LEFT, padx=2)
        
        # Text widget
        self.text = scrolledtext.ScrolledText(self, height=height, wrap=tk.WORD, font=('Arial', 12))
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags
        self.text.tag_configure('bold', font=('Arial', 12, 'bold'))
        self.text.tag_configure('italic', font=('Arial', 12, 'italic'))
        self.text.tag_configure('h1', font=('Arial', 18, 'bold'))
        self.text.tag_configure('h2', font=('Arial', 16, 'bold'))
        self.text.tag_configure('center', justify='center')
        self.text.tag_configure('left', justify='left')
    
    def toggle_bold(self):
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def toggle_italic(self):
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def change_size(self, event=None):
        size = int(self.size_var.get())
        self.text.configure(font=('Arial', size))
    
    def apply_header(self, level):
        try:
            tag = f'h{level}'
            self.text.tag_add(tag, "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def set_align(self, alignment):
        try:
            self.text.tag_add(alignment, "sel.first", "sel.last")
        except tk.TclError:
            # Apply to entire text if no selection
            self.text.tag_add(alignment, "1.0", "end")
    
    def get_text(self) -> str:
        return self.text.get("1.0", "end-1c")
    
    def set_text(self, text: str):
        self.text.delete("1.0", "end")
        self.text.insert("1.0", text)
    
    def clear(self):
        self.text.delete("1.0", "end")


class ContentEditorWindow:
    """Main Content Editor Window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("IELTS Content Editor")
        self.root.geometry("1200x800")
        
        self.current_package = ReadingPackage()
        self.current_package.package_id = str(uuid.uuid4())
        
        self.create_ui()
    
    def create_ui(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Package", command=self.new_package)
        file_menu.add_command(label="Open Package", command=self.open_package)
        file_menu.add_command(label="Save Package", command=self.save_package)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Reading Content
        self.create_reading_content_tab()
        
        # Tab 2: Question Groups
        self.create_question_groups_tab()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_reading_content_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Reading Content")
        
        # Canvas with scrollbar
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Explanation
        tk.Label(scrollable_frame, text="Explanation:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        self.explanation_editor = RichTextEditor(scrollable_frame, height=5)
        self.explanation_editor.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        tk.Label(scrollable_frame, text="Title:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        self.title_editor = RichTextEditor(scrollable_frame, height=3)
        self.title_editor.pack(fill=tk.X, padx=10, pady=5)
        
        # Paragraphs
        tk.Label(scrollable_frame, text="Paragraphs:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        
        self.paragraph_frame = tk.Frame(scrollable_frame)
        self.paragraph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.paragraph_editors = []
        
        # Add paragraph button
        tk.Button(scrollable_frame, text="Add Paragraph", command=self.add_paragraph).pack(pady=10)
        
        # Save reading content button
        tk.Button(scrollable_frame, text="Save Reading Content", 
                 command=self.save_reading_content, bg='green', fg='white').pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_paragraph(self):
        """Add a new paragraph editor"""
        para_container = tk.LabelFrame(self.paragraph_frame, text=f"Paragraph {len(self.paragraph_editors) + 1}")
        para_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(para_container, text="Paragraph Title:").pack(anchor=tk.W, padx=5)
        title_editor = RichTextEditor(para_container, height=2)
        title_editor.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(para_container, text="Paragraph Body:").pack(anchor=tk.W, padx=5)
        body_editor = RichTextEditor(para_container, height=8)
        body_editor.pack(fill=tk.X, padx=5, pady=2)
        
        # Remove button
        tk.Button(para_container, text="Remove Paragraph", 
                 command=lambda: self.remove_paragraph(para_container)).pack(pady=5)
        
        self.paragraph_editors.append({
            'container': para_container,
            'title': title_editor,
            'body': body_editor
        })
    
    def remove_paragraph(self, container):
        """Remove a paragraph editor"""
        self.paragraph_editors = [p for p in self.paragraph_editors if p['container'] != container]
        container.destroy()
    
    def save_reading_content(self):
        """Save reading content to current package"""
        reading_content = ReadingContent()
        reading_content.explanation = self.explanation_editor.get_text()
        reading_content.title = self.title_editor.get_text()
        
        for para_editor in self.paragraph_editors:
            paragraph = Paragraph()
            paragraph.title = para_editor['title'].get_text()
            paragraph.body = para_editor['body'].get_text()
            reading_content.paragraphs.append(paragraph)
        
        self.current_package.reading_content = reading_content
        self.status_bar.config(text="Reading content saved")
        messagebox.showinfo("Success", "Reading content saved successfully!")
    
    def create_question_groups_tab(self):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="Question Groups")
        
        # Toolbar
        toolbar = tk.Frame(tab)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(toolbar, text="Add Question Group", command=self.add_question_group).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="View Groups", command=self.view_question_groups).pack(side=tk.LEFT, padx=5)
        
        # Question group frame
        self.qg_frame = tk.Frame(tab)
        self.qg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_question_group(self):
        """Open dialog to add question group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Question Group")
        dialog.geometry("1000x750")
        dialog.minsize(860, 620)
        dialog.rowconfigure(0, weight=1)
        dialog.columnconfigure(0, weight=1)

        # Make dialog scrollable and responsive to resizing
        main_canvas = tk.Canvas(dialog, highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=main_canvas.yview)
        scrollable_dialog = tk.Frame(main_canvas)
        
        scrollable_dialog.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        dialog_window = main_canvas.create_window((0, 0), window=scrollable_dialog, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        def fit_dialog_content_to_canvas(event):
            main_canvas.itemconfigure(dialog_window, width=event.width)

        main_canvas.bind("<Configure>", fit_dialog_content_to_canvas)
        
        # Explanation
        tk.Label(scrollable_dialog, text="Explanation:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        explanation_editor = RichTextEditor(scrollable_dialog, height=3)
        explanation_editor.pack(fill=tk.X, padx=10, pady=5)
        
        # Question Type
        tk.Label(scrollable_dialog, text="Question Type:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        type_var = tk.StringVar(value=QuestionType.TYPE1.value)
        type_combo = ttk.Combobox(scrollable_dialog, textvariable=type_var, 
                                  values=[qt.value for qt in QuestionType], width=50, state='readonly')
        type_combo.pack(fill=tk.X, padx=10)
        
        # Additional inputs frame (for lists, images, etc.)
        additional_frame = tk.LabelFrame(scrollable_dialog, text="Additional Inputs (depends on question type)", 
                                        font=('Arial', 10, 'bold'), padx=10, pady=10)
        additional_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        additional_widgets = {}
        
        def update_additional_inputs(*args):
            """Update additional input fields based on question type"""
            # Clear existing widgets
            for widget in additional_frame.winfo_children():
                widget.destroy()
            additional_widgets.clear()
            
            selected_type = type_var.get()
            
            if selected_type == QuestionType.TYPE4.value:  # Matching information
                tk.Label(additional_frame, text="List of Information (one per line):", 
                        font=('Arial', 9)).pack(anchor=tk.W, pady=5)
                info_text = scrolledtext.ScrolledText(additional_frame, height=6, width=70)
                info_text.pack(fill=tk.X, pady=5)
                info_text.insert("1.0", "A. First piece of information\nB. Second piece of information\nC. Third piece of information")
                additional_widgets['infoList'] = info_text
                
            elif selected_type == QuestionType.TYPE5.value:  # Matching headings
                tk.Label(additional_frame, text="List of Headings (one per line):", 
                        font=('Arial', 9)).pack(anchor=tk.W, pady=5)
                heading_text = scrolledtext.ScrolledText(additional_frame, height=6, width=70)
                heading_text.pack(fill=tk.X, pady=5)
                heading_text.insert("1.0", "i. First heading\nii. Second heading\niii. Third heading")
                additional_widgets['headingList'] = heading_text
                
            elif selected_type == QuestionType.TYPE6.value:  # Matching features
                tk.Label(additional_frame, text="List of Features (one per line):", 
                        font=('Arial', 9)).pack(anchor=tk.W, pady=5)
                feature_text = scrolledtext.ScrolledText(additional_frame, height=6, width=70)
                feature_text.pack(fill=tk.X, pady=5)
                feature_text.insert("1.0", "A. Feature one\nB. Feature two\nC. Feature three")
                additional_widgets['featureList'] = feature_text
                
            elif selected_type == QuestionType.TYPE7.value:  # Matching sentence endings
                tk.Label(additional_frame, text="List of Sentence Endings (one per line):", 
                        font=('Arial', 9)).pack(anchor=tk.W, pady=5)
                ending_text = scrolledtext.ScrolledText(additional_frame, height=6, width=70)
                ending_text.pack(fill=tk.X, pady=5)
                ending_text.insert("1.0", "A. ending one.\nB. ending two.\nC. ending three.")
                additional_widgets['sentenceEndingList'] = ending_text
                
            elif selected_type == QuestionType.TYPE9.value:  # Summary/table/flow-chart
                tk.Label(additional_frame, text="Choose Input Type:", 
                        font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=5)
                
                input_type_var = tk.StringVar(value="Summary")
                input_type_frame = tk.Frame(additional_frame)
                input_type_frame.pack(anchor=tk.W, pady=5)
                
                tk.Radiobutton(input_type_frame, text="Summary/Note", variable=input_type_var, 
                              value="Summary").pack(side=tk.LEFT, padx=5)
                tk.Radiobutton(input_type_frame, text="Table", variable=input_type_var, 
                              value="Table").pack(side=tk.LEFT, padx=5)
                tk.Radiobutton(input_type_frame, text="Flow-chart", variable=input_type_var, 
                              value="Flowchart").pack(side=tk.LEFT, padx=5)
                
                # Content frame that changes based on selection
                content_frame = tk.Frame(additional_frame)
                content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
                
                def update_type9_input():
                    for widget in content_frame.winfo_children():
                        widget.destroy()
                    
                    input_type = input_type_var.get()
                    
                    if input_type == "Summary":
                        tk.Label(content_frame, text="Summary Text (use [1], [2], [3] for blanks):", 
                                font=('Arial', 9)).pack(anchor=tk.W)
                        summary_text = scrolledtext.ScrolledText(content_frame, height=8, width=70)
                        summary_text.pack(fill=tk.BOTH, pady=5)
                        summary_text.insert("1.0", "Enter your summary here. Use [1] for first blank, [2] for second blank, etc.\nExample: The bicycle was invented in [1] by [2].")
                        additional_widgets['summaryData'] = summary_text
                        additional_widgets['type9_mode'] = 'summary'
                    
                    elif input_type == "Table":
                        table_builder_frame = tk.LabelFrame(content_frame, text="Table Builder", 
                                                           font=('Arial', 9, 'bold'), padx=5, pady=5)
                        table_builder_frame.pack(fill=tk.BOTH, expand=True)
                        
                        # Table controls
                        control_frame = tk.Frame(table_builder_frame)
                        control_frame.pack(fill=tk.X, pady=5)
                        
                        tk.Label(control_frame, text="Rows:").pack(side=tk.LEFT, padx=5)
                        rows_var = tk.StringVar(value="3")
                        tk.Spinbox(control_frame, from_=2, to=10, textvariable=rows_var, width=5).pack(side=tk.LEFT)
                        
                        tk.Label(control_frame, text="Columns:").pack(side=tk.LEFT, padx=5)
                        cols_var = tk.StringVar(value="3")
                        tk.Spinbox(control_frame, from_=2, to=6, textvariable=cols_var, width=5).pack(side=tk.LEFT)
                        
                        table_data = {
                            'rows': rows_var,
                            'cols': cols_var,
                            'cells': {},
                            'selected_cell': None,
                            'font_family': 'Arial',
                            'font_size': 12
                        }

                        style_frame = tk.Frame(table_builder_frame)
                        style_frame.pack(fill=tk.X, pady=(0, 5))

                        tk.Label(style_frame, text="Cell Text Controls:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
                        tk.Label(style_frame, text="Size:").pack(side=tk.LEFT, padx=(8, 2))
                        font_size_var = tk.StringVar(value="12")
                        font_size_combo = ttk.Combobox(
                            style_frame,
                            textvariable=font_size_var,
                            values=['10', '11', '12', '13', '14', '16', '18'],
                            width=4,
                            state='readonly'
                        )
                        font_size_combo.pack(side=tk.LEFT)

                        def set_selected_cell(widget):
                            table_data['selected_cell'] = widget
                            widget.configure(highlightthickness=2, highlightbackground='#3498db', highlightcolor='#3498db')

                        def clear_other_cell_highlights(selected_widget):
                            for cell in table_data['cells'].values():
                                if cell != selected_widget:
                                    cell.configure(highlightthickness=1, highlightbackground='#d0d0d0', highlightcolor='#d0d0d0')

                        def apply_cell_style(style_name):
                            selected_cell = table_data.get('selected_cell')
                            if not selected_cell:
                                messagebox.showinfo("Select a table cell", "Click inside a cell first, then apply text style.")
                                return
                            try:
                                start = selected_cell.index('sel.first')
                                end = selected_cell.index('sel.last')
                            except tk.TclError:
                                start, end = '1.0', 'end-1c'

                            if style_name in selected_cell.tag_names('insert'):
                                selected_cell.tag_remove(style_name, start, end)
                            else:
                                selected_cell.tag_add(style_name, start, end)

                        def apply_font_size(event=None):
                            selected_cell = table_data.get('selected_cell')
                            if not selected_cell:
                                return
                            size = int(font_size_var.get())
                            table_data['font_size'] = size
                            selected_cell.configure(font=(table_data['font_family'], size))
                            selected_cell.tag_configure('bold', font=(table_data['font_family'], size, 'bold'))
                            selected_cell.tag_configure('italic', font=(table_data['font_family'], size, 'italic'))

                        tk.Button(style_frame, text='B', width=3, font=('Arial', 10, 'bold'),
                                  command=lambda: apply_cell_style('bold')).pack(side=tk.LEFT, padx=3)
                        tk.Button(style_frame, text='I', width=3, font=('Arial', 10, 'italic'),
                                  command=lambda: apply_cell_style('italic')).pack(side=tk.LEFT, padx=2)
                        font_size_combo.bind('<<ComboboxSelected>>', apply_font_size)

                        tk.Label(style_frame, text="Tip: select text in a cell and press B/I", 
                                font=('Arial', 8, 'italic')).pack(side=tk.LEFT, padx=10)

                        def create_table():
                            # Clear existing table
                            for widget in table_display_frame.winfo_children():
                                widget.destroy()

                            rows = int(rows_var.get())
                            cols = int(cols_var.get())
                            table_data['cells'] = {}
                            table_data['selected_cell'] = None

                            # Create table grid
                            for r in range(rows):
                                for c in range(cols):
                                    cell_entry = tk.Text(
                                        table_display_frame,
                                        width=34,
                                        height=5,
                                        wrap=tk.WORD,
                                        font=(table_data['font_family'], table_data['font_size']),
                                        relief=tk.SOLID,
                                        bd=1,
                                        padx=7,
                                        pady=6,
                                        undo=True
                                    )
                                    cell_entry.grid(row=r, column=c, padx=4, pady=4, sticky='nsew')
                                    cell_entry.tag_configure('bold', font=(table_data['font_family'], table_data['font_size'], 'bold'))
                                    cell_entry.tag_configure('italic', font=(table_data['font_family'], table_data['font_size'], 'italic'))
                                    cell_entry.configure(highlightthickness=1, highlightbackground='#d0d0d0', highlightcolor='#d0d0d0')
                                    cell_entry.bind('<FocusIn>', lambda e, w=cell_entry: (set_selected_cell(w), clear_other_cell_highlights(w)))

                                    # Pre-fill header row
                                    if r == 0:
                                        cell_entry.insert("1.0", f"Header {c+1}")

                                    table_data['cells'][f"{r},{c}"] = cell_entry

                            # Configure weights for easier expansion and editing
                            for r in range(rows):
                                table_display_frame.rowconfigure(r, weight=1)
                            for c in range(cols):
                                table_display_frame.columnconfigure(c, weight=1)

                        tk.Button(control_frame, text="Create Table", command=create_table,
                                 bg='#3498db', fg='white').pack(side=tk.LEFT, padx=10)

                        tk.Label(control_frame, text="Use [BLANK] or [1], [2], etc. for gaps",
                                font=('Arial', 8, 'italic')).pack(side=tk.LEFT, padx=10)

                        # Table display area with scrollbar
                        table_scroll_frame = tk.Frame(table_builder_frame)
                        table_scroll_frame.pack(fill=tk.BOTH, expand=True, pady=5)

                        table_canvas = tk.Canvas(table_scroll_frame, height=420)
                        table_scrollbar = tk.Scrollbar(table_scroll_frame, orient="vertical",
                                                      command=table_canvas.yview)
                        table_scrollbar_x = tk.Scrollbar(table_scroll_frame, orient="horizontal",
                                                         command=table_canvas.xview)
                        table_display_frame = tk.Frame(table_canvas)

                        table_display_frame.bind("<Configure>",
                                                lambda e: table_canvas.configure(scrollregion=table_canvas.bbox("all")))

                        table_canvas.create_window((0, 0), window=table_display_frame, anchor="nw")
                        table_canvas.configure(
                            yscrollcommand=table_scrollbar.set,
                            xscrollcommand=table_scrollbar_x.set
                        )

                        table_canvas.pack(side="left", fill="both", expand=True)
                        table_scrollbar.pack(side="right", fill="y")
                        table_scrollbar_x.pack(side="bottom", fill="x")

                        # Create initial table
                        create_table()

                        additional_widgets['tableData'] = table_data
                        additional_widgets['type9_mode'] = 'table'
                    
                    else:  # Flowchart
                        flowchart_frame = tk.LabelFrame(content_frame, text="Flow-chart Builder",
                                                       font=('Arial', 9, 'bold'), padx=5, pady=5)
                        flowchart_frame.pack(fill=tk.BOTH, expand=True)
                        
                        tk.Label(flowchart_frame, text="Flow-chart Structure (use → for arrows, [BLANK] for gaps):",
                                font=('Arial', 9)).pack(anchor=tk.W, pady=5)
                        
                        # Flowchart text editor
                        flowchart_text = scrolledtext.ScrolledText(flowchart_frame, height=10, width=70)
                        flowchart_text.pack(fill=tk.BOTH, expand=True, pady=5)
                        
                        flowchart_template = """Enter your flow-chart structure here. Examples:

Simple flow:
[Start] → [Process 1] → [BLANK] → [End]

Vertical flow:
┌─────────────┐
│   Start     │
└─────────────┘
       ↓
┌─────────────┐
│   [1]       │  ← Use [1], [2] for blanks
└─────────────┘
       ↓
┌─────────────┐
│   End       │
└─────────────┘

Or describe it:
Step 1: Starting point
   ↓
Step 2: [BLANK] (to be filled)
   ↓
Step 3: Final outcome
"""
                        flowchart_text.insert("1.0", flowchart_template)
                        
                        # Flowchart tools
                        tools_frame = tk.Frame(flowchart_frame)
                        tools_frame.pack(fill=tk.X, pady=5)
                        
                        tk.Label(tools_frame, text="Quick Insert:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=5)
                        
                        def insert_symbol(symbol):
                            flowchart_text.insert(tk.INSERT, symbol)
                        
                        symbols = [
                            ("→", "→"), ("↓", "↓"), ("↑", "↑"), ("←", "←"),
                            ("Box", "\n┌─────────────┐\n│             │\n└─────────────┘\n"),
                            ("[BLANK]", "[BLANK]"),
                            ("Decision", "\n    ╱────────╲\n   ╱          ╲\n  ╱            ╲\n  ╲            ╱\n   ╲          ╱\n    ╲────────╱\n")
                        ]
                        
                        for label, symbol in symbols:
                            tk.Button(tools_frame, text=label, 
                                     command=lambda s=symbol: insert_symbol(s),
                                     width=8).pack(side=tk.LEFT, padx=2)
                        
                        additional_widgets['flowchartData'] = flowchart_text
                        additional_widgets['type9_mode'] = 'flowchart'
                
                # Bind radio buttons
                for widget in input_type_frame.winfo_children():
                    if isinstance(widget, tk.Radiobutton):
                        widget.configure(command=update_type9_input)
                
                additional_widgets['type9_selector'] = input_type_var
                update_type9_input()  # Initialize
                
            elif selected_type == QuestionType.TYPE10.value:  # Diagram label completion
                tk.Label(additional_frame, text="Diagram Description/Image Path:", 
                        font=('Arial', 9)).pack(anchor=tk.W, pady=5)
                diagram_text = scrolledtext.ScrolledText(additional_frame, height=4, width=70)
                diagram_text.pack(fill=tk.X, pady=5)
                diagram_text.insert("1.0", "Enter diagram description or image file path")
                additional_widgets['diagramImage'] = diagram_text
            else:
                tk.Label(additional_frame, text="No additional inputs required for this question type.", 
                        font=('Arial', 9, 'italic'), fg='gray').pack(pady=10)
        
        # Bind the update function to type change
        type_combo.bind('<<ComboboxSelected>>', update_additional_inputs)
        update_additional_inputs()  # Initialize
        
        # Questions section
        tk.Label(scrollable_dialog, text="Questions (min 2, max 10):", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        
        questions_container = tk.Frame(scrollable_dialog)
        questions_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        question_entries = []
        
        def add_question_field():
            if len(question_entries) >= 10:
                messagebox.showwarning("Limit", "Maximum 10 questions per group")
                return
            
            q_frame = tk.LabelFrame(questions_container, text=f"Question {len(question_entries)+1}", 
                                   font=('Arial', 9, 'bold'), padx=5, pady=5)
            q_frame.pack(fill=tk.X, pady=5)
            
            # Question text
            tk.Label(q_frame, text="Question Text:").pack(anchor=tk.W, padx=5)
            q_text = tk.Entry(q_frame, width=80)
            q_text.pack(fill=tk.X, padx=5, pady=2)
            
            question_data = {'text': q_text, 'frame': q_frame}
            
            # Get current question type
            current_type = type_var.get()
            
            # Type 1: Multiple choice - need choices
            if current_type == QuestionType.TYPE1.value:
                tk.Label(q_frame, text="Choices (one per line):").pack(anchor=tk.W, padx=5, pady=2)
                choices_text = scrolledtext.ScrolledText(q_frame, height=4, width=70)
                choices_text.pack(fill=tk.X, padx=5, pady=2)
                choices_text.insert("1.0", "A. Choice one\nB. Choice two\nC. Choice three\nD. Choice four")
                question_data['choices'] = choices_text
                
                tk.Label(q_frame, text="Correct Answer (A, B, C, or D):").pack(anchor=tk.W, padx=5)
                q_answer = tk.Entry(q_frame, width=20)
                q_answer.pack(anchor=tk.W, padx=5, pady=2)
                question_data['answer'] = q_answer
            
            # Types 2 & 3: True/False/Not Given or Yes/No/Not Given
            elif current_type in [QuestionType.TYPE2.value, QuestionType.TYPE3.value]:
                answer_options = ['TRUE', 'FALSE', 'NOT GIVEN'] if current_type == QuestionType.TYPE2.value else ['YES', 'NO', 'NOT GIVEN']
                tk.Label(q_frame, text=f"Correct Answer ({'/'.join(answer_options)}):").pack(anchor=tk.W, padx=5)
                answer_var = tk.StringVar(value=answer_options[0])
                answer_combo = ttk.Combobox(q_frame, textvariable=answer_var, values=answer_options, 
                                           width=20, state='readonly')
                answer_combo.pack(anchor=tk.W, padx=5, pady=2)
                question_data['answer'] = answer_var
            
            # Types 4-7: Matching types - answer is letter/number
            elif current_type in [QuestionType.TYPE4.value, QuestionType.TYPE5.value, 
                                 QuestionType.TYPE6.value, QuestionType.TYPE7.value]:
                tk.Label(q_frame, text="Correct Answer (letter or number from the list):").pack(anchor=tk.W, padx=5)
                q_answer = tk.Entry(q_frame, width=20)
                q_answer.pack(anchor=tk.W, padx=5, pady=2)
                question_data['answer'] = q_answer
            
            # Types 8, 9, 10, 11: Text answer
            else:
                tk.Label(q_frame, text="Correct Answer:").pack(anchor=tk.W, padx=5)
                q_answer = tk.Entry(q_frame, width=60)
                q_answer.pack(anchor=tk.W, padx=5, pady=2)
                question_data['answer'] = q_answer
            
            # Remove button
            def remove_this_question():
                question_entries.remove(question_data)
                q_frame.destroy()
            
            tk.Button(q_frame, text="Remove Question", command=remove_this_question, 
                     bg='#e74c3c', fg='white').pack(anchor=tk.E, padx=5, pady=5)
            
            question_entries.append(question_data)
        
        # Add question button
        btn_frame = tk.Frame(scrollable_dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(btn_frame, text="+ Add Question", command=add_question_field,
                 bg='#3498db', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Add initial question fields
        for _ in range(2):
            add_question_field()
        
        # Save button
        def save_group():
            # Validate
            if len(question_entries) < 2:
                messagebox.showerror("Error", "Minimum 2 questions required")
                return
            
            # Create question group
            qg = QuestionGroup()
            qg.explanation = explanation_editor.get_text()
            
            # Set type
            for qt in QuestionType:
                if qt.value == type_var.get():
                    qg.type = qt
                    break
            
            # Collect additional inputs
            additional_data = {}
            for key, widget in additional_widgets.items():
                if key == 'type9_mode':
                    continue  # Skip mode indicator
                elif key == 'type9_selector':
                    continue  # Skip selector
                elif key == 'tableData':
                    # Extract table data
                    table_info = widget
                    rows = int(table_info['rows'].get())
                    cols = int(table_info['cols'].get())
                    
                    table_content = []
                    for r in range(rows):
                        row_data = []
                        for c in range(cols):
                            cell = table_info['cells'].get(f"{r},{c}")
                            if cell:
                                row_data.append(cell.get("1.0", "end-1c"))
                            else:
                                row_data.append("")
                        table_content.append(row_data)
                    
                    additional_data['tableData'] = {
                        'rows': rows,
                        'cols': cols,
                        'content': table_content
                    }
                elif key == 'flowchartData':
                    content = widget.get("1.0", "end-1c").strip()
                    if content:
                        additional_data['flowchartData'] = content
                elif isinstance(widget, scrolledtext.ScrolledText):
                    content = widget.get("1.0", "end-1c").strip()
                    if content:
                        if key in ['infoList', 'headingList', 'featureList', 'sentenceEndingList']:
                            # Split by lines for lists
                            additional_data[key] = [line.strip() for line in content.split('\n') if line.strip()]
                        else:
                            additional_data[key] = content
            
            if additional_data:
                qg.additional_inputs = AdditionalInput(input_type=qg.type.value, data=additional_data)
            
            # Add questions
            for i, qe in enumerate(question_entries):
                q = Question()
                q.question_id = f"{self.current_package.package_id}_qg{len(self.current_package.question_groups)}_q{i}"
                q.text = qe['text'].get().strip()
                
                if not q.text:
                    continue
                
                # Get answer based on type
                if 'choices' in qe:
                    # Type 1: Store choices in question text or additional data
                    choices = qe['choices'].get("1.0", "end-1c").strip()
                    q.text = f"{q.text}\n{choices}"
                    answer_widget = qe['answer']
                    q.answer = answer_widget.get().strip().upper() if isinstance(answer_widget, tk.Entry) else answer_widget.get()
                elif isinstance(qe['answer'], tk.StringVar):
                    q.answer = qe['answer'].get()
                else:
                    q.answer = qe['answer'].get().strip()
                
                if q.text and q.answer:
                    qg.questions.append(q)
            
            if not qg.validate():
                messagebox.showerror("Error", "Question group must have 2-10 valid questions with answers")
                return
            
            self.current_package.question_groups.append(qg)
            self.status_bar.config(text=f"Question group added. Total groups: {len(self.current_package.question_groups)}")
            messagebox.showinfo("Success", f"Question group added successfully!\nTotal questions: {len(qg.questions)}")
            dialog.destroy()
        
        save_btn = tk.Button(scrollable_dialog, text="Save Question Group", command=save_group, 
                            bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), width=20, height=2)
        save_btn.pack(pady=15)
        
        # Pack canvas and scrollbar
        main_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
    
    def view_question_groups(self):
        """View all question groups"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Question Groups")
        dialog.geometry("800x600")
        
        text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if not self.current_package.question_groups:
            text.insert("1.0", "No question groups added yet.")
        else:
            for i, qg in enumerate(self.current_package.question_groups):
                text.insert("end", f"\n{'='*60}\n")
                text.insert("end", f"Question Group {i+1}\n")
                text.insert("end", f"{'='*60}\n")
                text.insert("end", f"Type: {qg.type.value}\n")
                text.insert("end", f"Explanation: {qg.explanation}\n")
                text.insert("end", f"Number of questions: {len(qg.questions)}\n\n")
                
                for j, q in enumerate(qg.questions):
                    text.insert("end", f"Q{j+1}: {q.text}\n")
                    text.insert("end", f"Answer: {q.answer}\n\n")
        
        text.config(state=tk.DISABLED)
    
    def new_package(self):
        """Create new package"""
        if messagebox.askyesno("New Package", "Create a new package? Unsaved changes will be lost."):
            self.current_package = ReadingPackage()
            self.current_package.package_id = str(uuid.uuid4())
            
            # Clear editors
            self.explanation_editor.clear()
            self.title_editor.clear()
            for para in self.paragraph_editors:
                para['container'].destroy()
            self.paragraph_editors = []
            
            self.status_bar.config(text="New package created")
    
    def save_package(self):
        """Save package to file"""
        if not self.current_package.reading_content.title:
            messagebox.showerror("Error", "Please add reading content first")
            return
        
        if not self.current_package.question_groups:
            messagebox.showerror("Error", "Please add at least one question group")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                self.current_package.save_to_file(filepath)
                self.status_bar.config(text=f"Package saved: {filepath}")
                messagebox.showinfo("Success", f"Package saved successfully to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save package:\n{str(e)}")
    
    def open_package(self):
        """Open existing package"""
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                self.current_package = ReadingPackage.load_from_file(filepath)
                
                # Load reading content
                self.explanation_editor.set_text(self.current_package.reading_content.explanation)
                self.title_editor.set_text(self.current_package.reading_content.title)
                
                # Clear existing paragraphs
                for para in self.paragraph_editors:
                    para['container'].destroy()
                self.paragraph_editors = []
                
                # Load paragraphs
                for para in self.current_package.reading_content.paragraphs:
                    self.add_paragraph()
                    self.paragraph_editors[-1]['title'].set_text(para.title)
                    self.paragraph_editors[-1]['body'].set_text(para.body)
                
                self.status_bar.config(text=f"Package loaded: {filepath}")
                messagebox.showinfo("Success", "Package loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load package:\n{str(e)}")


def main():
    root = tk.Tk()
    app = ContentEditorWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
