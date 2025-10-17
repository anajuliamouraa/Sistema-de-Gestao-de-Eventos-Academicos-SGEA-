# Sistema de Gestão de Eventos Acadêmicos (SGEA)

## Documento de Requisitos e Casos de Uso

---

## 👥 Equipe de Desenvolvimento

**Desenvolvido por:**

- **Ana Júlia Moura** - RA: 22403137
- **Vinicius Martin** - RA: 22402759

**Instituição:** Centro Universitário de Brasília (UniCEUB)  
**Ano:** 2025

---

## 1. Introdução

### 1.1 Objetivo do Sistema

O Sistema de Gestão de Eventos Acadêmicos (SGEA) é uma aplicação web desenvolvida para facilitar o gerenciamento de eventos acadêmicos, tais como seminários, palestras, minicursos e semanas acadêmicas. O sistema permite o cadastro de usuários, criação e gerenciamento de eventos, inscrição de participantes e emissão de certificados.

### 1.2 Escopo

O sistema abrange:

- Cadastro e autenticação de usuários com diferentes perfis
- Criação e gerenciamento de eventos por organizadores
- Inscrição de alunos e professores em eventos
- Emissão e verificação de certificados de participação
- Controle de vagas e participantes

---

## 2. Requisitos Funcionais

### RF01 - Cadastro de Usuários

**Descrição:** O sistema deve permitir que novos usuários realizem seu cadastro informando dados pessoais e escolhendo seu perfil de acesso.

**Dados Necessários:**

- Nome (obrigatório)
- Sobrenome (obrigatório)
- Nome de usuário/login (obrigatório, único)
- E-mail (obrigatório, único)
- Senha (obrigatório)
- Telefone (opcional)
- Instituição de Ensino (obrigatório para alunos e professores)
- Perfil: Aluno, Professor ou Organizador (obrigatório)

**Regras de Negócio:**

- RN01: O nome de usuário deve ser único no sistema
- RN02: O e-mail deve ser único e válido
- RN03: A senha deve atender aos requisitos mínimos de segurança do Django
- RN04: Para perfis "Aluno" e "Professor", a instituição de ensino é obrigatória
- RN05: Para perfil "Organizador", a instituição de ensino é opcional

**Prioridade:** Alta

---

### RF02 - Autenticação de Usuários

**Descrição:** O sistema deve permitir que usuários cadastrados façam login utilizando seu nome de usuário e senha.

**Dados Necessários:**

- Nome de usuário
- Senha

**Regras de Negócio:**

- RN06: Apenas usuários cadastrados podem acessar o sistema
- RN07: Após 3 tentativas incorretas consecutivas, implementar medidas de segurança
- RN08: O sistema deve manter a sessão do usuário durante a navegação
- RN09: Usuários podem fazer logout a qualquer momento

**Prioridade:** Alta

---

### RF03 - Cadastro de Eventos

**Descrição:** Usuários com perfil "Organizador" podem criar novos eventos acadêmicos no sistema.

**Dados Necessários:**

- Título do evento (obrigatório)
- Descrição detalhada (obrigatório)
- Tipo de evento: Seminário, Palestra, Minicurso ou Semana Acadêmica (obrigatório)
- Data de início (obrigatório)
- Data de término (obrigatório)
- Horário de início (obrigatório)
- Horário de término (obrigatório)
- Local (obrigatório)
- Quantidade de vagas (obrigatório, mínimo 1)
- Imagem de divulgação (opcional)
- Status ativo/inativo (obrigatório)

**Regras de Negócio:**

- RN10: Apenas usuários com perfil "Organizador" podem criar eventos
- RN11: A data de término não pode ser anterior à data de início
- RN12: Se o evento ocorrer em um único dia, o horário de término deve ser posterior ao horário de início
- RN13: O número de vagas deve ser um valor positivo maior que zero
- RN14: O organizador responsável é automaticamente definido como o usuário que criou o evento
- RN15: As vagas disponíveis são inicializadas com o mesmo valor das vagas totais

**Prioridade:** Alta

---

### RF04 - Gerenciamento de Eventos

**Descrição:** Organizadores podem editar, visualizar detalhes e excluir eventos que criaram.

**Funcionalidades:**

- Editar informações do evento
- Ativar/desativar inscrições
- Visualizar lista de inscritos
- Excluir evento

**Regras de Negócio:**

