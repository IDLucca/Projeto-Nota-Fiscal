@echo off
title Instalação Completa - Sistema de Nota Fiscal
color 0A

echo.
echo ========================================
echo    SISTEMA DE NOTA FISCAL
echo    Instalação Completa
echo    Padaria Quero Mais
echo ========================================
echo.
echo Iniciando instalação completa do sistema...
echo.

REM Verificar se o Python está instalado
echo [1/8] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERRO: Python não está instalado!
    echo.
    echo 📋 Para instalar o Python:
    echo 1. Acesse: https://www.python.org/downloads/
    echo 2. Baixe a versão mais recente (3.7 ou superior)
    echo 3. Durante a instalação, marque "Add Python to PATH"
    echo 4. Execute este arquivo novamente
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version
echo.

REM Verificar se o pip está funcionando
echo [2/8] Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: pip não está funcionando!
    echo.
    echo 📋 Solução:
    echo 1. Reinstale o Python marcando "Add Python to PATH"
    echo 2. Execute este arquivo novamente
    echo.
    pause
    exit /b 1
)

echo ✅ pip funcionando!
echo.

REM Atualizar pip
echo [3/8] Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar dependências básicas
echo [4/8] Instalando dependências básicas...
echo.
echo 📦 Instalando ReportLab (geração de PDF)...
pip install reportlab==4.0.4
if errorlevel 1 (
    echo ❌ Erro ao instalar ReportLab
    pause
    exit /b 1
)

echo 📦 Instalando Pillow (processamento de imagens)...
pip install Pillow==10.0.1
if errorlevel 1 (
    echo ❌ Erro ao instalar Pillow
    pause
    exit /b 1
)

echo 📦 Instalando python-dateutil (manipulação de datas)...
pip install python-dateutil==2.8.2
if errorlevel 1 (
    echo ❌ Erro ao instalar python-dateutil
    pause
    exit /b 1
)

echo 📦 Instalando pywin32 (impressão Windows)...
pip install pywin32==311
if errorlevel 1 (
    echo ❌ Erro ao instalar pywin32
    pause
    exit /b 1
)

echo.

REM Instalar dependências para NF-e
echo [5/8] Instalando dependências para NF-e...
echo.
echo 📦 Instalando qrcode (geração de QR Code)...
pip install qrcode==7.4.2
if errorlevel 1 (
    echo ❌ Erro ao instalar qrcode
    pause
    exit /b 1
)

echo 📦 Instalando cryptography (certificados digitais)...
pip install cryptography==41.0.7
if errorlevel 1 (
    echo ❌ Erro ao instalar cryptography
    pause
    exit /b 1
)

echo.

REM Criar pastas necessárias
echo [6/8] Criando pastas do sistema...
if not exist "pdfs" mkdir pdfs
if not exist "xmls" mkdir xmls
if not exist "certificados" mkdir certificados
echo ✅ Pastas criadas com sucesso!
echo.

REM Verificar se os arquivos principais existem
echo [7/8] Verificando arquivos do sistema...
if not exist "sistema_nota_fiscal.pyw" (
    echo ❌ ERRO: Arquivo sistema_nota_fiscal.pyw não encontrado!
    echo.
    echo 📋 Certifique-se de que todos os arquivos do sistema estão na mesma pasta.
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ ERRO: Arquivo requirements.txt não encontrado!
    pause
    exit /b 1
)

echo ✅ Arquivos do sistema encontrados!
echo.

REM Testar importações
echo [8/8] Testando instalação...
echo.
python -c "import reportlab, qrcode, cryptography, win32print; print('✅ Todas as dependências funcionando!')" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Algumas dependências não estão funcionando!
    echo.
    echo 📋 Tente executar novamente ou reinicie o computador.
    echo.
    pause
    exit /b 1
)

echo ✅ Todas as dependências funcionando!
echo.

REM Criar arquivo de configuração inicial
echo [EXTRA] Configurando sistema...
if not exist "dados_sistema.json" (
    echo { > dados_sistema.json
    echo   "dados_empresa": { >> dados_sistema.json
    echo     "nome": "", >> dados_sistema.json
    echo     "cnpj": "", >> dados_sistema.json
    echo     "endereco": "", >> dados_sistema.json
    echo     "cidade": "", >> dados_sistema.json
    echo     "cep": "", >> dados_sistema.json
    echo     "telefone": "" >> dados_sistema.json
    echo   }, >> dados_sistema.json
    echo   "produtos": [], >> dados_sistema.json
    echo   "notas_fiscais": [] >> dados_sistema.json
    echo } >> dados_sistema.json
    echo ✅ Arquivo de configuração criado!
)

echo.
echo ========================================
echo    ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================
echo.
echo 🎉 O sistema está pronto para uso!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo 1. Execute SISTEMA.bat para iniciar o sistema
echo 2. Faça login com: admin1 / admin123
echo 3. Configure os dados da empresa
echo 4. Cadastre produtos
echo 5. Gere notas fiscais
echo.
echo 🔧 FUNCIONALIDADES INSTALADAS:
echo ✅ Geração de PDF profissional
echo ✅ Sistema NF-e XML completo
echo ✅ QR Code para NFC-e
echo ✅ Certificado digital (preparado)
echo ✅ Impressão automática
echo ✅ Interface moderna
echo.
echo 📁 PASTAS CRIADAS:
echo 📂 pdfs/ - Notas fiscais em PDF
echo 📂 xmls/ - Arquivos XML da NF-e
echo 📂 certificados/ - Certificados digitais
echo.
echo 🚀 Para executar o sistema:
echo Clique duas vezes em SISTEMA.bat
echo.
echo ========================================
echo.
pause 