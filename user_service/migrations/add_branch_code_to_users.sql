-- Migración: Agregar columna branch_code a la tabla users
-- Fecha: 2025-01-27
-- Descripción: Agregar campo para código de sucursal en usuarios

-- Agregar la nueva columna
ALTER TABLE users ADD COLUMN branch_code VARCHAR(20);

-- Crear índice para mejorar el rendimiento de consultas por branch_code
CREATE INDEX idx_users_branch_code ON users(branch_code);

-- Comentario en la columna
COMMENT ON COLUMN users.branch_code IS 'Código de sucursal del usuario';
