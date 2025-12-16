
@echo off
echo Installing dependencies...
py -m pip install -r understar/requirements.txt
if %errorlevel% neq 0 (
    echo "py" failed, trying "python"...
    python -m pip install -r understar/requirements.txt
)

echo Starting UnderStar-OS...
py exemple.py
if %errorlevel% neq 0 (
    echo "py" failed, trying "python"...
    python exemple.py
)
pause
