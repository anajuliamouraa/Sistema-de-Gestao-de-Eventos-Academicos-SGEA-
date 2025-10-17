# SGEA - Projeto Completo

## Sistema de Gestão de Eventos Acadêmicos

---

## 👥 Equipe de Desenvolvimento

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Curso:** Ciência da Computação  
**Disciplina:** Programação para Web  
**Professor(a):** Felippe Pires Ferreira  
**Ano:** 2025

---

## 📋 Resumo do Projeto

Este documento resume todos os componentes desenvolvidos para o **Sistema de Gestão de Eventos Acadêmicos (SGEA)**, um projeto acadêmico completo utilizando Django.

---

## ✅ Entregáveis Concluídos

### 1. Estrutura do Projeto Django ✓

#### Apps Criados:

- **users** - Gerenciamento de usuários com perfis customizados
- **events** - Gerenciamento de eventos e inscrições
- **certificates** - Emissão e verificação de certificados

#### Configurações:

- ✅ `settings.py` configurado com apps, banco de dados, internacionalização (pt-BR)
- ✅ URLs principais e de cada app configuradas
- ✅ Templates base responsivo com Bootstrap 5
- ✅ Arquivos estáticos organizados (CSS e JS)

### 2. Modelos de Dados (Backend) ✓

#### CustomUser (users/models.py)

```python
- username, password (herdados de AbstractUser)
- first_name, last_name, email
- telefone, instituicao_ensino
- perfil (ALUNO, PROFESSOR, ORGANIZADOR)
- data_cadastro
```

#### Event (events/models.py)

```python
- titulo, descricao, tipo_evento
- data_inicio, data_fim
- horario_inicio, horario_fim
- local, vagas, vagas_disponiveis
- organizador (FK → CustomUser)
- imagem, ativo
- data_criacao, data_atualizacao
```

#### Inscription (events/models.py)

```python
- evento (FK → Event)
- usuario (FK → CustomUser)
- status (PENDENTE, CONFIRMADA, CANCELADA)
- data_inscricao, observacoes
- UNIQUE(evento, usuario)
```

#### Certificate (certificates/models.py)

```python
- inscricao (OneToOne → Inscription)
- codigo_verificacao (UUID único)
- emitido_por (FK → CustomUser)
- carga_horaria
- data_emissao, observacoes
```

### 3. Funcionalidades Implementadas ✓

#### Autenticação e Usuários

- ✅ Cadastro de usuários com validação
- ✅ Login/Logout seguro
- ✅ Gerenciamento de perfil
- ✅ Três perfis: Aluno, Professor, Organizador
- ✅ Validação de instituição para alunos/professores

#### Gerenciamento de Eventos

- ✅ CRUD completo de eventos (Create, Read, Update, Delete)
- ✅ Listagem com busca e filtros
- ✅ Paginação (9 eventos por página)
- ✅ Controle de vagas em tempo real
- ✅ Upload de imagens
- ✅ Ativar/desativar eventos

#### Sistema de Inscrições

- ✅ Inscrição em eventos
- ✅ Cancelamento de inscrições
- ✅ Prevenção de inscrições duplicadas
- ✅ Verificação de vagas disponíveis
- ✅ Lista de inscrições do usuário
- ✅ Lista de inscritos por evento (organizador)

#### Certificados

- ✅ Emissão de certificados por organizadores
- ✅ Geração de PDF profissional com ReportLab
- ✅ Código UUID único para verificação
- ✅ Visualização online de certificados
- ✅ Download em PDF
- ✅ Verificação pública de autenticidade

### 4. Interface (Frontend) ✓

#### Templates Criados:

**Base:**

- ✅ `base.html` - Template base com navbar responsivo e footer

**Users:**

- ✅ `login.html` - Página de login
- ✅ `register.html` - Formulário de cadastro
- ✅ `profile.html` - Visualização e edição de perfil

**Events:**

- ✅ `home.html` - Listagem de eventos com busca e filtros
- ✅ `event_detail.html` - Detalhes completos do evento
- ✅ `event_form.html` - Criar/editar evento
- ✅ `event_confirm_delete.html` - Confirmação de exclusão
- ✅ `my_events.html` - Eventos do organizador
- ✅ `my_inscriptions.html` - Inscrições do usuário
- ✅ `inscription_form.html` - Formulário de inscrição
- ✅ `inscription_confirm_cancel.html` - Cancelar inscrição
- ✅ `event_inscriptions.html` - Lista de inscritos

**Certificates:**

- ✅ `issue_certificate.html` - Emitir certificado
- ✅ `my_certificates.html` - Certificados do usuário
- ✅ `view_certificate.html` - Visualizar certificado
- ✅ `verify_certificate.html` - Verificar autenticidade

#### Design:

- ✅ Interface moderna e responsiva
- ✅ Bootstrap 5.3 integrado
- ✅ Bootstrap Icons
- ✅ Cores personalizadas (azul, dourado)
- ✅ Animações e transições suaves
- ✅ Mensagens de feedback ao usuário
- ✅ Mobile-friendly