- RN16: Apenas o organizador responsável pode editar ou excluir seu evento
- RN17: Ao desativar um evento, novas inscrições não são permitidas
- RN18: A exclusão de um evento afeta as inscrições e certificados vinculados
- RN19: O sistema deve alertar sobre consequências antes da exclusão

**Prioridade:** Alta

---

### RF05 - Inscrição de Usuários em Eventos

**Descrição:** Alunos e professores podem se inscrever em eventos disponíveis.

**Dados Necessários:**

- Evento selecionado
- Observações (opcional)

**Regras de Negócio:**

- RN20: Usuários autenticados podem se inscrever em eventos ativos
- RN21: Não é permitida inscrição duplicada no mesmo evento
- RN22: Apenas eventos com vagas disponíveis aceitam novas inscrições
- RN23: Eventos inativos não aceitam inscrições
- RN24: Eventos que já ocorreram não aceitam inscrições
- RN25: Ao confirmar inscrição, uma vaga é decrementada
- RN26: O status inicial da inscrição é "Confirmada"
- RN27: Usuários podem cancelar suas próprias inscrições
- RN28: Ao cancelar inscrição, a vaga é liberada

**Prioridade:** Alta

---

### RF06 - Emissão de Certificados

**Descrição:** Organizadores podem emitir certificados de participação para usuários inscritos em seus eventos.

**Dados Necessários:**

- Inscrição do participante
- Carga horária do evento (obrigatório)
- Observações (opcional)

**Regras de Negócio:**

- RN29: Apenas o organizador do evento pode emitir certificados
- RN30: Certificados só podem ser emitidos para inscrições confirmadas
- RN31: Cada inscrição pode ter apenas um certificado
- RN32: O certificado recebe um código UUID único para verificação
- RN33: A data de emissão é registrada automaticamente
- RN34: O organizador emissor é registrado no certificado
- RN35: Certificados podem ser baixados em formato PDF
- RN36: O PDF deve conter todas as informações do evento e participante

**Prioridade:** Alta

---

### RF07 - Visualização e Download de Certificados

**Descrição:** Participantes podem visualizar e fazer download de seus certificados em formato PDF.

**Funcionalidades:**

- Listar todos os certificados do usuário
- Visualizar certificado online
- Download do certificado em PDF
- Compartilhar código de verificação

**Regras de Negócio:**

- RN37: Usuários podem acessar apenas seus próprios certificados
- RN38: O PDF deve ser gerado em tempo real
- RN39: O certificado deve conter informações completas do evento
- RN40: O código de verificação deve ser visível no certificado

**Prioridade:** Alta

---

### RF08 - Verificação de Autenticidade de Certificados

**Descrição:** Qualquer pessoa pode verificar a autenticidade de um certificado através do código de verificação.

**Dados Necessários:**

- Código de verificação (UUID)

**Regras de Negócio:**

- RN41: A verificação é pública, não requer autenticação
- RN42: O sistema deve validar o formato do código UUID
- RN43: Se o certificado existir, exibir informações básicas
- RN44: Se não existir, exibir mensagem de erro
- RN45: Não permitir múltiplas tentativas em curto período (proteção contra brute force)

**Prioridade:** Média

---

### RF09 - Busca e Filtro de Eventos

**Descrição:** Usuários podem buscar e filtrar eventos disponíveis.

**Critérios de Busca:**

- Texto livre (busca em título, descrição e local)
- Tipo de evento
- Disponibilidade de vagas

**Regras de Negócio:**

- RN46: A busca deve ser case-insensitive
- RN47: Apenas eventos ativos são exibidos por padrão
- RN48: Os resultados são paginados (9 eventos por página)
- RN49: Eventos são ordenados por data (mais recentes primeiro)

**Prioridade:** Média

---

### RF10 - Gerenciamento de Perfil

**Descrição:** Usuários podem visualizar e editar suas informações pessoais.

**Dados Editáveis:**

- Nome e sobrenome
- E-mail
- Telefone
- Instituição de ensino

**Regras de Negócio:**

- RN50: O perfil de usuário (aluno/professor/organizador) não pode ser alterado
- RN51: O nome de usuário não pode ser alterado
- RN52: Alterações são validadas antes de salvar
- RN53: O sistema exibe confirmação após atualização bem-sucedida

**Prioridade:** Média

---

## 3. Requisitos Não Funcionais

### RNF01 - Usabilidade

