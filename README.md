# SGEA - Sistema de Gestão de Eventos Acadêmicos

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)
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
- [Novidades da Fase 2](#novidades-da-fase-2)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [API REST](#api-rest)
- [Credenciais de Teste](#credenciais-de-teste)
- [Documentação](#documentação)

---

## 🎯 Sobre o Projeto

O **SGEA (Sistema de Gestão de Eventos Acadêmicos)** é uma aplicação web completa que facilita o gerenciamento de eventos acadêmicos em instituições de ensino. O sistema permite que organizadores criem e gerenciem eventos, estudantes e professores se inscrevam, e certificados sejam emitidos automaticamente.

---

## 🆕 Novidades da Fase 2

### API REST
- Endpoints para consulta de eventos e inscrição
- Autenticação via Token
- Rate limiting (20 req/dia eventos, 50 req/dia inscrições)

### Validações Avançadas
- Máscara de telefone (XX) XXXXX-XXXX
- Datepicker e Timepicker com jQuery
- Validação de imagens no upload de banner
- Senha com requisitos de segurança (8+ chars, maiúsculas, minúsculas, números, especiais)

### Notificações por E-mail
- Email de boas-vindas com código de ativação
- Confirmação de inscrição em eventos
- Notificação de certificado disponível

### Sistema de Auditoria
- Registro de todas as ações críticas
- Tela de consulta de logs para organizadores
- Filtros por data, usuário e tipo de ação

### Controle de Acesso Aprimorado
- Confirmação de email obrigatória
- Professor responsável vinculado a eventos
- Organizadores não podem se inscrever
- Validação de data de eventos (não permite datas passadas)

### Certificados Automáticos
- Confirmação de presença dos participantes
- Geração automática de certificados após término do evento
- Command para processamento em lote

---

## ⚡ Funcionalidades

### 🔐 Sistema de Autenticação
- Cadastro com validação de senha forte
- Login com email ou username
- Confirmação de email obrigatória
- Três perfis: Aluno, Professor, Organizador

### 📅 Gerenciamento de Eventos
- CRUD completo de eventos (organizadores)
- Professor responsável obrigatório
- Upload de banner com validação
- Datepicker e Timepicker visuais
- Validação de datas (não permite eventos passados)

### 📝 Sistema de Inscrições
- Inscrição com confirmação por email
- Controle de vagas em tempo real
- Organizadores impedidos de se inscrever
- Cancelamento de inscrições

### 🎓 Certificados
- Confirmação de presença pelo organizador
- Emissão automática após evento
- Download em PDF
- Verificação de autenticidade

### 🔍 API REST
- Autenticação por Token
- Endpoints de eventos e inscrições
- Rate limiting configurável
- Documentação integrada

### 📊 Auditoria
- Log de todas as ações críticas
- Consulta por data/usuário/ação
- Acesso exclusivo para organizadores

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Django 4.2**
- **Django REST Framework 3.14**
- **SQLite3** (desenvolvimento)

### Frontend
- **Bootstrap 5.3**
- **jQuery + jQuery UI**
- **Bootstrap Icons**
- **Google Fonts (Poppins)**

### Bibliotecas
- **Pillow** - Processamento de imagens
- **ReportLab** - Geração de PDFs
- **jQuery Mask** - Máscaras de input
- **jQuery Timepicker** - Seletor de hora

---

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-.git
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações
python manage.py migrate

# 5. Carregue os dados de teste
python manage.py seed_data

# 6. Inicie o servidor
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

---

## 🔑 Credenciais de Teste

| Perfil | Email | Senha |
|--------|-------|-------|
| **Organizador** | organizador@sgea.com | Admin@123 |
| **Professor** | professor@sgea.com | Professor@123 |
| **Aluno** | aluno@sgea.com | Aluno@123 |

---

## 📡 API REST

### Autenticação

```bash
# Obter token
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "aluno", "password": "Aluno@123"}'
```

### Endpoints

| Método | Endpoint | Descrição | Limite |
|--------|----------|-----------|--------|
| POST | `/api/auth/token/` | Obter token | - |
| GET | `/api/events/` | Listar eventos | 20/dia |
| GET | `/api/events/<id>/` | Detalhes do evento | 20/dia |
| POST | `/api/inscriptions/` | Criar inscrição | 50/dia |
| GET | `/api/inscriptions/me/` | Minhas inscrições | 50/dia |
| DELETE | `/api/inscriptions/<id>/` | Cancelar inscrição | 50/dia |

### Exemplo de Uso

```bash
# Listar eventos
curl http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Token SEU_TOKEN"

# Inscrever-se em evento
curl -X POST http://127.0.0.1:8000/api/inscriptions/ \
  -H "Authorization: Token SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"evento_id": 1}'
```

---

## 📚 Documentação

- **[Manual de Instalação](docs/MANUAL_INSTALACAO.md)**
- **[Guia de Uso](docs/GUIA_USO.md)**
- **[Guia de Testes](docs/GUIA_TESTES.md)**
- **[Requisitos e Casos de Uso](docs/REQUISITOS_E_CASOS_DE_USO.md)**
- **[Diagrama do Banco](docs/DIAGRAMA_BANCO_DADOS.md)**

---

## 🧪 Comandos Úteis

```bash
# Carregar dados de teste
python manage.py seed_data

# Gerar certificados automaticamente
python manage.py generate_certificates

# Verificar sistema
python manage.py check
```

---

## 📈 Status do Projeto

### ✅ Fase 1 - Concluída
- Sistema de autenticação
- CRUD de eventos
- Sistema de inscrições
- Emissão de certificados
- Interface responsiva

### ✅ Fase 2 - Concluída
- [x] API REST com autenticação
- [x] Rate limiting
- [x] Validações avançadas
- [x] Máscaras de input
- [x] Datepicker/Timepicker
- [x] Sistema de email
- [x] Confirmação de conta
- [x] Auditoria completa
- [x] Certificados automáticos
- [x] Professor responsável
- [x] Identidade visual aprimorada
- [x] Acessibilidade (WCAG)
- [x] Documentação de testes

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

**Email:** ana.fmoura@gmail.com  
**GitHub:** https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

---

**Desenvolvido com ❤️ usando Django**

**Última atualização:** Dezembro de 2025  
**Versão:** 2.0.0