### 5. Documentação ✓

#### Documentos Criados:

**README.md** - Documentação principal

- Descrição do projeto
- Funcionalidades
- Tecnologias utilizadas
- Estrutura do projeto
- Guia de instalação
- Guia de uso
- Contribuição e licença

**docs/REQUISITOS_E_CASOS_DE_USO.md** - Análise completa

- 10 Requisitos Funcionais detalhados (RF01-RF10)
- Requisitos Não Funcionais (RNF01-RNF06)
- 6 Casos de Uso completos (CU01-CU06)
- Fluxos principais e alternativos
- Regras de negócio (RN01-RN53)
- Diagrama de casos de uso
- Matriz de rastreabilidade
- Glossário

**docs/DIAGRAMA_BANCO_DADOS.md** - Modelo de dados

- Descrição detalhada de todas as entidades
- Diagrama Entidade-Relacionamento (MER)
- Cardinalidades e relacionamentos
- Regras de integridade
- Índices para otimização
- Triggers e regras de negócio
- Normalização (3FN)
- Estimativa de volume

**docs/database_schema.sql** - Script SQL

- Script completo de criação das tabelas
- Constraints e índices
- Dados de exemplo (população inicial)
- Consultas úteis comentadas
- Compatível com SQLite3 e PostgreSQL

**docs/MANUAL_INSTALACAO.md** - Guia de instalação

- Requisitos do sistema
- Instalação no Linux (passo a passo)
- Instalação no Windows (passo a passo)
- Instalação no macOS
- Configuração com PostgreSQL
- Deploy em produção (Gunicorn, Nginx)
- Solução de problemas
- Checklist de verificação

**docs/GUIA_USO.md** - Manual do usuário

- Primeiro acesso
- Navegação pelo sistema
- Funcionalidades por perfil
- Passo a passo de cada funcionalidade
- Dicas e boas práticas
- FAQ (Perguntas Frequentes)
- Suporte e contato

### 6. Scripts de Automação ✓

- ✅ `setup.sh` - Script de configuração automática (Linux/Mac)
- ✅ `setup.bat` - Script de configuração automática (Windows)
- ✅ Ambos instalam dependências, criam banco, e configuram o projeto

### 7. Arquivos de Configuração ✓

- ✅ `requirements.txt` - Dependências Python
- ✅ `.gitignore` - Arquivos ignorados pelo Git
- ✅ `.env.example` - Exemplo de variáveis de ambiente
- ✅ `LICENSE` - Licença MIT

---

## 📊 Estatísticas do Projeto

### Linhas de Código (aproximado)

| Componente          | Linhas      | Arquivos |
| ------------------- | ----------- | -------- |
| Models (Python)     | ~500        | 3        |
| Views (Python)      | ~800        | 3        |
| Forms (Python)      | ~300        | 3        |
| Templates (HTML)    | ~2000       | 16       |
| Admin (Python)      | ~200        | 3        |
| URLs (Python)       | ~100        | 4        |
| Utils (Python)      | ~200        | 1        |
| CSS/JS              | ~200        | 2        |
| Documentação (MD)   | ~6000       | 6        |
| Scripts (Shell/Bat) | ~300        | 2        |
| **TOTAL**           | **~10.600** | **43**   |

### Estrutura de Arquivos