- O sistema deve ter interface intuitiva e responsiva
- Deve funcionar em dispositivos móveis e desktops
- Mensagens de erro devem ser claras e orientativas
- Uso de ícones para melhor visualização

### RNF02 - Performance

- Páginas devem carregar em menos de 3 segundos
- Busca de eventos deve retornar resultados em menos de 1 segundo
- Geração de PDF deve ocorrer em menos de 5 segundos

### RNF03 - Segurança

- Senhas devem ser armazenadas com hash
- Proteção contra CSRF em todos os formulários
- Validação de permissões em todas as operações
- Sessões devem expirar após período de inatividade

### RNF04 - Confiabilidade

- Backup diário do banco de dados
- Tratamento de erros com mensagens amigáveis
- Log de operações críticas

### RNF05 - Manutenibilidade

- Código seguindo padrão PEP 8 (Python)
- Documentação inline do código
- Arquitetura MVC bem definida
- Testes unitários para funcionalidades críticas

### RNF06 - Compatibilidade

- Navegadores: Chrome, Firefox, Safari, Edge (versões recentes)
- Python 3.8+
- Django 4.2+
- Bootstrap 5.3+

---

## 4. Casos de Uso

### CU01 - Cadastro de Usuário

**Ator Principal:** Visitante (usuário não cadastrado)

**Pré-condições:** Nenhuma

**Fluxo Principal:**

1. Visitante acessa a página de cadastro
2. Sistema exibe formulário de cadastro
3. Visitante preenche todos os campos obrigatórios
4. Visitante seleciona seu perfil (Aluno, Professor ou Organizador)
5. Se perfil for Aluno ou Professor, visitante informa instituição de ensino
6. Visitante submete o formulário
7. Sistema valida os dados informados
8. Sistema cria novo usuário no banco de dados
9. Sistema redireciona para página de login
10. Sistema exibe mensagem de sucesso

**Fluxos Alternativos:**

**FA01 - Dados inválidos:**

- No passo 7, se algum dado for inválido:
  - Sistema exibe mensagem de erro específica
  - Sistema retorna ao passo 2
  - Campos já preenchidos são mantidos

**FA02 - Usuário já existe:**

- No passo 8, se nome de usuário ou e-mail já existir:
  - Sistema exibe mensagem informando que o dado já está em uso
  - Sistema retorna ao passo 2

**FA03 - Instituição não informada:**

- No passo 7, se perfil for Aluno/Professor e instituição não foi informada:
  - Sistema exibe mensagem de erro
  - Sistema retorna ao passo 2

**Pós-condições:** Novo usuário criado e pode fazer login no sistema

---

### CU02 - Autenticação de Usuário

**Ator Principal:** Usuário Cadastrado

**Pré-condições:** Usuário deve estar cadastrado no sistema

**Fluxo Principal:**

1. Usuário acessa a página de login
2. Sistema exibe formulário de login
3. Usuário informa nome de usuário e senha
4. Usuário submete o formulário
5. Sistema valida as credenciais
6. Sistema cria sessão para o usuário
7. Sistema redireciona para página inicial de eventos
8. Sistema exibe mensagem de boas-vindas

**Fluxos Alternativos:**

**FA01 - Credenciais inválidas:**

- No passo 5, se credenciais estiverem incorretas:
  - Sistema exibe mensagem de erro genérica
  - Sistema retorna ao passo 2
  - Campo de senha é limpo

**FA02 - Usuário já autenticado:**

- No passo 1, se usuário já está logado:
  - Sistema redireciona diretamente para página inicial
  - Caso de uso termina

**Pós-condições:** Usuário autenticado e pode acessar funcionalidades do sistema

---

### CU03 - Criar Evento

**Ator Principal:** Organizador

**Pré-condições:**

- Usuário deve estar autenticado
- Usuário deve ter perfil "Organizador"

**Fluxo Principal:**

1. Organizador acessa página de criação de evento
2. Sistema exibe formulário de cadastro de evento
3. Organizador preenche informações do evento:
   - Título, descrição, tipo
   - Datas e horários
   - Local e quantidade de vagas
   - Imagem (opcional)
4. Organizador submete o formulário
5. Sistema valida os dados
6. Sistema cria evento no banco de dados
7. Sistema define organizador como responsável
8. Sistema inicializa vagas disponíveis
9. Sistema redireciona para página de detalhes do evento
10. Sistema exibe mensagem de sucesso

**Fluxos Alternativos:**

**FA01 - Usuário não é organizador:**

