# Diagrama Lógico do Banco de Dados - SGEA

## Modelo Entidade-Relacionamento (MER)

---

## 👥 Equipe de Desenvolvimento

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Ano:** 2025

---

## 1. Entidades e Atributos

### 1.1 CustomUser (users_customuser)

Armazena informações dos usuários do sistema.

**Campos:**

- `id` (PK, INTEGER): Identificador único do usuário
- `password` (VARCHAR 128): Hash da senha do usuário
- `last_login` (DATETIME): Data e hora do último login
- `is_superuser` (BOOLEAN): Indica se é superusuário
- `username` (VARCHAR 150, UNIQUE): Nome de usuário para login
- `first_name` (VARCHAR 150): Primeiro nome
- `last_name` (VARCHAR 150): Sobrenome
- `email` (VARCHAR 254): Endereço de e-mail
- `is_staff` (BOOLEAN): Indica se tem acesso ao admin
- `is_active` (BOOLEAN): Indica se o usuário está ativo
- `date_joined` (DATETIME): Data de cadastro no sistema
- `telefone` (VARCHAR 15, NULL): Telefone de contato
- `instituicao_ensino` (VARCHAR 200, NULL): Nome da instituição
- `perfil` (VARCHAR 15): Tipo de perfil (ALUNO, PROFESSOR, ORGANIZADOR)
- `data_cadastro` (DATETIME): Data e hora do cadastro

**Índices:**

- PRIMARY KEY (id)
- UNIQUE (username)
- INDEX (perfil)
- INDEX (data_cadastro)

---

### 1.2 Event (events_event)

Armazena informações dos eventos acadêmicos.

**Campos:**

- `id` (PK, INTEGER): Identificador único do evento
- `titulo` (VARCHAR 200): Título do evento
- `descricao` (TEXT): Descrição detalhada
- `tipo_evento` (VARCHAR 20): Tipo (SEMINARIO, PALESTRA, MINICURSO, SEMANA_ACADEMICA)
- `data_inicio` (DATE): Data de início do evento
- `data_fim` (DATE): Data de término do evento
- `horario_inicio` (TIME): Horário de início
- `horario_fim` (TIME): Horário de término
- `local` (VARCHAR 200): Local de realização
- `vagas` (INTEGER): Número total de vagas
- `vagas_disponiveis` (INTEGER): Número de vagas disponíveis
- `organizador_id` (FK, INTEGER): Referência ao organizador
- `imagem` (VARCHAR 100, NULL): Caminho da imagem
- `ativo` (BOOLEAN): Indica se está aceitando inscrições
- `data_criacao` (DATETIME): Data de criação do registro
- `data_atualizacao` (DATETIME): Data da última atualização

**Relacionamentos:**

- `organizador_id` FK → `users_customuser.id` (PROTECT)

**Índices:**

- PRIMARY KEY (id)
- FOREIGN KEY (organizador_id)
- INDEX (tipo_evento)
- INDEX (ativo)
- INDEX (data_inicio)
- INDEX (data_criacao)

---

### 1.3 Inscription (events_inscription)

Armazena as inscrições dos usuários nos eventos.

**Campos:**

- `id` (PK, INTEGER): Identificador único da inscrição
- `evento_id` (FK, INTEGER): Referência ao evento
- `usuario_id` (FK, INTEGER): Referência ao usuário
- `status` (VARCHAR 15): Status (PENDENTE, CONFIRMADA, CANCELADA)
- `data_inscricao` (DATETIME): Data e hora da inscrição
- `observacoes` (TEXT, NULL): Observações adicionais

**Relacionamentos:**

- `evento_id` FK → `events_event.id` (CASCADE)
- `usuario_id` FK → `users_customuser.id` (CASCADE)

**Restrições:**

- UNIQUE (evento_id, usuario_id): Impede inscrição duplicada

**Índices:**

- PRIMARY KEY (id)
- FOREIGN KEY (evento_id)
- FOREIGN KEY (usuario_id)
- UNIQUE (evento_id, usuario_id)
- INDEX (status)
- INDEX (data_inscricao)

---

### 1.4 Certificate (certificates_certificate)

Armazena os certificados emitidos.

**Campos:**

- `id` (PK, INTEGER): Identificador único do certificado
- `inscricao_id` (FK, INTEGER, UNIQUE): Referência à inscrição
- `codigo_verificacao` (UUID, UNIQUE): Código único para verificação
- `data_emissao` (DATETIME): Data e hora de emissão
- `emitido_por_id` (FK, INTEGER): Referência ao organizador emissor
- `carga_horaria` (INTEGER): Carga horária do evento em horas
- `observacoes` (TEXT, NULL): Observações adicionais

**Relacionamentos:**

- `inscricao_id` FK → `events_inscription.id` (PROTECT, UNIQUE)
- `emitido_por_id` FK → `users_customuser.id` (PROTECT)

