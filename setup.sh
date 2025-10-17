#!/bin/bash

# ==============================================================================
# SGEA - Script de Configuração Rápida
# Sistema de Gestão de Eventos Acadêmicos
# ==============================================================================

echo "======================================"
echo "SGEA - Configuração Rápida"
echo "======================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Erro ao criar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual criado"
echo ""

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Erro ao ativar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual ativado"
echo ""

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip -q

echo "✅ pip atualizado"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências!"
    exit 1
fi

echo "✅ Dependências instaladas"
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado"
    echo "📝 Criando arquivo .env a partir do exemplo..."
    
    # Gerar SECRET_KEY
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    
    cat > .env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=True

# Database Settings
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
EOF
    
    echo "✅ Arquivo .env criado"
else
    echo "✅ Arquivo .env já existe"
fi

echo ""

# Executar migrações
echo "🔄 Executando migrações do banco de dados..."
python manage.py makemigrations

if [ $? -ne 0 ]; then
    echo "❌ Erro ao criar migrações!"
    exit 1
fi

python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Erro ao executar migrações!"
    exit 1
fi

echo "✅ Migrações concluídas"
echo ""

# Criar superusuário
echo "👤 Criando superusuário..."
echo ""
echo "Você precisará definir um nome de usuário e senha para o administrador."
echo ""

python manage.py createsuperuser

if [ $? -ne 0 ]; then
    echo "⚠️  Criação de superusuário cancelada ou com erro"
else
    echo "✅ Superusuário criado"
fi

echo ""

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

if [ $? -ne 0 ]; then
    echo "⚠️  Erro ao coletar arquivos estáticos (não crítico)"
else
    echo "✅ Arquivos estáticos coletados"
fi

echo ""
echo "======================================"
echo "✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
echo "======================================"
echo ""
echo "Para iniciar o servidor, execute:"
echo ""
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Depois acesse: http://127.0.0.1:8000"
echo ""
echo "Para acessar o admin: http://127.0.0.1:8000/admin"
echo ""
echo "======================================"

