import subprocess
import sys
import time
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    print("==================================================")
    print("🚀 Launching AI Loan Predictor (Python Stack)")
    print("==================================================")
    
    python_exe = sys.executable

    # 1. Start FastAPI backend server on port 8000
    print("\n1. Starting FastAPI Backend (Uvicorn) on port 8000...")
    backend_cmd = [python_exe, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    backend_proc = subprocess.Popen(backend_cmd)

    time.sleep(2)

    # 2. Start Streamlit Frontend on port 8501
    print("\n2. Starting Streamlit Frontend on port 8501...")
    frontend_cmd = [python_exe, "-m", "streamlit", "run", os.path.join("frontend", "Home.py"), "--server.port", "8501"]
    
    try:
        frontend_proc = subprocess.Popen(frontend_cmd)
        print("\n==================================================")
        print("✅ AI Loan Predictor System Launched Successfully!")
        print("🌐 Streamlit Web Interface: http://localhost:8501")
        print("⚡ FastAPI REST API Docs:   http://localhost:8000/docs")
        print("==================================================\n")
        
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping AI Loan Predictor processes...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
