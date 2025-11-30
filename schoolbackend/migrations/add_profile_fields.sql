-- Migración para agregar campos de perfil del profesor
-- Ejecutar este script en tu base de datos MySQL

ALTER TABLE users 
ADD COLUMN description TEXT NULL AFTER is_active,
ADD COLUMN photo_url VARCHAR(500) NULL AFTER description;

