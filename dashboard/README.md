# Blockchain Voting System - Dashboard

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation & Running

#### Option 1: Using Virtual Environment (Recommended)

1. **Navigate to the dashboard directory:**
   ```bash
   cd dashboard
   ```

2. **Create a virtual environment:**
   ```bash
   # On Windows
   python -m venv venv
   
   # On macOS/Linux
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # On Windows (Command Prompt)
   venv\Scripts\activate.bat
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

#### Option 2: Direct Installation (Without Virtual Environment)

1. **Navigate to the dashboard directory:**
   ```bash
   cd dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

### Accessing the Dashboard

Once the application is running, you'll see:
```
🚀 Blockchain Voting Dashboard Starting...
📊 Dashboard: http://localhost:5000
🔗 API Status: http://localhost:5000/api/status
📈 Live Statistics: http://localhost:5000/api/statistics
```

**Open your web browser and navigate to:**
- **Main Dashboard:** http://localhost:5000
- **API Status:** http://localhost:5000/api/status
- **Statistics API:** http://localhost:5000/api/statistics

### Features

- ✅ Real-time blockchain statistics
- ✅ Candidate voting results with visual progress bars
- ✅ Blockchain explorer with block navigation
- ✅ Chain verification system
- ✅ Recent activity feed
- ✅ System status monitoring
- ✅ Auto-refresh every 15 seconds

### Troubleshooting

**Port already in use?**
- The app runs on port 5000 by default
- If port 5000 is busy, modify `app.py` line 247 to use a different port:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

**Module not found errors?**
- Make sure you've installed all requirements: `pip install -r requirements.txt`
- Verify you're in the correct directory (dashboard folder)

**Dashboard not loading?**
- Check the terminal for error messages
- Ensure Flask is installed: `pip install Flask`
- Try accessing http://127.0.0.1:5000 instead of localhost

### Stopping the Application

Press `Ctrl + C` in the terminal to stop the server.

