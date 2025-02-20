# AI QUIZ APP 🤖

An AI-powered quiz generator that creates intelligent multiple-choice questions from any text input. Built with Python, Streamlit, and GitHub AI for seamless quiz creation and assessment.

## ✨ Features

- **Instant Quiz Generation**: Convert any text into MCQ questions
- **AI-Powered**: Utilizes GitHub's AI model for intelligent question creation
- **User-Friendly**: Clean, modern interface built with Streamlit
- **Difficulty Levels**: Choose between Easy, Medium, and Hard
- **Instant Scoring**: Get immediate feedback on your answers

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- GitHub Token
- Internet connection

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/abhishek-kumar-5031/AI-QUIZ-APP.git
cd AI-QUIZ-APP
```

2. **Set Up Environment**
```bash
# Create virtual environment
python -m venv quiz_env

# Activate it (Windows)
quiz_env\Scripts\activate
```

3. **Install Requirements**
```bash
pip install -r requirements.txt
```

4. **Configure GitHub Token**
Create a `.env` file:
```
GITHUB_TOKEN=your_github_token_here
```

5. **Run the App**
```bash
streamlit run quizapp.py
```

## 💻 How to Use

1. Launch the application
2. Paste your text content in the input area
3. Select difficulty level
4. Click "Generate Quiz"
5. Answer the questions and submit
6. View your score and correct answers

## 📦 Dependencies

```
streamlit==1.31.1
openai==1.12.0
python-dotenv==1.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔑 Environment Variables

Create a `.env` file in the root directory:
```
GITHUB_TOKEN=your_github_token_here
```

## 🛠️ Troubleshooting

**Common Issues:**
1. Token Error: Verify GitHub token in `.env`
2. Installation Issues: Ensure Python 3.8+ and all dependencies are installed
3. Quiz Generation Issues: Check internet connection and token validity

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Abhishek Kumar

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by GitHub AI

---
Made with ❤️ by Abhishek Kumar