@echo off
REM ============================================================
REM Atualiza o repositorio e envia para o GitHub.
REM
REM Este arquivo precisa estar na RAIZ do repo, ou seja em:
REM   ...\trabalho_aprendizado_profundo_repo\repo\
REM
REM O que ele faz, em ordem:
REM   1. copia do projeto pro repo os arquivos que mudaram fora dele
REM      (modelo treinado, figuras, apresentacao e guia)
REM   2. mostra o que o git vai enviar
REM   3. git add, git commit e git push
REM ============================================================

cd /d "%~dp0"
title Commit e push - Aprendizado Profundo

set "PROJETO=C:\Users\lucas\Saida one drive\Documentos\Mestrado\Aprendizado Profundo\trabalho_final_recomendacao_consultorias"
set "DESTINO=%~dp0trabalho_final_recomendacao_consultorias"

where git >nul 2>&1
if errorlevel 1 (
    echo.
    echo Nao encontrei o git neste terminal. Instale o Git para Windows
    echo ou rode este arquivo pelo "Git Bash" / pelo terminal do VS Code.
    pause
    exit /b 1
)

echo.
echo [1/4] Copiando do projeto para o repo
if not exist "%PROJETO%" (
    echo      AVISO: nao achei a pasta do projeto em:
    echo      %PROJETO%
    echo      Seguindo sem copiar - o que ja esta no repo sera enviado.
) else (
    if not exist "%DESTINO%\modelos" mkdir "%DESTINO%\modelos"
    if not exist "%DESTINO%\figuras" mkdir "%DESTINO%\figuras"
    copy /Y "%PROJETO%\modelos\propensao_consultoria.keras" "%DESTINO%\modelos\" >nul
    copy /Y "%PROJETO%\modelos\propensao_artefatos.joblib" "%DESTINO%\modelos\" >nul
    copy /Y "%PROJETO%\figuras\*.png" "%DESTINO%\figuras\" >nul
    copy /Y "%PROJETO%\figuras\*.gif" "%DESTINO%\figuras\" >nul
    copy /Y "%PROJETO%\apresentacao_propensao.pptx" "%DESTINO%\" >nul
    copy /Y "%PROJETO%\guia_apresentacao.md" "%DESTINO%\" >nul
    copy /Y "%PROJETO%\trabalho_final_propensao_consultoria.ipynb" "%DESTINO%\" >nul
    echo      ok
)

echo.
echo [2/4] Branch atual e arquivos que mudaram
git branch --show-current
echo.
git status --short
echo.

echo ============================================================
echo Confira a lista acima. ENTER continua, Ctrl+C cancela.
echo ============================================================
pause >nul

echo.
echo [3/4] Registrando o commit
git add -A
git commit -m "Trabalho final: escopo binario orientado a recall, app de demonstracao e apresentacao" -m "- notebook executado com o escopo binario (contratar ou nao consultoria), recall como criterio de selecao do modelo" -m "- modelo treinado e artefatos de pre-processamento atualizados em modelos/" -m "- app Streamlit para demonstracao local em app/" -m "- apresentacao e guia de apresentacao" -m "- README com o link do Colab e os resultados do conjunto de teste" -m "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_015CtUzrPF4pnTcR4uFxgAHD"

if errorlevel 1 (
    echo.
    echo O commit nao foi criado. Se a mensagem acima diz "nothing to commit",
    echo e porque nao havia mudanca nenhuma - nesse caso esta tudo ja enviado.
    pause
    exit /b 1
)

echo.
echo [4/4] Enviando para o GitHub
git push
if errorlevel 1 (
    echo.
    echo O push falhou. Causas comuns:
    echo   - login do GitHub expirado (o git vai pedir usuario e token)
    echo   - alguem alterou o repo pelo site; nesse caso rode "git pull --rebase" e tente de novo
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Pronto. Confira em:
echo https://github.com/lucassmsantoss/aprendizado-profundo
echo ============================================================
echo.
pause