- No passo 1, se usuário não tem perfil de organizador:
  - Sistema exibe mensagem de erro
  - Sistema redireciona para página inicial
  - Caso de uso termina

**FA02 - Dados inválidos:**

- No passo 5, se dados forem inválidos:
  - Sistema exibe mensagens de erro específicas
  - Sistema retorna ao passo 2
  - Dados válidos são mantidos no formulário

**FA03 - Data inválida:**

- No passo 5, se data final for anterior à data inicial:
  - Sistema exibe mensagem de erro
  - Sistema retorna ao passo 2

**Pós-condições:** Novo evento criado e disponível para inscrições

---

### CU04 - Inscrever-se em Evento

**Ator Principal:** Aluno ou Professor

**Pré-condições:**

- Usuário deve estar autenticado
- Evento deve estar ativo
- Evento deve ter vagas disponíveis
- Usuário não deve estar inscrito no evento

**Fluxo Principal:**

1. Usuário visualiza detalhes do evento
2. Sistema exibe botão "Inscrever-se"
3. Usuário clica no botão
4. Sistema exibe página de confirmação de inscrição
5. Usuário pode adicionar observações (opcional)
6. Usuário confirma a inscrição
7. Sistema valida disponibilidade de vagas
8. Sistema cria registro de inscrição
9. Sistema decrementa vaga disponível do evento
10. Sistema redireciona para página do evento
11. Sistema exibe mensagem de sucesso

**Fluxos Alternativos:**

**FA01 - Usuário não autenticado:**

- No passo 1, se usuário não estiver logado:
  - Sistema exibe mensagem informativa
  - Sistema exibe botão para fazer login
  - Caso de uso termina

**FA02 - Sem vagas disponíveis:**

- No passo 7, se não houver vagas:
  - Sistema exibe mensagem de erro
  - Sistema retorna à página do evento
  - Caso de uso termina

**FA03 - Já inscrito:**

- No passo 7, se usuário já estiver inscrito:
  - Sistema exibe mensagem informativa
  - Sistema exibe opção de cancelar inscrição
  - Caso de uso termina

**FA04 - Evento inativo:**

- No passo 2, se evento estiver inativo:
  - Sistema não exibe botão de inscrição
  - Sistema exibe mensagem informativa
  - Caso de uso termina

**Pós-condições:** Usuário inscrito no evento com status "Confirmada"

---

### CU05 - Emitir Certificado

**Ator Principal:** Organizador

**Pré-condições:**

- Usuário deve estar autenticado
- Usuário deve ser o organizador do evento
- Deve existir inscrição confirmada
- Certificado não deve ter sido emitido previamente para a inscrição

**Fluxo Principal:**

1. Organizador acessa lista de inscritos do seu evento
2. Sistema exibe lista com opção de emitir certificado
3. Organizador clica em "Emitir Certificado" para um inscrito
4. Sistema exibe formulário de emissão
5. Organizador informa carga horária do evento
6. Organizador pode adicionar observações (opcional)
7. Organizador submete o formulário
8. Sistema valida os dados
9. Sistema cria certificado com código UUID único
10. Sistema registra organizador emissor e data
11. Sistema vincula certificado à inscrição
12. Sistema redireciona para visualização do certificado
13. Sistema exibe mensagem de sucesso

**Fluxos Alternativos:**

**FA01 - Não é o organizador:**

- No passo 1, se usuário não for o organizador:
  - Sistema exibe mensagem de erro
  - Sistema redireciona para página inicial
  - Caso de uso termina

**FA02 - Certificado já emitido:**

- No passo 3, se certificado já existir:
  - Sistema exibe mensagem informativa
  - Sistema redireciona para visualização do certificado existente
  - Caso de uso termina

**FA03 - Inscrição não confirmada:**

- No passo 8, se inscrição não estiver confirmada:
  - Sistema exibe mensagem de erro
  - Sistema retorna à lista de inscritos
  - Caso de uso termina

**FA04 - Dados inválidos:**

- No passo 8, se carga horária for inválida:
  - Sistema exibe mensagem de erro
  - Sistema retorna ao passo 4

**Pós-condições:** Certificado emitido e disponível para download

---

### CU06 - Verificar Certificado

**Ator Principal:** Qualquer pessoa (autenticada ou não)

**Pré-condições:** Nenhuma

**Fluxo Principal:**

