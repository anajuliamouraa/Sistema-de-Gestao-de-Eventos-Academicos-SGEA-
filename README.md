# SGEA - Sistema de Gestão de Eventos Acadêmicos

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema web desenvolvido em Django para gerenciamento completo de eventos acadêmicos como seminários, palestras, minicursos e semanas acadêmicas.

## 👥 Equipe de Desenvolvimento

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Ano:** 2025

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Documentação](#documentação)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

---

## 🎯 Sobre o Projeto

O **SGEA (Sistema de Gestão de Eventos Acadêmicos)** é uma aplicação web completa que facilita o gerenciamento de eventos acadêmicos em instituições de ensino. O sistema permite que organizadores criem e gerenciem eventos, estudantes e professores se inscrevam, e certificados sejam emitidos automaticamente.

### Objetivos

- Centralizar o gerenciamento de eventos acadêmicos
- Facilitar o processo de inscrição e controle de participantes
- Automatizar a emissão e verificação de certificados
- Fornecer uma interface intuitiva e moderna
- Garantir segurança e integridade dos dados

---

## ⚡ Funcionalidades

### 🔐 Sistema de Autenticação

- Cadastro de novos usuários com validação de dados
- Login/logout seguro
- Três perfis de usuário: Aluno, Professor e Organizador
- Gerenciamento de perfil pessoal

### 📅 Gerenciamento de Eventos

- **Para Organizadores:**

  - Criar novos eventos com informações detalhadas
  - Editar eventos existentes
  - Controlar vagas disponíveis
  - Visualizar lista de inscritos
  - Gerenciar status (ativo/inativo)
  - Excluir eventos

- **Para Todos os Usuários:**
  - Listar eventos disponíveis
  - Buscar eventos por título, descrição ou local
  - Filtrar por tipo de evento
  - Visualizar detalhes completos do evento
  - Ver disponibilidade de vagas em tempo real

### 📝 Sistema de Inscrições

- Inscrição rápida em eventos com vagas disponíveis
- Confirmação automática de inscrição
- Gerenciamento de vagas em tempo real
- Visualização de inscrições ativas
- Cancelamento de inscrições
- Prevenção de inscrições duplicadas

### 🎓 Emissão de Certificados

- Emissão de certificados para participantes
- Código UUID único para verificação
- Download em formato PDF profissional
- Visualização online do certificado
- Verificação pública de autenticidade
- Informações completas no certificado

### 🔍 Funcionalidades Adicionais

- Interface responsiva (mobile-friendly)
- Paginação de resultados
- Mensagens de feedback ao usuário
- Sistema de busca e filtros
- Estatísticas de eventos e inscrições
- Design moderno e intuitivo

---

## 🛠️ Tecnologias Utilizadas

### Backend

- **Python 3.8+** - Linguagem de programação
- **Django 4.2** - Framework web
- **SQLite3** - Banco de dados (desenvolvimento)
- **PostgreSQL** - Banco de dados (produção)

### Frontend

- **HTML5** - Estrutura
- **CSS3** - Estilização
- **Bootstrap 5.3** - Framework CSS
- **Bootstrap Icons** - Ícones
- **JavaScript** - Interatividade

### Bibliotecas Python

- **Pillow** - Processamento de imagens
- **ReportLab** - Geração de PDFs
- **python-decouple** - Gerenciamento de variáveis de ambiente
- **psycopg2** - Adaptador PostgreSQL

---

## 📁 Estrutura do Projeto

```
Sistema-de-Gestao-de-Eventos-Academicos-SGEA-/
│
├── sgea/                      # Configurações principais do Django
│   ├── __init__.py
│   ├── settings.py           # Configurações do projeto
│   ├── urls.py               # URLs principais
│   ├── wsgi.py               # WSGI config
│   └── asgi.py               # ASGI config
│
├── users/                     # App de usuários
│   ├── models.py             # Modelo CustomUser
│   ├── views.py              # Views de autenticação e perfil
│   ├── forms.py              # Formulários de usuário
│   ├── urls.py               # URLs do app
│   └── admin.py              # Configuração admin
│
├── events/                    # App de eventos
│   ├── models.py             # Modelos Event e Inscription
│   ├── views.py              # Views de eventos e inscrições
│   ├── forms.py              # Formulários de eventos
│   ├── urls.py               # URLs do app
│   └── admin.py              # Configuração admin
│
├── certificates/              # App de certificados
│   ├── models.py             # Modelo Certificate
│   ├── views.py              # Views de certificados
│   ├── forms.py              # Formulários de certificados
│   ├── urls.py               # URLs do app
│   ├── utils.py              # Geração de PDFs
│   └── admin.py              # Configuração admin
│
├── templates/                 # Templates HTML
│   ├── base.html             # Template base
│   ├── users/                # Templates de usuários
│   ├── events/               # Templates de eventos
│   └── certificates/         # Templates de certificados
│
├── static/                    # Arquivos estáticos
│   ├── css/                  # Arquivos CSS customizados
│   ├── js/                   # JavaScript customizado
│   └── images/               # Imagens do sistema
│
├── media/                     # Arquivos de mídia (uploads)
│   └── eventos/              # Imagens de eventos
│
├── docs/                      # Documentação
│   ├── REQUISITOS_E_CASOS_DE_USO.md
│   ├── DIAGRAMA_BANCO_DADOS.md
│   └── database_schema.sql
│
├── manage.py                  # Script de gerenciamento Django
├── requirements.txt           # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Este arquivo
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (recomendado)
- Git

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-.git
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
```

2. **Crie e ative um ambiente virtual**

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3
```

5. **Execute as migrações**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crie um superusuário**

**Opção A: Credenciais Padrão (Recomendado para Teste)**

```bash
python manage.py shell
```

Depois cole este código:

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
- **Perfil:** ORGANIZADOR

**Opção B: Criar Manualmente**

```bash
python manage.py createsuperuser
```

Siga as instruções para criar o usuário administrador.

⚠️ **Importante:** A senha padrão (12345) é apenas para desenvolvimento/demonstração. Em produção, use uma senha forte!

7. **Execute o servidor de desenvolvimento**

```bash
python manage.py runserver
```

8. **Acesse o sistema**

Abra seu navegador e acesse: `http://127.0.0.1:8000`

---

## ⚙️ Configuração

### Configurações de Banco de Dados

#### SQLite (Desenvolvimento)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Produção)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sgea_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Configurações de Mídia

As imagens dos eventos são armazenadas em `media/eventos/`. Configure o servidor web para servir esses arquivos em produção.

### Configurações de Email (Opcional)

Para notificações por email, configure em `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua_senha'
```

---

## 💻 Uso

### Perfis de Usuário

#### 1. Aluno/Professor

- Visualizar eventos disponíveis
- Buscar e filtrar eventos
- Inscrever-se em eventos
- Cancelar inscrições
- Visualizar certificados
- Fazer download de certificados em PDF

#### 2. Organizador

- Todas as funcionalidades de Aluno/Professor
- Criar novos eventos
- Editar eventos criados
- Visualizar lista de inscritos
- Emitir certificados
- Gerenciar status dos eventos

#### 3. Administrador

- Acesso completo ao Django Admin
- Gerenciar usuários, eventos, inscrições e certificados
- Visualizar estatísticas completas

### Fluxo Básico de Uso

1. **Cadastro**: Novo usuário se registra escolhendo seu perfil
2. **Login**: Usuário faz login com suas credenciais
3. **Navegação**: Usuário explora eventos disponíveis
4. **Inscrição**: Usuário se inscreve em evento de interesse
5. **Participação**: Usuário participa do evento
6. **Certificado**: Organizador emite certificado após o evento
7. **Download**: Participante baixa seu certificado em PDF
8. **Verificação**: Qualquer pessoa pode verificar autenticidade

---

## 📚 Documentação

### Documentos Disponíveis

- **[Requisitos e Casos de Uso](docs/REQUISITOS_E_CASOS_DE_USO.md)** - Requisitos funcionais, não funcionais e casos de uso detalhados
- **[Diagrama do Banco de Dados](docs/DIAGRAMA_BANCO_DADOS.md)** - Modelo lógico completo do banco de dados
- **[Script SQL](docs/database_schema.sql)** - Script de criação e população do banco

### API Django Admin

O Django Admin está disponível em `/admin/` para gerenciamento completo do sistema.

### Modelos de Dados

#### CustomUser

```python
- username (único)
- first_name, last_name
- email
- telefone
- instituicao_ensino
- perfil (ALUNO, PROFESSOR, ORGANIZADOR)
```

#### Event

```python
- titulo
- descricao
- tipo_evento (SEMINARIO, PALESTRA, MINICURSO, SEMANA_ACADEMICA)
- data_inicio, data_fim
- horario_inicio, horario_fim
- local
- vagas, vagas_disponiveis
- organizador (FK)
```

#### Inscription

```python
- evento (FK)
- usuario (FK)
- status (PENDENTE, CONFIRMADA, CANCELADA)
- data_inscricao
```

#### Certificate

```python
- inscricao (FK, OneToOne)
- codigo_verificacao (UUID)
- emitido_por (FK)
- carga_horaria
- data_emissao
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Siga o PEP 8 para código Python
- Documente novas funcionalidades
- Adicione testes quando apropriado
- Mantenha o código limpo e legível
- Atualize o README se necessário

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autores

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Ano:** 2025

---

## 📞 Contato

Para dúvidas, sugestões ou feedback sobre o projeto:

**Autores:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Email do Projeto:** ana.fmoura@gmail.com  
**GitHub:** https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

---

## 🙏 Agradecimentos

- Comunidade Django
- Bootstrap Team
- ReportLab
- Todos os contribuidores do projeto

---

## 📈 Status do Projeto

✅ **Versão 1.0 - Concluída**

### Funcionalidades Implementadas

- [x] Sistema de autenticação completo
- [x] Gerenciamento de usuários com múltiplos perfis
- [x] CRUD completo de eventos
- [x] Sistema de inscrições
- [x] Emissão de certificados em PDF
- [x] Verificação de certificados
- [x] Interface responsiva
- [x] Busca e filtros
- [x] Documentação completa

### Futuras Melhorias

- [ ] Sistema de notificações por email
- [ ] Relatórios e estatísticas avançadas
- [ ] Integração com redes sociais
- [ ] Sistema de avaliação de eventos
- [ ] QR Code nos certificados
- [ ] API REST para integração externa
- [ ] Modo escuro (dark mode)
- [ ] Suporte a múltiplos idiomas

---

## 🔧 Troubleshooting

### Problema: Erro ao instalar psycopg2

**Solução**: Instale as dependências do sistema:

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libpq-dev

# CentOS/RHEL
sudo yum install python3-devel postgresql-devel
```

### Problema: Erro de permissão em media/

**Solução**: Ajuste as permissões:

```bash
chmod -R 755 media/
```

### Problema: SECRET_KEY não configurada

**Solução**: Crie o arquivo `.env` com uma SECRET_KEY válida ou configure em settings.py

---

## 📸 Screenshots

### Tela Inicial

![Home](docs/screenshots/home.png)

### Detalhes do Evento

![Evento](docs/screenshots/evento.png)

### Certificado

![Certificado](docs/screenshots/certificado.png)

---

**Desenvolvido com ❤️ usando Django**

---

**Última atualização**: Outubro de 2025  
**Versão**: 1.0.0
