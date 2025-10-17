# Manual de Instalação - SGEA

## Guia Completo de Instalação e Configuração

---

## 👥 Equipe de Desenvolvimento

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Ano:** 2025

---

## 1. Requisitos do Sistema

### Hardware Mínimo

- Processador: 2 GHz ou superior
- RAM: 2 GB mínimo (4 GB recomendado)
- Espaço em Disco: 500 MB livre

### Software

- **Python**: 3.8, 3.9, 3.10 ou 3.11
- **pip**: Gerenciador de pacotes Python
- **Git**: Para clonar o repositório
- **Navegador Web**: Chrome, Firefox, Safari ou Edge (versões atuais)

### Sistemas Operacionais Suportados

- Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+)
- macOS 10.15+
- Windows 10/11

---

## 2. Instalação no Linux (Ubuntu/Debian)

### 2.1 Atualizar o Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 2.2 Instalar Dependências

```bash
# Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Git
sudo apt install git -y

# Dependências para PostgreSQL (opcional)
sudo apt install libpq-dev python3-dev -y

# Dependências para Pillow
sudo apt install libjpeg-dev zlib1g-dev -y
```

### 2.3 Clonar o Repositório

```bash
cd ~
git clone https://github.com/seu-usuario/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-.git
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
```

### 2.4 Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.5 Instalar Dependências Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.6 Configurar Variáveis de Ambiente

```bash
cp .env.example .env
nano .env
```

Edite o arquivo com suas configurações:

```env
SECRET_KEY=cole-aqui-uma-chave-secreta-aleatoria
DEBUG=True
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

Para gerar uma SECRET_KEY segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2.7 Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2.8 Criar Superusuário

**Opção A: Usar Credenciais Padrão (Recomendado para Teste)**

```bash
python manage.py shell
```

Cole este código no shell Python:

```python
from users.models import CustomUser
CustomUser.objects.filter(username='admin').delete()
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@sgea.edu.br',
    password='12345',
    first_name='Administrador',
    last_name='Sistema',
    perfil='ORGANIZADOR',
    instituicao_ensino='SGEA'
)
print('✅ Superusuário admin criado!')
exit()
```

**Credenciais de Acesso:**

- **Username:** admin
- **Password:** 12345

**Opção B: Criar Manualmente**

```bash
python manage.py createsuperuser
```

Preencha as informações solicitadas:

- Username: admin (ou outro de sua escolha)
- Email: seu_email@exemplo.com
- Password: (senha segura)

⚠️ **Nota:** A senha padrão (12345) é apenas para desenvolvimento/demonstração!

### 2.9 Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 2.10 Iniciar o Servidor

```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

---

## 3. Instalação no Windows

### 3.1 Instalar Python

1. Baixe o Python em: https://www.python.org/downloads/
2. Execute o instalador
3. ✅ Marque "Add Python to PATH"
4. Clique em "Install Now"

### 3.2 Instalar Git

1. Baixe em: https://git-scm.com/download/win
2. Execute o instalador com configurações padrão

### 3.3 Abrir PowerShell ou CMD

```cmd
# Verificar instalação
python --version
pip --version
git --version
```

### 3.4 Clonar o Repositório

```cmd
cd C:\Users\SeuUsuario\Documents
git clone https://github.com/seu-usuario/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-.git
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
```

### 3.5 Criar Ambiente Virtual

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3.6 Instalar Dependências

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.7 Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```cmd
copy .env.example .env
notepad .env
```

Configure conforme necessário.

### 3.8 Executar Migrações

```cmd
python manage.py makemigrations
python manage.py migrate
```

### 3.9 Criar Superusuário

**Opção A: Usar Credenciais Padrão**

```cmd
python manage.py shell
```

Cole este código:

```python
from users.models import CustomUser
CustomUser.objects.filter(username='admin').delete()
admin = CustomUser.objects.create_superuser(username='admin', email='admin@sgea.edu.br', password='12345', first_name='Administrador', last_name='Sistema', perfil='ORGANIZADOR', instituicao_ensino='SGEA')
print('✅ Admin criado! Username: admin, Password: 12345')
exit()
```

**Opção B: Criar Manualmente**

```cmd
python manage.py createsuperuser
```

### 3.10 Iniciar Servidor

```cmd
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

---

## 4. Instalação no macOS

### 4.1 Instalar Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 4.2 Instalar Python e Git

```bash
brew install python3 git
```

### 4.3 Seguir Passos do Linux

Os passos 2.3 a 2.10 são idênticos no macOS.

---

## 5. Configuração com PostgreSQL (Produção)

### 5.1 Instalar PostgreSQL

**Ubuntu/Debian:**

```bash
sudo apt install postgresql postgresql-contrib -y
```

**macOS:**

```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Baixe em: https://www.postgresql.org/download/windows/

