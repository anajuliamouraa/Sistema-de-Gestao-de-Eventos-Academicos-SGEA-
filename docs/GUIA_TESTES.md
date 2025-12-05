# Guia de Testes - SGEA

## Sistema de Gestão de Eventos Acadêmicos - Fase 2

---

## 1. Configuração Inicial para Testes

### 1.1 Instalar Dependências

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 1.2 Executar Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 1.3 Carregar Dados de Teste (Seeding)

Execute o comando de seeding para popular o banco com dados iniciais:

```bash
python manage.py seed_data
```

Este comando irá criar:
- 3 usuários de teste (organizador, professor, aluno)
- Usuários extras para testes
- 5 eventos de exemplo

---

## 2. Credenciais de Teste

### Usuário Organizador
- **Email:** organizador@sgea.com
- **Senha:** Admin@123
- **Permissões:** Criar/editar/excluir eventos, ver inscritos, confirmar presenças, emitir certificados, acessar auditoria

### Usuário Professor
- **Email:** professor@sgea.com
- **Senha:** Professor@123
- **Permissões:** Inscrever-se em eventos, ver certificados, pode ser responsável por eventos

### Usuário Aluno
- **Email:** aluno@sgea.com
- **Senha:** Aluno@123
- **Permissões:** Inscrever-se em eventos, ver certificados

---

## 3. Roteiro de Testes Funcionais

### 3.1 Testes de Autenticação

#### Teste 1: Cadastro de Novo Usuário
1. Acesse http://127.0.0.1:8000/users/register/
2. Preencha o formulário:
   - Nome: João
   - Sobrenome: Silva
   - Usuário: joaosilva
   - Email: joao@teste.com
   - Telefone: (61) 99999-0000 (testar máscara)
   - Perfil: Aluno
   - Instituição: UniCEUB
   - Senha: Teste@123 (testar validação de força)
   - Confirmar senha: Teste@123
3. **Resultado esperado:** 
   - Cadastro realizado com sucesso
   - Email de confirmação enviado (verificar console)
   - Redirecionamento para login

#### Teste 2: Validação de Senha Fraca
1. Tente cadastrar com senha "123456"
2. **Resultado esperado:** Erro de validação exigindo senha mais forte

#### Teste 3: Login com Email Não Confirmado
1. Tente fazer login com usuário recém-cadastrado
2. **Resultado esperado:** Mensagem solicitando confirmação de email

#### Teste 4: Confirmação de Email
1. Copie o código de ativação do console (ou email)
2. Acesse http://127.0.0.1:8000/users/activate/{codigo}/
3. **Resultado esperado:** Email confirmado, pode fazer login

#### Teste 5: Login com Credenciais Válidas
1. Acesse http://127.0.0.1:8000/users/login/
2. Use: organizador@sgea.com / Admin@123
3. **Resultado esperado:** Login bem-sucedido, redirecionamento para home

### 3.2 Testes de Eventos

#### Teste 6: Criar Evento (Organizador)
1. Faça login como organizador
2. Clique em "Criar Evento"
3. Preencha o formulário:
   - Título: Evento Teste
   - Descrição: Descrição do evento teste
   - Tipo: Palestra
   - Professor Responsável: (selecione um professor)
   - Data Início: (use o datepicker - data futura)
   - Data Fim: (igual ou após data início)
   - Horário Início: 09:00 (use o timepicker)
   - Horário Fim: 17:00
   - Local: Auditório Principal
   - Vagas: 50
   - Banner: (upload de imagem JPG/PNG)
4. **Resultado esperado:** Evento criado com sucesso

#### Teste 7: Validação de Data Passada
1. Tente criar evento com data de início no passado
2. **Resultado esperado:** Erro de validação

#### Teste 8: Validação de Banner
1. Tente fazer upload de arquivo não-imagem (ex: .pdf)
2. **Resultado esperado:** Erro de validação de tipo de arquivo

### 3.3 Testes de Inscrição

#### Teste 9: Inscrição em Evento (Aluno)
1. Faça logout e login como aluno@sgea.com
2. Navegue até um evento com vagas
3. Clique em "Inscrever-se"
4. Adicione observações (opcional)
5. Confirme inscrição
6. **Resultado esperado:** 
   - Inscrição confirmada
   - Email de confirmação enviado
   - Vagas disponíveis decrementadas

#### Teste 10: Tentativa de Inscrição Duplicada
1. Tente se inscrever novamente no mesmo evento
2. **Resultado esperado:** Mensagem de erro informando já estar inscrito

#### Teste 11: Organizador Tentando se Inscrever
1. Faça login como organizador
2. Tente se inscrever em qualquer evento
3. **Resultado esperado:** Mensagem de erro - organizadores não podem se inscrever

### 3.4 Testes de Certificados

#### Teste 12: Confirmar Presenças
1. Faça login como organizador
2. Vá para "Meus Eventos" → evento com inscritos
3. Clique em "Confirmar Presenças"
4. Marque alguns participantes como presentes
5. **Resultado esperado:** Presenças salvas com sucesso

