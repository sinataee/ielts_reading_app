# IELTS Reading Test Application

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/yourusername/ielts-reading-app)

A comprehensive desktop application for creating, taking, and scoring IELTS Academic Reading tests. Built with Python and Tkinter.

![IELTS Reading App Screenshot](docs/screenshot.png)

## 🌟 Features

### Content Editor
- 📝 Rich text editing with formatting (bold, italic, headers, alignment)
- 📄 Create reading passages with multiple paragraphs
- ❓ Support for all 11 IELTS question types
- 📊 Visual table builder for Type 9 questions
- 🔄 Graphical flow-chart builder
- 💾 Save and load reading packages as JSON files
- ✅ Automatic validation (2-10 questions per group)

### Exam Engine
- 🖥️ Fullscreen exam interface
- ⏱️ 60-minute countdown timer with pause/resume
- 🎨 Text highlighting system (4 colors)
- 📋 Professional table and flow-chart rendering
- 💡 Real-time answer recording
- 🔒 Automatic submission when time expires

### Result Engine
- 🎯 IELTS band score calculation (0-9 scale)
- 📊 Comprehensive result display
- ✅ Question-by-question feedback
- 📈 Performance statistics by question type
- 💾 Export results to JSON

## 📋 Question Types Supported

1. ✅ Multiple Choice
2. ✅ True/False/Not Given
3. ✅ Yes/No/Not Given
4. ✅ Matching Information
5. ✅ Matching Headings
6. ✅ Matching Features
7. ✅ Matching Sentence Endings
8. ✅ Sentence Completion
9. ✅ Summary/Table/Flow-chart Completion (with visual builders)
10. ✅ Diagram Label Completion
11. ✅ Short Answer Questions

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ielts-reading-app.git
   cd ielts-reading-app
   ```

2. **Verify installation**
   ```bash
   python test_installation.py
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### First Steps

1. Click **"Create Sample Package"** to generate an example test
2. Click **"Take Exam"** and select the sample package
3. Click **"Start Exam"** and complete the test
4. View your results with detailed feedback

## 📖 Usage

### Creating a Test Package

1. Launch the application: `python main.py`
2. Click **"Content Editor"**
3. Add reading content (title, paragraphs)
4. Add question groups:
   - Select question type
   - Enter questions and answers
   - For Type 9, use visual table/flowchart builders
5. Save package: File → Save Package

### Taking a Test

1. Click **"Take Exam"**
2. Select a package file (.json)
3. Click **"Start Exam"**
4. Use highlighting tools to mark important text
5. Answer all questions
6. Click **"End Exam"** or wait for timer

### Viewing Results

Results display automatically showing:
- Band score (0-9)
- Correct/Incorrect/Unanswered counts
- Detailed feedback
- Performance by question type
- Option to export results

## 📚 Documentation

- [Installation Guide](INSTALL_GUIDE.md) - Detailed setup instructions
- [Quick Start Guide](QUICK_START.txt) - Fast reference
- [Question Types Guide](QUESTION_TYPES_GUIDE.md) - Input requirements for each type
- [Update Notes](UPDATE_NOTES_v1.2.md) - Version history and changes

## 🏗️ Architecture

```
ielts-reading-app/
├── main.py                    # Application launcher
├── models.py                  # Data models
├── content_editor.py          # Content creation module
├── exam_engine.py             # Test-taking module
├── result_engine.py           # Results and scoring
├── test_installation.py       # Installation verification
├── requirements.txt           # Dependencies
└── docs/                      # Documentation
```

### Key Components

- **Models**: Data structures (ReadingPackage, QuestionGroup, Question, etc.)
- **Content Editor**: Rich text editing, question creation, table/flowchart builders
- **Exam Engine**: Fullscreen interface, timer, highlighting, rendering
- **Result Engine**: Scoring, feedback, statistics, export

## 🎨 Screenshots

### Content Editor
![Content Editor](docs/content-editor.png)

### Exam Interface
![Exam Interface](docs/exam-interface.png)

### Results Display
![Results](docs/results.png)

## 🔧 Technical Details

### Built With

- **Python 3.7+** - Programming language
- **Tkinter** - GUI framework
- **JSON** - Data storage format

### IELTS Scoring System

The application uses official IELTS Academic Reading band score conversion:

| Correct Answers | Band Score |
|----------------|------------|
| 39-40          | 9.0        |
| 37-38          | 8.5        |
| 35-36          | 8.0        |
| 33-34          | 7.5        |
| 30-32          | 7.0        |
| 27-29          | 6.5        |
| 23-26          | 6.0        |

## 🐛 Troubleshooting

### tkinter not found

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Reinstall Python with tcl/tk option checked

### Application won't start fullscreen

This is normal on some window managers. The app will open in a maximized window instead.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on Cambridge IELTS test format specifications
- Designed for IELTS test preparation
- Built following software engineering best practices

## 📧 Contact

Project Link: [https://github.com/yourusername/ielts-reading-app](https://github.com/yourusername/ielts-reading-app)

## 🗺️ Roadmap

- [ ] User authentication system
- [ ] Database storage for packages
- [ ] Progress tracking across tests
- [ ] PDF export
- [ ] Listening section support
- [ ] Writing task modules
- [ ] Mobile version

## 📊 Version History

### v1.2 (Current)
- Enhanced Type 9 with visual table/flowchart builders
- Fullscreen exam interface
- Improved text highlighting in tables and flowcharts
- Better visual display of complex content

### v1.1
- Fixed question type input requirements
- Added comprehensive question types guide
- Improved multiple choice display
- Enhanced matching question dropdowns

### v1.0
- Initial release
- All 11 question types supported
- Complete exam workflow
- IELTS band scoring

---

**Made with ❤️ for IELTS test preparation**
