@echo off
REM Quick launcher for HebiKata MVP

echo.
echo ======================================
echo   🐍 HebiKata - Python Kata Dojo 🐍
echo ======================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: uv venv
    echo Then: uv pip install pyyaml streamlit pytest
    pause
    exit /b 1
)

REM Activate and run
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Launching Streamlit app...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

streamlit run app\main.py

pause
