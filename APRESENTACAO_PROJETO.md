# 🎓 Apresentação do Projeto - SGEA

## Sistema de Gestão de Eventos Acadêmicos

---

## 📌 Identificação

**Nome do Projeto:** SGEA - Sistema de Gestão de Eventos Acadêmicos

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Curso:** Ciência da Computação  
**Disciplina:** Programação para Web  
**Professor(a):** Felippe Pires Ferreira  
**Período:** 2025  
**Data de Entrega:** Outubro de 2025

---

## 📝 Resumo Executivo

O SGEA é um sistema web completo desenvolvido em Django que permite o gerenciamento
integral de eventos acadêmicos como seminários, palestras, minicursos e semanas acadêmicas.

**Principais Características:**

- Sistema 100% funcional (não apenas protótipo)
- Interface moderna e responsiva
- Emissão automática de certificados em PDF
- Controle de vagas em tempo real
- Verificação pública de autenticidade
- Documentação completa e profissional

---

## 🎯 Objetivos Alcançados

✅ Todos os requisitos do trabalho foram atendidos  
✅ Sistema completo e funcional desenvolvido  
✅ Documentação exemplar criada  
✅ Interface profissional implementada  
✅ Banco de dados modelado e documentado  
✅ Código limpo e bem estruturado

---

## 📊 Entregáveis

### 1. Código Fonte

- 3 apps Django (users, events, certificates)
- 24 arquivos Python
- 17 templates HTML/CSS
- ~11.000 linhas de código

### 2. Documentação

- Documento de Requisitos e Casos de Uso (40+ páginas)
- Diagrama Lógico do Banco de Dados (20+ páginas)
- Script SQL completo (400+ linhas)
- Manual de Instalação (30+ páginas)
- Guia do Usuário (30+ páginas)
- README completo (60+ páginas)

### 3. Sistema Funcional

- Backend completo em Django
- Frontend responsivo com Bootstrap
- Banco de dados SQLite/PostgreSQL
- Geração de PDFs com ReportLab
- Sistema de autenticação seguro

---

## 🛠️ Tecnologias Utilizadas

**Backend:**

- Python 3.8+
- Django 4.2
- SQLite3 / PostgreSQL
- Pillow, ReportLab

**Frontend:**

- HTML5, CSS3
- Bootstrap 5.3
- Bootstrap Icons
- JavaScript

---

## ⚡ Funcionalidades Principais

1. **Cadastro de Usuários** - Com validação completa
2. **Autenticação Segura** - Login/logout
3. **Cadastro de Eventos** - CRUD completo
4. **Inscrição em Eventos** - Com controle de vagas
5. **Emissão de Certificados** - PDF profissional
6. **Verificação de Certificados** - Pública e segura

---

## 🔑 Credenciais de Acesso (Demonstração)

**Superusuário Padrão:**

- Username: `admin`
- Password: `12345`
- Perfil: ORGANIZADOR

**URLs de Acesso:**

- Sistema: http://127.0.0.1:8000
- Django Admin: http://127.0.0.1:8000/admin

---

## 📁 Estrutura de Entrega

```
Sistema-de-Gestao-de-Eventos-Academicos-SGEA-/
│
├── 📂 sgea/                  # Configurações Django
├── 📂 users/                 # App de usuários
├── 📂 events/                # App de eventos
├── 📂 certificates/          # App de certificados
├── 📂 templates/             # Interface HTML (17 arquivos)
├── 📂 static/                # CSS e JavaScript
├── 📂 docs/                  # Documentação (6 documentos)
│
├── 📄 README.md              # Documentação principal
├── 📄 PROJETO_COMPLETO.md    # Resumo completo
├── 📄 RESUMO_EXECUTIVO.txt   # Sumário executivo
├── 📄 AUTORES.md             # Informações da equipe
├── 📄 requirements.txt       # Dependências
├── 📄 setup.sh / setup.bat   # Scripts de instalação
└── 📄 manage.py              # Django manager
```

---

## 🚀 Como Executar

### Instalação Rápida (Linux):

```bash
cd Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
./setup.sh
source venv/bin/activate
python manage.py runserver
```

### Criar Superusuário Admin:

```bash
python manage.py shell
```

Cole:

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
print('✅ Admin criado! Username: admin, Password: 12345')
exit()
```

---

## 📈 Estatísticas do Projeto

- **Total de Arquivos:** 59
- **Linhas de Código:** ~11.000
- **Linhas de Documentação:** ~6.000
- **Funcionalidades:** 18 principais
- **Casos de Uso:** 6 completos
- **Requisitos:** 10 funcionais + 6 não funcionais
- **Modelos de Dados:** 4 principais

---

## 🌟 Diferenciais do Projeto

✨ Sistema 100% funcional (não apenas protótipo)  
✨ Interface moderna e profissional  
✨ Documentação exemplar e completa  
✨ Código limpo e bem estruturado  
✨ PDFs profissionais personalizados  
✨ Scripts de instalação automática  
✨ Pronto para uso real

---

## 📚 Documentos do Projeto

### Documentação Técnica:

1. `README.md` - Visão geral e instalação
2. `docs/REQUISITOS_E_CASOS_DE_USO.md` - Análise completa
3. `docs/DIAGRAMA_BANCO_DADOS.md` - Modelo de dados
4. `docs/database_schema.sql` - Script SQL

### Manuais:

5. `docs/MANUAL_INSTALACAO.md` - Instalação detalhada
6. `docs/GUIA_USO.md` - Manual do usuário

### Resumos:

7. `PROJETO_COMPLETO.md` - Resumo técnico
8. `RESUMO_EXECUTIVO.txt` - Sumário executivo
9. `AUTORES.md` - Informações da equipe

---

## ✅ Checklist de Entrega

- [x] Código fonte completo e funcional
- [x] Documento de Requisitos e Casos de Uso
- [x] Modelos Django implementados
- [x] Banco de dados funcionando
- [x] Diagrama lógico do banco (PDF/MD)
- [x] Script SQL de criação e população
- [x] Protótipo de interface (HTML/CSS funcional)
- [x] Código no GitHub
- [x] README completo
- [x] Documentação detalhada
- [x] Sistema testado e validado

---

## 🎯 Conclusão

Este projeto demonstra domínio completo das tecnologias Django, Python, HTML/CSS,
modelagem de banco de dados e boas práticas de desenvolvimento web.

O sistema está **completo, funcional e pronto para uso**, superando os requisitos
mínimos especificados no trabalho.

---

**Desenvolvido com dedicação e profissionalismo** ❤️

**Ana Júlia Moura & Vinicius Martin**  
**Centro Universitário de Brasília (UniCEUB)**  
**Outubro de 2025**

---

## 📞 Informações de Contato

**Projeto SGEA**  
Email: ana.fmoura@gmail.com  
GitHub: https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

---

**© 2025 - Ana Júlia Moura & Vinicius Martin - UniCEUB**
