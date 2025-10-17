-- ============================================================================
-- SGEA - Sistema de Gestão de Eventos Acadêmicos
-- Script de Criação e População do Banco de Dados
-- 
-- Desenvolvido por:
--   • Ana Júlia Moura - RA: 22403137
--   • Vinicius Martin - RA: 22402759
-- 
-- Instituição: Centro Universitário de Brasília (UniCEUB)
-- Ano: 2025
-- 
-- SGBD: SQLite3 / PostgreSQL
-- Versão: 1.0
-- Data: Outubro 2025
-- ============================================================================

-- ============================================================================
-- 1. CRIAÇÃO DAS TABELAS
-- ============================================================================

-- Tabela: users_customuser
-- Descrição: Armazena informações dos usuários do sistema
CREATE TABLE users_customuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    telefone VARCHAR(15) NULL,
    instituicao_ensino VARCHAR(200) NULL,
    perfil VARCHAR(15) NOT NULL DEFAULT 'ALUNO' CHECK (perfil IN ('ALUNO', 'PROFESSOR', 'ORGANIZADOR')),
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices para users_customuser
CREATE INDEX idx_user_perfil ON users_customuser(perfil);
CREATE INDEX idx_user_cadastro ON users_customuser(data_cadastro);
CREATE INDEX idx_user_email ON users_customuser(email);

-- ============================================================================

-- Tabela: events_event
-- Descrição: Armazena informações dos eventos acadêmicos
CREATE TABLE events_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    tipo_evento VARCHAR(20) NOT NULL CHECK (tipo_evento IN ('SEMINARIO', 'PALESTRA', 'MINICURSO', 'SEMANA_ACADEMICA')),
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    local VARCHAR(200) NOT NULL,
    vagas INTEGER NOT NULL CHECK (vagas > 0),
    vagas_disponiveis INTEGER NOT NULL CHECK (vagas_disponiveis >= 0),
    organizador_id INTEGER NOT NULL,
    imagem VARCHAR(100) NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizador_id) REFERENCES users_customuser(id) ON DELETE RESTRICT,
    CHECK (data_fim >= data_inicio)
);

-- Índices para events_event
CREATE INDEX idx_event_tipo ON events_event(tipo_evento);
CREATE INDEX idx_event_ativo ON events_event(ativo);
CREATE INDEX idx_event_data_inicio ON events_event(data_inicio);
CREATE INDEX idx_event_criacao ON events_event(data_criacao);
CREATE INDEX idx_event_organizador ON events_event(organizador_id);

-- ============================================================================

-- Tabela: events_inscription
-- Descrição: Armazena as inscrições dos usuários nos eventos
CREATE TABLE events_inscription (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'CONFIRMADA' CHECK (status IN ('PENDENTE', 'CONFIRMADA', 'CANCELADA')),
    data_inscricao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT NULL,
    FOREIGN KEY (evento_id) REFERENCES events_event(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES users_customuser(id) ON DELETE CASCADE,
    UNIQUE (evento_id, usuario_id)
);

-- Índices para events_inscription
CREATE INDEX idx_inscription_status ON events_inscription(status);
CREATE INDEX idx_inscription_data ON events_inscription(data_inscricao);
CREATE INDEX idx_inscription_evento ON events_inscription(evento_id);
CREATE INDEX idx_inscription_usuario ON events_inscription(usuario_id);

-- ============================================================================

-- Tabela: certificates_certificate
-- Descrição: Armazena os certificados emitidos
CREATE TABLE certificates_certificate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inscricao_id INTEGER NOT NULL UNIQUE,
    codigo_verificacao VARCHAR(36) NOT NULL UNIQUE,
    data_emissao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    emitido_por_id INTEGER NOT NULL,
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0),
    observacoes TEXT NULL,
    FOREIGN KEY (inscricao_id) REFERENCES events_inscription(id) ON DELETE RESTRICT,
    FOREIGN KEY (emitido_por_id) REFERENCES users_customuser(id) ON DELETE RESTRICT
);

