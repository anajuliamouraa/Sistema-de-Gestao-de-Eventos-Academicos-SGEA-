@echo off
REM ==============================================================================
REM SGEA - Script de Configuracao Rapida (Windows)
REM Sistema de Gestao de Eventos Academicos
REM ==============================================================================

echo ======================================
echo SGEA - Configuracao Rapida
echo ======================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python 3 nao encontrado!
    echo Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python encontrado: %PYTHON_VERSION%
echo.

REM Criar ambiente virtual
echo [*] Criando ambiente virtual...
python -m venv venv

if errorlevel 1 (
    echo [X] Erro ao criar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual criado
echo.

REM Ativar ambiente virtual
echo [*] Ativando ambiente virtual...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [X] Erro ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado
echo.

REM Atualizar pip
echo [*] Atualizando pip...
python -m pip install --upgrade pip -q

echo [OK] pip atualizado
echo.

REM Instalar dependencias
echo [*] Instalando dependencias...
pip install -r requirements.txt -q

if errorlevel 1 (
    echo [X] Erro ao instalar dependencias!
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.

REM Verificar se .env existe
if not exist .env (
    echo [!] Arquivo .env nao encontrado
    echo [*] Criando arquivo .env a partir do exemplo...
    
    REM Gerar SECRET_KEY
    for /f "tokens=*" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set SECRET_KEY=%%i
    
    (
        echo # Django Settings
        echo SECRET_KEY=%SECRET_KEY%
        echo DEBUG=True
        echo.
        echo # Database Settings
        echo DATABASE_ENGINE=django.db.backends.sqlite3
        echo DATABASE_NAME=db.sqlite3
    ) > .env
    
    echo [OK] Arquivo .env criado
) else (
    echo [OK] Arquivo .env ja existe
)

echo.

REM Executar migracoes
echo [*] Executando migracoes do banco de dados...
python manage.py makemigrations

if errorlevel 1 (
    echo [X] Erro ao criar migracoes!
    pause
    exit /b 1
)

python manage.py migrate

if errorlevel 1 (
    echo [X] Erro ao executar migracoes!
    pause
    exit /b 1
)

echo [OK] Migracoes concluidas
echo.

REM Criar superusuario
echo [*] Criando superusuario...
echo.
echo Voce precisara definir um nome de usuario e senha para o administrador.
echo.

python manage.py createsuperuser

if errorlevel 1 (
    echo [!] Criacao de superusuario cancelada ou com erro
) else (
    echo [OK] Superusuario criado
)

echo.

REM Coletar arquivos estaticos
echo [*] Coletando arquivos estaticos...
python manage.py collectstatic --noinput

if errorlevel 1 (
    echo [!] Erro ao coletar arquivos estaticos (nao critico)
) else (
    echo [OK] Arquivos estaticos coletados
)

echo.
echo ======================================
echo [OK] CONFIGURACAO CONCLUIDA COM SUCESSO!
echo ======================================
echo.
echo Para iniciar o servidor, execute:
echo.
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Depois acesse: http://127.0.0.1:8000
echo.
echo Para acessar o admin: http://127.0.0.1:8000/admin
echo.
echo ======================================
pause

