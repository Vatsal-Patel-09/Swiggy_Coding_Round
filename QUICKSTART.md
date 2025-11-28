# 🚀 QUICK START GUIDE

## Ready to run your Interactive Story Generator!

### Step 1: Install Dependencies (One-time setup)

```powershell
pip install -r requirements.txt
```

**Expected output**: Installation of streamlit, google-generativeai, pydantic, python-dotenv

---

### Step 2: Launch the Application

**Easy way:**
```powershell
.\run.ps1
```

**Or directly:**
```powershell
streamlit run app.py
```

---

### Step 3: Use the App

1. Browser opens at `http://localhost:8501`
2. Enter your story idea (e.g., "A detective solving a mystery in a haunted mansion")
3. Click **🚀 Start Story**
4. Read the generated scene
5. Click one of the two choices
6. Continue making choices to shape your story!

---

## ⚡ First Time Testing

Try this example to test the app:

**Story Prompt**: 
> "A young wizard discovers a mysterious portal in their school library"

**Expected Result**:
- Opening scene describing the discovery
- 2 choices like:
  1. "Step through the portal to investigate"
  2. "Run to find a teacher for help"

---

## 🐛 Troubleshooting

**Problem**: Import errors
- **Solution**: Run `pip install -r requirements.txt` in your venv

**Problem**: API key error
- **Solution**: Check `.env` file has `GEMINI_API_KEY=your_actual_key`

**Problem**: Port already in use
- **Solution**: Add `--server.port 8502` to streamlit command

---

## 📁 Project Files

- `app.py` - Main application (run this)
- `requirements.txt` - Dependencies
- `.env` - Your API key
- `README.md` - Full documentation
- `BUILD_COMPLETE.md` - Build summary

---

## 🎯 What's Been Validated

✅ All Python files have no syntax errors  
✅ Modular architecture implemented  
✅ Type hints throughout  
✅ Error handling in place  
✅ UI components created  
✅ Gemini API integration ready  

---

## 🎉 You're All Set!

The application is fully built and ready to test. 

**Next step**: Install dependencies and run the app!

```powershell
pip install -r requirements.txt
streamlit run app.py
```

Enjoy your interactive storytelling experience! 📖✨