**Índices:**

- PRIMARY KEY (id)
- FOREIGN KEY (inscricao_id) UNIQUE
- FOREIGN KEY (emitido_por_id)
- UNIQUE (codigo_verificacao)
- INDEX (data_emissao)

---

## 2. Diagrama Entidade-Relacionamento

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                         SGEA - Database Schema                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


┌──────────────────────────────┐
│     users_customuser         │
├──────────────────────────────┤
│ PK  id                       │
│     username (UNIQUE)        │
│     password                 │
│     first_name               │
│     last_name                │
│     email                    │
│     telefone                 │
│     instituicao_ensino       │
│     perfil                   │◄─────┐
│     data_cadastro            │      │
│     is_active                │      │
│     is_staff                 │      │
│     is_superuser             │      │
│     last_login               │      │
│     date_joined              │      │
└──────────────────────────────┘      │
       │                               │
       │ 1:N (organizador)             │ N:1 (usuario)
       │                               │
       ▼                               │
┌──────────────────────────────┐      │
│      events_event            │      │
├──────────────────────────────┤      │
│ PK  id                       │      │
│ FK  organizador_id           │──────┘
│     titulo                   │
│     descricao                │
│     tipo_evento              │
│     data_inicio              │
│     data_fim                 │
│     horario_inicio           │
│     horario_fim              │
│     local                    │
│     vagas                    │
│     vagas_disponiveis        │
│     imagem                   │
│     ativo                    │
│     data_criacao             │
│     data_atualizacao         │
└──────────────────────────────┘
       │
       │ 1:N (evento)
       │
       ▼
┌──────────────────────────────┐
│   events_inscription         │
├──────────────────────────────┤
│ PK  id                       │          ┌──────────────────────────────┐
│ FK  evento_id                │          │  certificates_certificate    │
│ FK  usuario_id               │◄─────────├──────────────────────────────┤
│     status                   │  1:1     │ PK  id                       │
│     data_inscricao           │ (inscr)  │ FK  inscricao_id (UNIQUE)    │
│     observacoes              │          │ FK  emitido_por_id           │─────┐
│ UK  (evento_id, usuario_id)  │          │     codigo_verificacao (UUID)│     │
└──────────────────────────────┘          │     data_emissao             │     │
                                          │     carga_horaria            │     │
                                          │     observacoes              │     │
                                          └──────────────────────────────┘     │
                                                                               │
                                                N:1 (emitido_por)              │
                                                                               │
                                          ┌────────────────────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │   users_customuser      │
                              │  (mesmo da primeira     │
                              │   tabela)               │
                              └─────────────────────────┘