1. Usuário acessa página de verificação de certificados
2. Sistema exibe formulário de verificação
3. Usuário informa código de verificação (UUID)
4. Usuário submete o formulário
5. Sistema valida formato do código
6. Sistema busca certificado no banco de dados
7. Sistema exibe informações do certificado:
   - Participante
   - Evento
   - Carga horária
   - Datas
   - Organizador
8. Sistema exibe mensagem de confirmação de autenticidade

**Fluxos Alternativos:**

**FA01 - Código inválido:**

- No passo 5, se formato do código for inválido:
  - Sistema exibe mensagem de erro
  - Sistema retorna ao passo 2
  - Caso de uso termina

**FA02 - Certificado não encontrado:**

- No passo 6, se certificado não existir:
  - Sistema exibe mensagem informando que certificado não foi encontrado
  - Sistema retorna ao passo 2
  - Caso de uso termina

**FA03 - Visualizar certificado completo:**

- No passo 8, usuário pode optar por visualizar certificado completo:
  - Sistema redireciona para página de visualização
  - Sistema exibe certificado formatado
  - Usuário pode fazer download em PDF

**Pós-condições:** Autenticidade do certificado verificada

---

## 5. Diagrama de Casos de Uso

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    SGEA - Sistema de Gestão                     │
│                  de Eventos Acadêmicos                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Visitante                                                      │
│     │                                                           │
│     ├──────> (Cadastrar-se)                                     │
│     │                                                           │
│     └──────> (Verificar Certificado)                            │
│                                                                 │
│  Usuário                                                        │
│     │                                                           │
│     ├──────> (Fazer Login)                                      │
│     │                                                           │
│     ├──────> (Buscar Eventos)                                   │
│     │                                                           │
│     ├──────> (Visualizar Evento)                                │
│     │                                                           │
│     └──────> (Gerenciar Perfil)                                 │
│                                                                 │
│  Aluno/Professor                                                │
│     │                                                           │
│     ├──────> (Inscrever-se em Evento)                           │
│     │                                                           │
│     ├──────> (Cancelar Inscrição)                               │
│     │                                                           │
│     ├──────> (Visualizar Minhas Inscrições)                     │
│     │                                                           │
│     ├──────> (Visualizar Meus Certificados)                     │
│     │                                                           │
│     └──────> (Download Certificado PDF)                         │
│                                                                 │
│  Organizador                                                    │
│     │                                                           │
│     ├──────> (Criar Evento)                                     │
│     │                                                           │
│     ├──────> (Editar Evento)                                    │
│     │                                                           │
│     ├──────> (Excluir Evento)                                   │
│     │                                                           │
│     ├──────> (Visualizar Inscritos)                             │
│     │                                                           │
│     ├──────> (Emitir Certificado)                               │
│     │                                                           │
│     └──────> (Gerenciar Meus Eventos)                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Matriz de Rastreabilidade

| Requisito | CU01 | CU02 | CU03 | CU04 | CU05 | CU06 |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- |
| RF01      | X    |      |      |      |      |      |
| RF02      |      | X    |      |      |      |      |
| RF03      |      |      | X    |      |      |      |
| RF04      |      |      | X    |      |      |      |
| RF05      |      |      |      | X    |      |      |
| RF06      |      |      |      |      | X    |      |
| RF07      |      |      |      |      | X    |      |
| RF08      |      |      |      |      |      | X    |
| RF09      |      | X    |      | X    |      |      |
| RF10      | X    |      |      |      |      |      |

---

## 7. Glossário

- **SGEA**: Sistema de Gestão de Eventos Acadêmicos
- **Evento**: Atividade acadêmica organizada (seminário, palestra, minicurso ou semana acadêmica)
- **Inscrição**: Registro de participação de um usuário em um evento
- **Certificado**: Documento digital que comprova a participação em um evento
- **UUID**: Identificador Único Universal (Universally Unique Identifier)
- **Organizador**: Usuário responsável pela criação e gerenciamento de eventos
- **Perfil**: Tipo de usuário no sistema (Aluno, Professor ou Organizador)
- **Vaga**: Posição disponível para participação em um evento
- **Carga Horária**: Duração total do evento em horas
- **Código de Verificação**: Identificador único do certificado usado para validação

---

## 8. Referências

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- ReportLab Documentation: https://www.reportlab.com/docs/
- Python PEP 8 Style Guide: https://pep8.org/

---

**Documento elaborado em:** Outubro de 2025  
**Versão:** 1.0  
**Status:** Aprovado
