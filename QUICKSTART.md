# 🚀 Quick Start Guide - DocBot Advisor

Get up and running with DocBot in under 5 minutes!

---

## ⚡ Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.8+ installed ([Download](https://www.python.org/downloads/))
- [ ] Git installed ([Download](https://git-scm.com/downloads))
- [ ] OpenRouter or OpenAI API key ([Get OpenRouter key](https://openrouter.ai/keys))

---

## 📥 Installation (3 Steps)

### Step 1: Clone & Navigate

```bash
git clone https://github.com/Saranya1092/DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare.git
cd DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Configure API Key

```bash
# Copy the example file
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux
```

Edit `.env` and add your API key:

```env
OPENROUTER_API_KEY=sk-or-v1-YOUR_ACTUAL_KEY_HERE
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🎯 First Steps

1. **Upload a Document**
   - Click "Browse files" in the sidebar
   - Upload a PDF, DOCX, or TXT file (try the sample: `localresource/DietaryGuidelinesforNINwebsite.pdf`)

2. **Process It**
   - Click "Process Data" button
   - Wait 10-30 seconds for embedding

3. **Ask a Question**
   - Type: "What are the key dietary guidelines?"
   - Press Enter
   - Get your AI-powered answer!

---

## 🐛 Common Issues & Fixes

### Issue 1: "ModuleNotFoundError"
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "API key missing"
```bash
# Solution: Check your .env file
# Make sure it contains:
OPENROUTER_API_KEY=sk-or-v1-...
```

### Issue 3: "Port already in use"
```bash
# Solution: Use a different port
streamlit run app.py --server.port 8502
```

### Issue 4: ChromaDB errors
```bash
# Solution: Clear the database
# Windows:
Remove-Item -Recurse -Force chromadb_store/
# Mac/Linux:
rm -rf chromadb_store/
```

---

## 📚 Example Use Cases

### Healthcare Clinic Example
```
1. Upload: "Treatment_Protocol_Diabetes.pdf"
2. Ask: "What is the recommended insulin dosage for Type 2 diabetes?"
3. Get: Contextual answer with source citations
```

### Medical Student Example
```
1. Upload: "Anatomy_Textbook_Chapter5.pdf"
2. Ask: "Explain the cardiovascular system in simple terms"
3. Get: Simplified explanation with references
```

### Drug Reference Example
```
1. Upload: "Pharmacology_Manual.pdf"
2. Ask: "What are the side effects of metformin?"
3. Get: Comprehensive list with dosage info
```

---

## 🎓 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [Architecture section](README.md#architecture)
- Explore [Use Cases](README.md#use-cases) for your industry
- Join discussions in [GitHub Issues](https://github.com/Saranya1092/DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare/issues)

---

## 💡 Pro Tips

1. **Better Results**: Use focused documents (protocols, manuals) instead of entire textbooks
2. **Faster Processing**: Smaller chunk sizes (500-800) work better for medical documents
3. **Accurate Answers**: Ask specific questions with context (e.g., "For adult patients, what is...")
4. **Save Costs**: Use OpenRouter with cheaper models for testing (e.g., `mistralai/mistral-7b-instruct`)

---

## 🆘 Need Help?

- **Documentation**: See [README.md](README.md)
- **Report Bugs**: [GitHub Issues](https://github.com/Saranya1092/DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/Saranya1092/DocBot-Advisor-A-RAG-Based-Conversational-AI-Assistant-for-Healthcare/issues)

---

<div align="center">

**✅ You're all set! Start asking questions to your documents! 🎉**

Made with 💙 for Healthcare Professionals

</div>
