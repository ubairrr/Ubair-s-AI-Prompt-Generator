<div align="center">
  <h1>✨ AI Prompt Studio ✨</h1>
  <p><strong>Transform simple ideas into precision-crafted AI prompts using the Gemini 2.5 Flash model and our custom 4-D Methodology.</strong></p>
  
  <p>
    <a href="https://github.com/ubairrr/Ubair-s-AI-Prompt-Generator/stargazers"><img src="https://img.shields.io/github/stars/ubairrr/Ubair-s-AI-Prompt-Generator?style=for-the-badge&color=yellow" alt="Stars"></a>
    <a href="https://github.com/ubairrr/Ubair-s-AI-Prompt-Generator/network/members"><img src="https://img.shields.io/github/forks/ubairrr/Ubair-s-AI-Prompt-Generator?style=for-the-badge&color=blue" alt="Forks"></a>
    <a href="https://github.com/ubairrr/Ubair-s-AI-Prompt-Generator/issues"><img src="https://img.shields.io/github/issues/ubairrr/Ubair-s-AI-Prompt-Generator?style=for-the-badge&color=red" alt="Issues"></a>
    <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge" alt="License"></a>
  </p>
</div>

<br/>

## 📖 Overview

**AI Prompt Studio** is a powerful web-based application built with Flask that takes your basic ideas and turns them into highly optimized, master-level AI prompts. Powered by **Google's Gemini 2.5 Flash API**, it acts as your personal prompt engineering specialist, ensuring you get the absolute best performance out of any LLM you use.

The application features a sleek, brutalist-inspired UI design that focuses on typography and usability, providing an unopinionated, frictionless experience.

## ✨ Features

- **🚀 AI-Powered Optimization**: Leverages the lightning-fast Gemini 2.5 Flash model for instantaneous prompt generation.
- **🧠 4-D Methodology Engine**: Systematically deconstructs, diagnoses, develops, and delivers the ultimate prompt tailored to your input.
- **📊 Sectioned Output**: Clearly separates the final prompt, key improvements, applied techniques, and expert tips for unparalleled clarity.
- **📋 One-Click Copy**: Easily copy just your optimized prompt directly to your clipboard securely—no extra fluff included.
- **🎨 Premium UI/UX**: Designed with a professional, minimalist editorial aesthetic featuring engaging micro-animations and responsive layout.

---

## 📐 The 4-D Methodology

AI Prompt Studio strictly adheres to a robust heuristic framework to guarantee prompt perfection:

1. **Deconstruct**: Extracts core intent, context, and output requirements from your rough idea.
2. **Diagnose**: Audits the input for ambiguity, clarity gaps, and structural formatting needs.
3. **Develop**: Enhances the request utilizing advanced strategies (chain-of-thought, multi-perspective, few-shot generation, etc.).
4. **Deliver**: Formats and presents the optimal prompt accompanied by actionable implementation advice.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, `requests`
- **Frontend**: HTML5, Vanilla CSS3 (Brutalist/Editorial Aesthetic), Vanilla JavaScript
- **AI Integration**: Custom payload to Google Generative AI (`gemini-2.5-flash` model endpoint)
- **Icons**: [Lucide Icons](https://lucide.dev/)

---

## 🚀 Getting Started

Follow these steps to set up and run the AI Prompt Studio locally.

### 1. Clone the repository
```bash
git clone https://github.com/ubairrr/Ubair-s-AI-Prompt-Generator.git
cd Ubair-s-AI-Prompt-Generator
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(If `requirements.txt` is not provided, simply run: `pip install flask requests python-dotenv`)*

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API key:
```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```
> **Note:** You can grab your free API key from [Google AI Studio](https://aistudio.google.com/).

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to start engineering incredible prompts!

---

## 💡 How to Use

1. **Enter Idea**: Type an idea or a vague prompt in the main input field (e.g., *"Write a story about a space pirate"*).
2. **Generate**: Click the **GENERATE** button. The app will communicate with the Gemini AI model behind the scenes.
3. **Review**: Analyze the structured response containing your optimized prompt alongside the techniques and tips applied.
4. **Copy**: Hit the **COPY** button on the panel header to immediately save the prompt to your clipboard and drop it into ChatGPT, Claude, Gemini, or any other AI tool!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! 
Feel free to check out the [issues page](https://github.com/ubairrr/Ubair-s-AI-Prompt-Generator/issues) to see where you can help out.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

<br/>

<div align="center">
  <b>Built with ❤️ by <a href="https://github.com/ubairrr">ubairrr</a></b>
</div>
