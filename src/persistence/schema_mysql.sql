-- ==========================================================
-- Physical Model v2 - Viajes Aventura (MySQL 5.7+ / MariaDB / WampServer)
-- Compatible with utf8mb4_unicode_ci and 767-byte index limits
-- ==========================================================
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS viajes_aventura
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE viajes_aventura;

CREATE TABLE IF NOT EXISTS destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(90) NOT NULL,
    country VARCHAR(90) NOT NULL,
    description TEXT,
    base_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_destination_name_country (name, country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS travel_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS itinerary_stops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    destination_id INT NOT NULL,
    visit_order INT NOT NULL,
    FOREIGN KEY (package_id) REFERENCES travel_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES destinations(id),
    UNIQUE KEY uq_package_order (package_id, visit_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS package_departures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    max_capacity INT NOT NULL,
    status ENUM('OPEN', 'CLOSED', 'CANCELLED') NOT NULL DEFAULT 'OPEN',
    FOREIGN KEY (package_id) REFERENCES travel_packages(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('CLIENT', 'ADMIN') NOT NULL DEFAULT 'CLIENT'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    departure_id INT NOT NULL,
    reserved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contracted_unit_price DECIMAL(10, 2) NOT NULL,
    status ENUM('PENDING', 'CONFIRMED', 'CANCELLED') NOT NULL DEFAULT 'CONFIRMED',
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (departure_id) REFERENCES package_departures(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reservation_passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    passenger_name VARCHAR(150) NOT NULL,
    document_id VARCHAR(50) NOT NULL,
    trip_status ENUM('PENDING', 'TRAVELING', 'COMPLETED') NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS passenger_stage_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT NOT NULL,
    stop_id INT NOT NULL,
    stage_status ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED') NOT NULL DEFAULT 'PENDING',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by_admin_id INT,
    FOREIGN KEY (passenger_id) REFERENCES reservation_passengers(id) ON DELETE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES itinerary_stops(id),
    FOREIGN KEY (updated_by_admin_id) REFERENCES customers(id),
    UNIQUE KEY uq_passenger_stop (passenger_id, stop_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
