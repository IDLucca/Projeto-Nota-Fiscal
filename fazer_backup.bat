@echo off
echo ========================================
echo    Sistema de Nota Fiscal - Backup
echo ========================================
echo.

echo Criando backup dos dados...
echo.

REM Criar pasta de backup se não existir
if not exist "backup" mkdir backup

REM Criar nome do arquivo com data e hora
set data_hora=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set data_hora=%data_hora: =0%

REM Copiar arquivo de dados
if exist "dados_sistema.json" (
    copy "dados_sistema.json" "backup\dados_sistema_%data_hora%.json"
    echo Backup criado: backup\dados_sistema_%data_hora%.json
) else (
    echo Nenhum dado encontrado para backup.
)

echo.
echo ========================================
echo    Backup concluido!
echo ========================================
echo.
echo Arquivos de backup salvos em:
echo %cd%\backup\
echo.
echo Para restaurar um backup:
echo 1. Copie o arquivo .json da pasta backup
echo 2. Cole na pasta principal com o nome "dados_sistema.json"
echo.
pause 