#### Teste 13: Gerar Certificados Automaticamente
```bash
# Executar o comando (em modo simulação primeiro)
python manage.py generate_certificates --dry-run

# Se tudo OK, executar de verdade
python manage.py generate_certificates
```
**Resultado esperado:** Certificados gerados para inscritos com presença confirmada em eventos passados

#### Teste 14: Verificar Certificado
1. Acesse "Verificar Certificado"
2. Digite o código UUID de um certificado
3. **Resultado esperado:** Dados do certificado exibidos

### 3.5 Testes da API REST

#### Teste 15: Obter Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "aluno", "password": "Aluno@123"}'
```
**Resultado esperado:** JSON com token

#### Teste 16: Consultar Eventos
```bash
curl http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Token SEU_TOKEN"
```
**Resultado esperado:** Lista de eventos em JSON

#### Teste 17: Inscrever via API
```bash
curl -X POST http://127.0.0.1:8000/api/inscriptions/ \
  -H "Authorization: Token SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"evento_id": 1}'
```
**Resultado esperado:** Inscrição criada

#### Teste 18: Testar Rate Limiting
1. Execute mais de 20 consultas de eventos em um dia
2. **Resultado esperado:** Erro 429 (Too Many Requests)

### 3.6 Testes de Auditoria

#### Teste 19: Consultar Logs de Auditoria
1. Faça login como organizador
2. Acesse "Auditoria" no menu
3. Filtre por data, usuário ou ação
4. **Resultado esperado:** Lista de ações auditadas

#### Teste 20: Verificar Log de Ações
1. Realize algumas ações (criar evento, inscrever, etc.)
2. Verifique se aparecem nos logs de auditoria
3. **Resultado esperado:** Todas as ações registradas

### 3.7 Testes de Validação de Formulários

#### Teste 21: Máscara de Telefone
1. No cadastro ou perfil, digite um número de telefone
2. **Resultado esperado:** Máscara (XX) XXXXX-XXXX aplicada automaticamente

#### Teste 22: Datepicker
1. No formulário de evento, clique no campo de data
2. **Resultado esperado:** Calendário visual em português

#### Teste 23: Timepicker
1. No formulário de evento, clique no campo de horário
2. **Resultado esperado:** Seletor de hora com intervalos de 15 minutos

---

## 4. Testes de Permissões

| Ação | Organizador | Professor | Aluno |
|------|-------------|-----------|-------|
| Criar Evento | ✅ | ❌ | ❌ |
| Editar Evento | ✅ (próprios) | ❌ | ❌ |
| Excluir Evento | ✅ (próprios) | ❌ | ❌ |
| Inscrever-se | ❌ | ✅ | ✅ |
| Ver Inscritos | ✅ (próprios eventos) | ❌ | ❌ |
| Confirmar Presenças | ✅ | ❌ | ❌ |
| Emitir Certificados | ✅ | ❌ | ❌ |
| Ver Auditoria | ✅ | ❌ | ❌ |
| Ser Responsável | ❌ | ✅ | ❌ |

---

## 5. Testes de Interface

### 5.1 Responsividade
1. Acesse o sistema em diferentes tamanhos de tela
2. **Resultado esperado:** Layout adaptado para mobile e desktop

### 5.2 Acessibilidade
1. Navegue usando apenas o teclado (Tab)
2. Use leitor de tela
3. **Resultado esperado:** 
   - Skip link funcional
   - Foco visível
   - Labels adequados

---

## 6. Checklist de Funcionalidades Fase 2

- [ ] Máscara de telefone (XX) XXXXX-XXXX
- [ ] Datepicker com jQuery
- [ ] Timepicker com jQuery
- [ ] Validação de imagem no banner
- [ ] Seeding de usuários de teste
- [ ] API REST - Consulta de eventos
- [ ] API REST - Inscrição
- [ ] Autenticação por token
- [ ] Rate limiting (20/dia eventos, 50/dia inscrições)
- [ ] Professor responsável no evento
- [ ] Data de início não pode ser passada
- [ ] Organizador não pode se inscrever
- [ ] Senha com requisitos de segurança
- [ ] Email de confirmação de cadastro
- [ ] Campo de confirmação de email
- [ ] Bloqueio até confirmar email
- [ ] Confirmação de presença
- [ ] Emissão automática de certificados
- [ ] Registros de auditoria
- [ ] Tela de consulta de auditoria
- [ ] Identidade visual consistente

---

## 7. Comandos Úteis

```bash
# Executar servidor
python manage.py runserver

# Popular banco de dados
python manage.py seed_data

# Gerar certificados automaticamente
python manage.py generate_certificates

# Verificar migrações pendentes
python manage.py showmigrations

# Criar superusuário
python manage.py createsuperuser

# Shell interativo
python manage.py shell
```

---

## 8. Solução de Problemas

### Erro: "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Erro: Migrações não aplicadas
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erro: Usuários de teste não existem
```bash
python manage.py seed_data
```

### Erro: Certificados não sendo gerados
- Verifique se o evento já passou (data_fim < hoje)
- Verifique se há inscritos com presença confirmada

---

## 9. Contato

Para dúvidas sobre os testes:
- **Email:** ana.fmoura@gmail.com
- **GitHub:** https://github.com/anajuliamouraa/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-

---

**Versão do Guia:** 2.0  
**Data:** Dezembro de 2025

