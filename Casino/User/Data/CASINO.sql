CREATE DATABASE CASINO;
USE CASINO;

CREATE TABLE user (
ID_USER INT PRIMARY KEY AUTO_INCREMENT,
USERNAME VARCHAR(25),
Password VARCHAR(12),
SCORE INT NOT NULL DEFAULT 50,
chip5_chips INT NOT NULL DEFAULT 0,
chip10_chips INT NOT NULL DEFAULT 0,
chip50_chips INT NOT NULL DEFAULT 0,
chip100_chips INT NOT NULL DEFAULT 0,
chip500_chips INT NOT NULL DEFAULT 0,
chip1000_chips INT NOT NULL DEFAULT 0,
chip5000_chips INT NOT NULL DEFAULT 0);