### 5.2 Criar Banco de Dados

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE sgea_db;
CREATE USER sgea_user WITH PASSWORD 'senha_segura';
ALTER ROLE sgea_user SET client_encoding TO 'utf8';
ALTER ROLE sgea_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sgea_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE sgea_db TO sgea_user;
\q
```

### 5.3 Configurar Django

Edite `.env`:

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=sgea_db
DATABASE_USER=sgea_user
DATABASE_PASSWORD=senha_segura
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Atualize `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
```

### 5.4 Executar Migrações

```bash
python manage.py migrate
```

---

## 6. Configuração para Produção

### 6.1 Configurações de Segurança

Em `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 6.2 Configurar Gunicorn

```bash
pip install gunicorn
gunicorn sgea.wsgi:application --bind 0.0.0.0:8000
```

### 6.3 Configurar Nginx

Crie `/etc/nginx/sites-available/sgea`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location /static/ {
        alias /caminho/para/sgea/staticfiles/;
    }

    location /media/ {
        alias /caminho/para/sgea/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Ativar site:

```bash
sudo ln -s /etc/nginx/sites-available/sgea /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6.4 Configurar Systemd Service

Crie `/etc/systemd/system/sgea.service`:

```ini
[Unit]
Description=SGEA Django Application
After=network.target

[Service]
User=seu-usuario
Group=www-data
WorkingDirectory=/caminho/para/sgea
Environment="PATH=/caminho/para/sgea/venv/bin"
ExecStart=/caminho/para/sgea/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 sgea.wsgi:application

[Install]
WantedBy=multi-user.target
```

Ativar serviço:

```bash
sudo systemctl start sgea
sudo systemctl enable sgea
sudo systemctl status sgea
```

---

## 7. Popular Banco de Dados (Dados de Teste)

### 7.1 Criar Usuários de Teste

```bash
python manage.py shell
```

```python
from users.models import CustomUser

# Criar organizador
org = CustomUser.objects.create_user(
    username='organizador1',
    password='senha123',
    first_name='Maria',
    last_name='Silva',
    email='maria@exemplo.com',
    perfil='ORGANIZADOR',
    instituicao_ensino='Universidade Federal'
)

# Criar aluno
aluno = CustomUser.objects.create_user(
    username='aluno1',
    password='senha123',
    first_name='João',
    last_name='Santos',
    email='joao@exemplo.com',
    perfil='ALUNO',
    instituicao_ensino='Universidade Federal'
)

exit()
```

### 7.2 Criar Eventos de Teste

Acesse o Django Admin (`/admin/`) e crie alguns eventos manualmente, ou use o shell:

```python
from events.models import Event
from users.models import CustomUser
from datetime import date, time

org = CustomUser.objects.get(username='organizador1')

Event.objects.create(
    titulo='Seminário de Python',
    descricao='Evento sobre Python e Django',
    tipo_evento='SEMINARIO',
    data_inicio=date(2024, 12, 1),
    data_fim=date(2024, 12, 3),
    horario_inicio=time(9, 0),
    horario_fim=time(18, 0),
    local='Auditório Central',
    vagas=50,
    organizador=org,
    ativo=True
)
```

---

## 8. Solução de Problemas

### Erro: "No module named 'django'"

**Solução:** Ative o ambiente virtual

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Erro: "Unable to open database file"

**Solução:** Verifique permissões

```bash
chmod 644 db.sqlite3
```

### Erro: "Port already in use"

**Solução:** Use outra porta

```bash
python manage.py runserver 8080
```

### Erro: "CSRF verification failed"

**Solução:** Limpe cookies do navegador ou desabilite CSRF temporariamente (apenas desenvolvimento)

### Erro ao instalar Pillow

**Solução:** Instale dependências

```bash
# Ubuntu
sudo apt install libjpeg-dev zlib1g-dev

# macOS
brew install libjpeg zlib
```

---

## 9. Verificação da Instalação

### 9.1 Checklist

- [ ] Python instalado (versão 3.8+)
- [ ] Repositório clonado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Servidor iniciado com sucesso
- [ ] Página inicial carrega sem erros
- [ ] Login funcional
- [ ] Django Admin acessível

### 9.2 Comandos de Teste

```bash
# Verificar configuração
python manage.py check

# Executar testes (se disponíveis)
python manage.py test

# Verificar migrações pendentes
python manage.py showmigrations
```

---

## 10. Próximos Passos

Após instalação bem-sucedida:

1. Acesse o Django Admin em `/admin/`
2. Crie alguns usuários de teste
3. Crie eventos de exemplo
4. Teste o fluxo de inscrição
5. Teste a emissão de certificados
6. Verifique a geração de PDFs

---

## 11. Suporte

Para problemas durante a instalação:

- **Documentação**: Consulte o README.md
- **Issues**: Abra uma issue no GitHub
- **Email**: ana.fmoura@gmail.com
- **GitHub**: https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

---

**Boa sorte com sua instalação!** 🚀
