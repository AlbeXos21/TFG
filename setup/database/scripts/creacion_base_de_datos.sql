-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS reviews;

-- Seleccionar la base de datos para usarla
USE reviews;

-- Crear la tabla 'productos'
CREATE TABLE `productos` (
  `IDAPP` int NOT NULL,
  `NOMBRE` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ESTADO` tinyint(1) NOT NULL DEFAULT '0',
  `MEDIA` float DEFAULT NULL,
  `FECHA` datetime DEFAULT NULL,
  `RESUMEN` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `GENEROS` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '000000',
  PRIMARY KEY (`IDAPP`)
)

-- Crear la tabla 'reseñas' con clave foránea correcta
CREATE TABLE `reseñas` (
  `IDRESEÑA` int NOT NULL AUTO_INCREMENT,
  `IDPRODUCTO` int NOT NULL,
  `RESEÑA` text NOT NULL,
  `CALIFICACION` int DEFAULT NULL,
  `TIPO` int NOT NULL,
  PRIMARY KEY (`IDRESEÑA`),
  KEY `IDPRODUCTO` (`IDPRODUCTO`),
  CONSTRAINT `reseñas_ibfk_1` FOREIGN KEY (`IDPRODUCTO`) REFERENCES `productos` (`IDAPP`) ON DELETE CASCADE
)