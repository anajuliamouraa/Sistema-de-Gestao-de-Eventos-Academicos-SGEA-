# ℹ️ Informações do Projeto SGEA

## Sistema de Gestão de Eventos Acadêmicos

---

## 👥 AUTORES

### Ana Júlia Moura

- **RA:** 22403137
- **Email:** ana.fmoura@gmail.com
- **Contribuição:** 50%

### Vinicius Martin

- **RA:** 22402759
- **Email:** vinicius.martin@exemplo.com
- **Contribuição:** 50%

---

## 🏫 INFORMAÇÕES ACADÊMICAS

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Curso:** Ciência da Computação  
**Disciplina:** Programação para Web  
**Professor(a):** Felippe Pires Ferreira  
**Semestre/Período:** 2025  
**Data de Entrega:** Outubro de 2025

---

## 🎯 SOBRE O PROJETO

**Nome:** SGEA - Sistema de Gestão de Eventos Acadêmicos  
**Tipo:** Sistema Web Completo  
**Tecnologia:** Django 4.2 + Python 3.8+  
**Status:** ✅ Completo e Funcional  
**Versão:** 1.0.0

---

## 🔑 CREDENCIAIS DE ACESSO (DEMO)

### Superusuário Padrão:

```
Username: admin
Password: 12345
Perfil:   ORGANIZADOR
```

### URLs do Sistema:

- **Sistema Principal:** http://127.0.0.1:8000
- **Django Admin:** http://127.0.0.1:8000/admin
- **Login:** http://127.0.0.1:8000/users/login
- **Cadastro:** http://127.0.0.1:8000/users/register

---

## 📊 ESTATÍSTICAS DO PROJETO

| Item                      | Quantidade |
| ------------------------- | ---------- |
| Total de Arquivos         | 62         |
| Linhas de Código Python   | ~2.500     |
| Linhas de HTML/CSS/JS     | ~2.200     |
| Linhas de Documentação    | ~6.000     |
| Apps Django               | 3          |
| Modelos de Dados          | 4          |
| Templates HTML            | 17         |
| Views Implementadas       | 15+        |
| Casos de Uso Documentados | 6          |
| Requisitos Funcionais     | 10         |

---

## 📁 ESTRUTURA DE ENTREGA

```
SGEA/
├── Código Fonte (Backend + Frontend)
│   ├── 3 Apps Django
│   ├── 24 arquivos Python
│   ├── 17 templates HTML
│   └── Arquivos CSS/JS
│
├── Documentação Técnica
│   ├── Requisitos e Casos de Uso (40+ páginas)
│   ├── Diagrama do Banco de Dados (20+ páginas)
│   ├── Script SQL completo
│   └── README completo (60+ páginas)
│
├── Manuais de Uso
│   ├── Manual de Instalação (30+ páginas)
│   ├── Guia do Usuário (30+ páginas)
│   └── Documentos de Apresentação
│
└── Scripts de Automação
    ├── setup.sh (Linux/Mac)
    └── setup.bat (Windows)
```

---

## ✅ REQUISITOS ATENDIDOS

- [x] Cadastro de usuários completo
- [x] Autenticação de usuários
- [x] Cadastro de eventos
- [x] Gerenciamento de eventos (CRUD)
- [x] Inscrição de usuários
- [x] Emissão de certificados em PDF
- [x] Documento de Requisitos e Casos de Uso
- [x] Modelos Django funcionando
- [x] Banco de dados modelado
- [x] Diagrama lógico do banco
- [x] Script SQL de criação e população
- [x] Interface funcional (HTML/CSS)
- [x] Código no GitHub
- [x] README e documentação completa

---

## 🚀 COMO EXECUTAR

### Instalação Rápida:

```bash
cd /home/s0ft/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
./setup.sh
source venv/bin/activate
python manage.py runserver
```

### Criar Admin Padrão:

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
print('✅ Admin criado!')
exit()
```

---

## 📚 DOCUMENTOS PARA ENTREGA

### Principais:

1. ✅ `README.md` - Visão geral completa
2. ✅ `PROJETO_COMPLETO.md` - Resumo técnico
3. ✅ `RESUMO_EXECUTIVO.txt` - Sumário executivo
4. ✅ `APRESENTACAO_PROJETO.md` - Apresentação formal
5. ✅ `AUTORES.md` - Informações da equipe

### Documentação Técnica:

6. ✅ `docs/REQUISITOS_E_CASOS_DE_USO.md`
7. ✅ `docs/DIAGRAMA_BANCO_DADOS.md`
8. ✅ `docs/database_schema.sql`
9. ✅ `docs/MANUAL_INSTALACAO.md`
10. ✅ `docs/GUIA_USO.md`

### Código Fonte:

11. ✅ Todos os arquivos Python (.py)
12. ✅ Todos os templates HTML
13. ✅ Arquivos CSS e JavaScript
14. ✅ Configurações Django

---

## 🎓 DIFERENCIAIS

✨ Sistema 100% funcional (não apenas protótipo)  
✨ Interface profissional e responsiva  
✨ Documentação exemplar (150+ páginas)  
✨ Geração automática de PDFs  
✨ Scripts de instalação automatizada  
✨ Código limpo e bem documentado  
✨ Pronto para uso real

---

## 📞 CONTATO

**Email do Projeto:** ana.fmoura@gmail.com  
**GitHub:** https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

---

## ⚠️ NOTA IMPORTANTE

**Senha Padrão:** A senha "12345" é apenas para demonstração acadêmica.  
**Segurança:** Em produção, use senhas fortes e secure!

---

**© 2025 - Ana Júlia Moura & Vinicius Martin**  
**Centro Universitário de Brasília (UniCEUB)**  
**Todos os direitos reservados**
