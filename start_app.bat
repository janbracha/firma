@echo off
echo.
echo =================================================
echo          🚀 FIREMNI APLIKACE 🚀
echo =================================================
echo.
echo Spoustim aplikaci...
echo.

cd /d "C:\git\firma"
call .venv\Scripts\activate.bat
python main.py

echo.
echo =================================================
echo Aplikace byla ukoncena. Stisknete libovolnou klavesu...
pause > nul