-- Índices para certificates_certificate
CREATE INDEX idx_certificate_emissao ON certificates_certificate(data_emissao);
CREATE INDEX idx_certificate_emissor ON certificates_certificate(emitido_por_id);
CREATE INDEX idx_certificate_codigo ON certificates_certificate(codigo_verificacao);

-- ============================================================================
-- 2. POPULAÇÃO INICIAL DO BANCO DE DADOS
-- ============================================================================

-- Inserir usuários de exemplo
-- Nota: As senhas são hashes para 'senha123' usando Django PBKDF2
-- Em produção, use manage.py createsuperuser para criar usuários reais

-- Organizadores
INSERT INTO users_customuser (
    username, password, first_name, last_name, email, 
    telefone, instituicao_ensino, perfil, is_staff, is_superuser
) VALUES 
(
    'admin',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Administrador',
    'Sistema',
    'admin@sgea.edu.br',
    '11987654321',
    'SGEA',
    'ORGANIZADOR',
    1,
    1
),
(
    'organizador1',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Maria',
    'Silva',
    'maria.silva@sgea.edu.br',
    '11987654322',
    'Universidade Federal',
    'ORGANIZADOR',
    0,
    0
),
(
    'organizador2',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Carlos',
    'Santos',
    'carlos.santos@sgea.edu.br',
    '11987654323',
    'Instituto de Tecnologia',
    'ORGANIZADOR',
    0,
    0
);

-- Professores
INSERT INTO users_customuser (
    username, password, first_name, last_name, email,
    telefone, instituicao_ensino, perfil
) VALUES
(
    'prof1',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'João',
    'Oliveira',
    'joao.oliveira@universidade.edu.br',
    '11987654324',
    'Universidade Estadual',
    'PROFESSOR'
),
(
    'prof2',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Ana',
    'Costa',
    'ana.costa@universidade.edu.br',
    '11987654325',
    'Universidade Federal',
    'PROFESSOR'
);

-- Alunos
INSERT INTO users_customuser (
    username, password, first_name, last_name, email,
    telefone, instituicao_ensino, perfil
) VALUES
(
    'aluno1',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Pedro',
    'Almeida',
    'pedro.almeida@estudante.edu.br',
    '11987654326',
    'Universidade Federal',
    'ALUNO'
),
(
    'aluno2',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Julia',
    'Ferreira',
    'julia.ferreira@estudante.edu.br',
    '11987654327',
    'Universidade Estadual',
    'ALUNO'
),
(
    'aluno3',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Lucas',
    'Rodrigues',
    'lucas.rodrigues@estudante.edu.br',
    '11987654328',
    'Instituto de Tecnologia',
    'ALUNO'
),
(
    'aluno4',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Beatriz',
    'Lima',
    'beatriz.lima@estudante.edu.br',
    '11987654329',
    'Universidade Federal',
    'ALUNO'
),
(
    'aluno5',
    'pbkdf2_sha256$600000$placeholder$hashplaceholder',
    'Rafael',
    'Sousa',
    'rafael.sousa@estudante.edu.br',
    '11987654330',
    'Universidade Estadual',
    'ALUNO'
);

-- ============================================================================