LEGENDA:
--------
PK  = Primary Key (Chave Primária)
FK  = Foreign Key (Chave Estrangeira)
UK  = Unique Key (Chave Única/Restrição de Unicidade)
1:N = Relação Um para Muitos
N:1 = Relação Muitos para Um
1:1 = Relação Um para Um
```

---

## 3. Cardinalidades

### 3.1 CustomUser → Event

- **Tipo:** 1:N (Um para Muitos)
- **Descrição:** Um organizador pode criar vários eventos
- **Regra:** Um evento tem exatamente um organizador
- **Ação em Cascata:** ON DELETE PROTECT (não pode excluir organizador com eventos)

### 3.2 Event → Inscription

- **Tipo:** 1:N (Um para Muitos)
- **Descrição:** Um evento pode ter várias inscrições
- **Regra:** Uma inscrição pertence a exatamente um evento
- **Ação em Cascata:** ON DELETE CASCADE (excluir evento exclui inscrições)

### 3.3 CustomUser → Inscription

- **Tipo:** 1:N (Um para Muitos)
- **Descrição:** Um usuário pode ter várias inscrições
- **Regra:** Uma inscrição pertence a exatamente um usuário
- **Restrição:** Um usuário não pode se inscrever duas vezes no mesmo evento
- **Ação em Cascata:** ON DELETE CASCADE (excluir usuário exclui suas inscrições)

### 3.4 Inscription → Certificate

- **Tipo:** 1:1 (Um para Um)
- **Descrição:** Uma inscrição pode ter apenas um certificado
- **Regra:** Um certificado está vinculado a exatamente uma inscrição
- **Ação em Cascata:** ON DELETE PROTECT (não pode excluir inscrição com certificado)

### 3.5 CustomUser → Certificate

- **Tipo:** 1:N (Um para Muitos)
- **Descrição:** Um organizador pode emitir vários certificados
- **Regra:** Um certificado tem exatamente um emissor
- **Ação em Cascata:** ON DELETE PROTECT (não pode excluir organizador com certificados)

---

## 4. Regras de Integridade

### 4.1 Integridade de Domínio

- `perfil` deve ser: 'ALUNO', 'PROFESSOR' ou 'ORGANIZADOR'
- `tipo_evento` deve ser: 'SEMINARIO', 'PALESTRA', 'MINICURSO' ou 'SEMANA_ACADEMICA'
- `status` deve ser: 'PENDENTE', 'CONFIRMADA' ou 'CANCELADA'
- `vagas` deve ser maior que 0
- `vagas_disponiveis` deve ser maior ou igual a 0
- `carga_horaria` deve ser maior que 0
- `data_fim` deve ser maior ou igual a `data_inicio`

### 4.2 Integridade Referencial

- Todo evento deve ter um organizador válido
- Toda inscrição deve ter um evento e usuário válidos
- Todo certificado deve ter uma inscrição e emissor válidos
- Organizadores com eventos não podem ser excluídos (PROTECT)
- Organizadores com certificados emitidos não podem ser excluídos (PROTECT)
- Inscrições com certificados não podem ser excluídas (PROTECT)

### 4.3 Integridade de Chave

- `username` deve ser único
- `email` deve ser único
- `codigo_verificacao` deve ser único
- Combinação `(evento_id, usuario_id)` deve ser única em Inscription
- `inscricao_id` deve ser único em Certificate

---

## 5. Triggers e Regras de Negócio

### 5.1 Gerenciamento de Vagas

**Trigger:** Após inserir/atualizar/deletar Inscription

**Lógica:**

- Ao criar inscrição com status CONFIRMADA: decrementar vagas_disponiveis
- Ao cancelar inscrição (status → CANCELADA): incrementar vagas_disponiveis
- Ao deletar inscrição CONFIRMADA: incrementar vagas_disponiveis

### 5.2 Validação de Instituição

**Trigger:** Antes de inserir/atualizar CustomUser

**Lógica:**

- Se perfil = 'ALUNO' ou 'PROFESSOR': instituicao_ensino é obrigatória
- Se perfil = 'ORGANIZADOR': instituicao_ensino é opcional

### 5.3 Validação de Datas

**Trigger:** Antes de inserir/atualizar Event

**Lógica:**

- data_fim >= data_inicio
- Se data_inicio = data_fim: horario_fim > horario_inicio

---

## 6. Índices para Otimização

### 6.1 Índices em CustomUser

```sql
CREATE INDEX idx_user_perfil ON users_customuser(perfil);
CREATE INDEX idx_user_cadastro ON users_customuser(data_cadastro);
```

### 6.2 Índices em Event

```sql
CREATE INDEX idx_event_tipo ON events_event(tipo_evento);
CREATE INDEX idx_event_ativo ON events_event(ativo);
CREATE INDEX idx_event_data_inicio ON events_event(data_inicio);
CREATE INDEX idx_event_criacao ON events_event(data_criacao);
CREATE INDEX idx_event_organizador ON events_event(organizador_id);
```

### 6.3 Índices em Inscription

```sql
CREATE INDEX idx_inscription_status ON events_inscription(status);
CREATE INDEX idx_inscription_data ON events_inscription(data_inscricao);
CREATE INDEX idx_inscription_evento ON events_inscription(evento_id);
CREATE INDEX idx_inscription_usuario ON events_inscription(usuario_id);
```

### 6.4 Índices em Certificate

```sql
CREATE INDEX idx_certificate_emissao ON certificates_certificate(data_emissao);
CREATE INDEX idx_certificate_emissor ON certificates_certificate(emitido_por_id);
```

---

## 7. Considerações de Segurança

1. **Senhas:** Armazenadas com hash usando algoritmo PBKDF2 (Django padrão)
2. **Códigos UUID:** Gerados automaticamente, não sequenciais
3. **Soft Delete:** Usar flag `is_active` ao invés de exclusão física quando apropriado
4. **Auditoria:** Campos `data_criacao` e `data_atualizacao` em tabelas principais
5. **Validação:** Constraints a nível de banco + validação a nível de aplicação

---

## 8. Normalização

O banco de dados está na **3ª Forma Normal (3FN)**:

- **1FN:** Todos os atributos são atômicos
- **2FN:** Todos os atributos não-chave dependem totalmente da chave primária
- **3FN:** Não há dependências transitivas entre atributos não-chave

---

## 9. Estimativa de Volume de Dados

| Tabela      | Registros Estimados | Crescimento Anual |
| ----------- | ------------------- | ----------------- |
| CustomUser  | 1.000 - 10.000      | 20%               |
| Event       | 100 - 500           | 30%               |
| Inscription | 5.000 - 50.000      | 40%               |
| Certificate | 3.000 - 30.000      | 35%               |

---

**Documento elaborado em:** Outubro de 2025  
**Versão:** 1.0  
**SGBD:** SQLite3 (Desenvolvimento) / PostgreSQL (Produção)
