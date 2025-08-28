@echo off
title Sistema de Nota Fiscal
color 0A

echo.
echo ========================================
echo    SISTEMA DE NOTA FISCAL
echo    Padaria Quero Mais
echo ========================================
echo.
echo Iniciando o sistema...
echo.

REM Verificar se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao esta instalado!
    echo.
    echo Por favor, instale o Python primeiro:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verificar se o arquivo principal existe
if not exist "sistema_nota_fiscal.pyw" (
    echo ERRO: Arquivo sistema_nota_fiscal.pyw nao encontrado!
    echo.
    pause
    exit /b 1
)

REM Verificar se as dependências estão instaladas
echo Verificando dependencias...
python -c "import reportlab, qrcode, cryptography" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Instalando dependencias automaticamente...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao instalar dependencias!
        echo Execute: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Sistema iniciado com sucesso!
echo O sistema abrira em uma nova janela.
echo.

REM Executar o sistema sem mostrar CMD
start /min pythonw sistema_nota_fiscal.pyw

REM Aguardar um pouco para o sistema carregar
timeout /t 2 /nobreak >nul

REM Verificar se o processo está rodando
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Sistema executando com sucesso!
    echo.
    echo Para fechar o sistema, feche a janela do programa.
    echo.
) else (
    echo.
    echo ERRO: Sistema nao iniciou corretamente!
    echo.
    pause
)

REM Fechar este CMD automaticamente após 3 segundos
timeout /t 3 /nobreak >nul
exit 