-- Inserir eventos de exemplo
INSERT INTO events_event (
    titulo, descricao, tipo_evento, data_inicio, data_fim,
    horario_inicio, horario_fim, local, vagas, vagas_disponiveis,
    organizador_id, ativo
) VALUES
(
    'Seminário de Inteligência Artificial 2024',
    'Seminário abordando os últimos avanços em IA, Machine Learning e Deep Learning. Palestrantes renomados da área compartilharão suas experiências e pesquisas.',
    'SEMINARIO',
    '2024-11-15',
    '2024-11-17',
    '09:00',
    '18:00',
    'Auditório Central - Campus Principal',
    100,
    85,
    2,
    1
),
(
    'Palestra: O Futuro da Computação Quântica',
    'Palestra introdutória sobre computação quântica, suas aplicações práticas e o impacto esperado na indústria nos próximos anos.',
    'PALESTRA',
    '2024-11-20',
    '2024-11-20',
    '14:00',
    '16:00',
    'Sala de Conferências 1',
    50,
    45,
    2,
    1
),
(
    'Minicurso: Desenvolvimento Web com Django',
    'Minicurso prático de 3 dias sobre desenvolvimento de aplicações web usando o framework Django. Inclui projeto hands-on.',
    'MINICURSO',
    '2024-11-25',
    '2024-11-27',
    '08:00',
    '12:00',
    'Laboratório de Informática 3',
    30,
    18,
    3,
    1
),
(
    'Semana Acadêmica de Ciência da Computação 2024',
    'Evento completo com palestras, workshops, minicursos e competições de programação. Uma semana inteira dedicada à tecnologia e inovação.',
    'SEMANA_ACADEMICA',
    '2024-12-02',
    '2024-12-06',
    '08:00',
    '20:00',
    'Campus Central - Múltiplos Espaços',
    200,
    150,
    2,
    1
),
(
    'Palestra: Cibersegurança e Proteção de Dados',
    'Discussão sobre os desafios atuais em cibersegurança, LGPD e melhores práticas para proteção de dados pessoais e corporativos.',
    'PALESTRA',
    '2024-12-10',
    '2024-12-10',
    '19:00',
    '21:00',
    'Auditório do Instituto de Tecnologia',
    80,
    80,
    3,
    1
),
(
    'Minicurso: Python para Ciência de Dados',
    'Minicurso focado em análise de dados usando Python, pandas, numpy e visualização com matplotlib e seaborn.',
    'MINICURSO',
    '2024-12-15',
    '2024-12-16',
    '09:00',
    '17:00',
    'Laboratório de Computação Científica',
    25,
    20,
    2,
    1
);

-- ============================================================================

-- Inserir inscrições de exemplo
INSERT INTO events_inscription (
    evento_id, usuario_id, status, observacoes
) VALUES
-- Inscrições no Seminário de IA (evento 1)
(1, 4, 'CONFIRMADA', 'Interesse em Deep Learning'),
(1, 5, 'CONFIRMADA', NULL),
(1, 6, 'CONFIRMADA', 'Primeira participação em eventos acadêmicos'),
(1, 7, 'CONFIRMADA', NULL),
(1, 8, 'CONFIRMADA', 'Desenvolvo pesquisa na área'),

-- Inscrições na Palestra de Computação Quântica (evento 2)
(2, 6, 'CONFIRMADA', NULL),
(2, 7, 'CONFIRMADA', 'Muito interessado no tema'),
(2, 8, 'CONFIRMADA', NULL),
(2, 9, 'CONFIRMADA', NULL),
(2, 10, 'CONFIRMADA', NULL),

-- Inscrições no Minicurso de Django (evento 3)
(3, 6, 'CONFIRMADA', 'Já tenho conhecimento básico de Python'),
(3, 7, 'CONFIRMADA', NULL),
(3, 8, 'CONFIRMADA', 'Quero aprender desenvolvimento web'),
(3, 9, 'CONFIRMADA', NULL),
(3, 10, 'CONFIRMADA', 'Desenvolvedor iniciante'),
(3, 4, 'CONFIRMADA', 'Interesse em expandir conhecimentos'),

-- Inscrições na Semana Acadêmica (evento 4)
(4, 4, 'CONFIRMADA', 'Participarei de todas as atividades'),
(4, 5, 'CONFIRMADA', NULL),
(4, 6, 'CONFIRMADA', 'Interesse especial nas competições'),
(4, 7, 'CONFIRMADA', NULL),
(4, 8, 'CONFIRMADA', 'Primeira vez na Semana Acadêmica'),
(4, 9, 'CONFIRMADA', NULL),
(4, 10, 'CONFIRMADA', 'Muito animado para participar');

-- ============================================================================

