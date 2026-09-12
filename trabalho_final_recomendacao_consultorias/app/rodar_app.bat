@echo off
REM ============================================================
REM Sobe o app de demonstracao do modelo no localhost.
REM De dois cliques neste arquivo, ou rode pelo cmd:
REM     rodar_app.bat
REM
REM Na primeira vez ele instala as dependencias (demora,
REM o tensorflow tem quase 1 GB). Depois disso, so sobe o app.
REM ============================================================

cd /d "%~dp0"
title App - Propensao a contratar consultoria

set "PY_EXE="
set "PY_ARGS="

REM Procura um Python que realmente funcione. O teste e importar o sys:
REM o atalho da Microsoft Store aparece no PATH mas falha aqui, e entao e descartado.
echo Procurando o Python...

python -c "import sys" >nul 2>&1 && (set "PY_EXE=python")

if not defined PY_EXE (
    py -3 -c "import sys" >nul 2>&1 && (set "PY_EXE=py" & set "PY_ARGS=-3")
)

if not defined PY_EXE call :tentar "%USERPROFILE%\anaconda3\python.exe"
if not defined PY_EXE call :tentar "%USERPROFILE%\miniconda3\python.exe"
if not defined PY_EXE call :tentar "%LOCALAPPDATA%\anaconda3\python.exe"
if not defined PY_EXE call :tentar "C:\ProgramData\anaconda3\python.exe"

REM qualquer instalacao padrao do Python na pasta do usuario
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if not defined PY_EXE call :tentar "%%~D\python.exe"
)

if not defined PY_EXE (
    echo.
    echo Nao encontrei um Python que funcione. Procurei em:
    echo   - o comando "python" do PATH
    echo   - o lancador "py -3"
    echo   - %USERPROFILE%\anaconda3\python.exe
    echo   - %USERPROFILE%\miniconda3\python.exe
    echo   - %LOCALAPPDATA%\anaconda3\python.exe
    echo   - C:\ProgramData\anaconda3\python.exe
    echo   - %LOCALAPPDATA%\Programs\Python\Python3*\python.exe
    echo.
    echo Abra o "Anaconda Prompt" pelo menu Iniciar e rode estas duas linhas:
    echo.
    echo     cd /d "%~dp0"
    echo     rodar_app.bat
    echo.
    pause
    exit /b 1
)

echo.
echo Usando: %PY_EXE% %PY_ARGS%
"%PY_EXE%" %PY_ARGS% --version
echo.

REM streamlit instalado? se sim, pula a instalacao e vai direto pro app
"%PY_EXE%" %PY_ARGS% -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Instalando as dependencias. Isso acontece so na primeira vez.
    echo.
    "%PY_EXE%" %PY_ARGS% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo A instalacao falhou. Leia a mensagem acima e tente de novo.
        pause
        exit /b 1
    )
) else (
    echo Dependencias ja instaladas.
)

echo.
echo ============================================================
echo Subindo o app. O navegador abre em http://localhost:8501
echo Para encerrar, feche esta janela ou pressione Ctrl+C.
echo ============================================================
echo.

"%PY_EXE%" %PY_ARGS% -m streamlit run app.py

pause
exit /b 0


:tentar
REM testa um caminho de python; se funcionar, guarda em PY_EXE
if not exist "%~1" goto :eof
"%~1" -c "import sys" >nul 2>&1
if errorlevel 1 goto :eof
set "PY_EXE=%~1"
goto :eof