```
SGEA/
├── sgea/                  # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── users/                 # App usuários
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── events/                # App eventos
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── certificates/          # App certificados
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── utils.py
│   └── admin.py
├── templates/             # Templates HTML
│   ├── base.html
│   ├── users/
│   ├── events/
│   └── certificates/
├── static/                # Arquivos estáticos
│   ├── css/
│   └── js/
├── docs/                  # Documentação
│   ├── REQUISITOS_E_CASOS_DE_USO.md
│   ├── DIAGRAMA_BANCO_DADOS.md
│   ├── database_schema.sql
│   ├── MANUAL_INSTALACAO.md
│   └── GUIA_USO.md
├── manage.py
├── requirements.txt
├── setup.sh
├── setup.bat
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🎯 Funcionalidades Principais

### Para Alunos e Professores:

1. ✅ Cadastro com validação de instituição
2. ✅ Login seguro
3. ✅ Buscar eventos (por texto, tipo, vagas)
4. ✅ Visualizar detalhes de eventos
5. ✅ Inscrever-se em eventos
6. ✅ Cancelar inscrições
7. ✅ Ver minhas inscrições
8. ✅ Visualizar certificados
9. ✅ Download de certificados em PDF
10. ✅ Editar perfil

### Para Organizadores:

11. ✅ Todas as funcionalidades acima, MAIS:
12. ✅ Criar eventos
13. ✅ Editar eventos
14. ✅ Excluir eventos
15. ✅ Ver lista de inscritos
16. ✅ Emitir certificados
17. ✅ Gerenciar meus eventos

### Para Todos (incluindo visitantes):

18. ✅ Verificar autenticidade de certificados

---

## 🛠️ Tecnologias Utilizadas

### Backend

- Python 3.8+
- Django 4.2
- SQLite3 (dev) / PostgreSQL (prod)
- Pillow (processamento de imagens)
- ReportLab (geração de PDFs)

### Frontend

- HTML5
- CSS3
- Bootstrap 5.3
- Bootstrap Icons
- JavaScript

### Ferramentas

- Git (controle de versão)
- VSCode/PyCharm (desenvolvimento)
- Django Admin (administração)

---

## 📈 Boas Práticas Implementadas

### Código

- ✅ Arquitetura MVC (Model-View-Controller)
- ✅ DRY (Don't Repeat Yourself)
- ✅ Separação de responsabilidades
- ✅ Comentários e docstrings
- ✅ Nomenclatura clara e consistente
- ✅ Validações em múltiplas camadas

### Segurança

- ✅ Senhas com hash (PBKDF2)
- ✅ Proteção CSRF em formulários
- ✅ Validação de permissões
- ✅ SQL Injection prevention (ORM Django)
- ✅ XSS prevention (template escaping)

### UX/UI

- ✅ Interface intuitiva
- ✅ Responsividade mobile
- ✅ Feedback visual constante
- ✅ Mensagens de erro claras
- ✅ Confirmações em ações críticas
- ✅ Design moderno e profissional

### Banco de Dados

- ✅ Normalização (3FN)
- ✅ Índices em campos de busca
- ✅ Relacionamentos bem definidos
- ✅ Integridade referencial
- ✅ Constraints apropriadas

---

## 🚀 Como Usar Este Projeto

### Instalação Rápida (Linux/Mac)

```bash
git clone [repositório]
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python manage.py runserver
```

### Instalação Rápida (Windows)

```cmd
git clone [repositório]
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
setup.bat
venv\Scripts\activate
python manage.py runserver
```

### Acesso

- **Sistema**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin

---

## 📚 Documentação Disponível

Toda a documentação está organizada em:

1. **README.md** - Visão geral e guia rápido
2. **REQUISITOS_E_CASOS_DE_USO.md** - Análise detalhada
3. **DIAGRAMA_BANCO_DADOS.md** - Modelo de dados
4. **database_schema.sql** - Script do banco
5. **MANUAL_INSTALACAO.md** - Guia de instalação completo
6. **GUIA_USO.md** - Manual do usuário
7. **PROJETO_COMPLETO.md** - Este documento (resumo geral)

---

## ✅ Checklist de Entrega

### Requisitos Atendidos:

- [x] **Cadastro de usuários** com validação completa
- [x] **Autenticação de usuários** segura
- [x] **Cadastro de eventos** com todas as informações
- [x] **Gerenciamento de eventos** (CRUD completo)
- [x] **Inscrição de usuários** em eventos
- [x] **Cancelamento de inscrições**
- [x] **Emissão de certificados** em PDF
- [x] **Verificação de certificados** pública
- [x] **Documento de Requisitos e Casos de Uso** (5+ funcionalidades)
- [x] **Modelos Django** funcionando
- [x] **Banco de dados** funcionando
- [x] **Diagrama lógico** do banco (PDF/MD)
- [x] **Script SQL** de criação e população
- [x] **Protótipo de interface** (HTML/CSS funcional)
- [x] **Código no GitHub** organizado
- [x] **README** completo
- [x] **Documentação** detalhada

### Diferenciais Implementados:

- [x] Interface completamente funcional (não apenas protótipo)
- [x] Sistema totalmente implementado e testável
- [x] Scripts de instalação automatizada
- [x] Manual do usuário completo
- [x] Geração de PDFs profissionais
- [x] Busca e filtros avançados
- [x] Design responsivo e moderno
- [x] Validações em múltiplas camadas
- [x] Feedback visual constante
- [x] Documentação exemplar

---

## 🎓 Conclusão

Este projeto entrega um **Sistema de Gestão de Eventos Acadêmicos** completo e profissional, superando os requisitos mínimos especificados.

### Destaques:

- ✅ Todos os requisitos atendidos
- ✅ Sistema 100% funcional
- ✅ Interface moderna e intuitiva
- ✅ Documentação completa e detalhada
- ✅ Código limpo e bem estruturado
- ✅ Pronto para uso em produção (com ajustes de segurança)

### Resultado Final:

Um sistema robusto, escalável e de fácil manutenção que demonstra domínio completo do Django framework e boas práticas de desenvolvimento web.

---

**Desenvolvido com dedicação e atenção aos detalhes** ❤️

**Data de Conclusão**: Outubro de 2025  
**Versão**: 1.0.0  
**Status**: ✅ COMPLETO E FUNCIONAL

---

## 📞 Suporte

Para dúvidas sobre o projeto:

- Consulte a documentação em `/docs/`
- Leia o README.md
- Verifique o GUIA_USO.md
- Email: ana.fmoura@gmail.com
- GitHub: https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

**Obrigado por usar o SGEA!** 🎓