-- Inserir certificados de exemplo
-- Nota: UUIDs devem ser gerados pelo sistema Django
-- Aqui usamos exemplos fixos apenas para demonstração
INSERT INTO certificates_certificate (
    inscricao_id, codigo_verificacao, emitido_por_id, carga_horaria, observacoes
) VALUES
-- Certificados do Seminário de IA
(1, '550e8400-e29b-41d4-a716-446655440001', 2, 24, 'Participação integral com presença mínima de 75%'),
(2, '550e8400-e29b-41d4-a716-446655440002', 2, 24, NULL),
(3, '550e8400-e29b-41d4-a716-446655440003', 2, 24, 'Excelente participação'),

-- Certificados da Palestra de Computação Quântica
(6, '550e8400-e29b-41d4-a716-446655440004', 2, 2, NULL),
(7, '550e8400-e29b-41d4-a716-446655440005', 2, 2, NULL),

-- Certificados do Minicurso de Django
(11, '550e8400-e29b-41d4-a716-446655440006', 3, 12, 'Completou projeto prático'),
(12, '550e8400-e29b-41d4-a716-446655440007', 3, 12, 'Desempenho exemplar'),
(13, '550e8400-e29b-41d4-a716-446655440008', 3, 12, NULL);

-- ============================================================================
-- 3. CONSULTAS ÚTEIS PARA VERIFICAÇÃO
-- ============================================================================

-- Listar todos os eventos com seus organizadores
-- SELECT 
--     e.id,
--     e.titulo,
--     e.tipo_evento,
--     e.data_inicio,
--     e.vagas,
--     e.vagas_disponiveis,
--     u.first_name || ' ' || u.last_name AS organizador
-- FROM events_event e
-- JOIN users_customuser u ON e.organizador_id = u.id
-- ORDER BY e.data_inicio;

-- Listar inscrições por evento
-- SELECT 
--     e.titulo AS evento,
--     COUNT(i.id) AS total_inscritos,
--     e.vagas AS vagas_totais,
--     e.vagas_disponiveis
-- FROM events_event e
-- LEFT JOIN events_inscription i ON e.id = i.evento_id AND i.status = 'CONFIRMADA'
-- GROUP BY e.id, e.titulo, e.vagas, e.vagas_disponiveis
-- ORDER BY total_inscritos DESC;

-- Listar certificados emitidos
-- SELECT 
--     c.codigo_verificacao,
--     u.first_name || ' ' || u.last_name AS participante,
--     e.titulo AS evento,
--     c.carga_horaria,
--     c.data_emissao
-- FROM certificates_certificate c
-- JOIN events_inscription i ON c.inscricao_id = i.id
-- JOIN users_customuser u ON i.usuario_id = u.id
-- JOIN events_event e ON i.evento_id = e.id
-- ORDER BY c.data_emissao DESC;

-- Estatísticas gerais do sistema
-- SELECT 
--     'Usuários Cadastrados' AS metrica,
--     COUNT(*) AS total
-- FROM users_customuser
-- UNION ALL
-- SELECT 'Eventos Criados', COUNT(*) FROM events_event
-- UNION ALL
-- SELECT 'Inscrições Confirmadas', COUNT(*) FROM events_inscription WHERE status = 'CONFIRMADA'
-- UNION ALL
-- SELECT 'Certificados Emitidos', COUNT(*) FROM certificates_certificate;

-- ============================================================================
-- FIM DO SCRIPT
-- ============================================================================

-- OBSERVAÇÕES:
-- 1. Este script é compatível com SQLite3 (usado no desenvolvimento)
-- 2. Para PostgreSQL, substitua AUTOINCREMENT por SERIAL
-- 3. As senhas precisam ser geradas pelo Django usando manage.py createsuperuser
-- 4. Os UUIDs devem ser gerados automaticamente pelo Django
-- 5. Execute as migrações Django após criar as tabelas:
--    python manage.py makemigrations
--    python manage.py migrate
-- 6. Para popular o banco, use fixtures Django ou o Django Admin

