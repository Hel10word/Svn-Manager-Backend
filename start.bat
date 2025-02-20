@echo off
REM Change the python version if necessary
set PYTHON_VERSION=python

REM Check if virtual environment already exists, if not create one
if not exist "venv" (
    echo Creating virtual environment...
    %PYTHON_VERSION% -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install the dependencies from requirements.txt, if they haven't already been installed
pip install -r requirements.txt

REM Run your application (Replace the following line with the command to run your Python app)
%PYTHON_VERSION% run.py

REM Pause the script on completion so the window doesn't close immediately
echo.
echo Startup complete, press any key to exit.
pause >nul
exit