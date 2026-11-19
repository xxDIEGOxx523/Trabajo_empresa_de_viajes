CREATE TABLE IF NOT EXISTS CUSTOMERS (
    id INT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(190) NOT NULL UNIQUE,
    phone VARCHAR(30),
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS DESTINATIONS (
    id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    description TEXT,
    base_cost DECIMAL(12,2) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS PACKAGES (
    id INT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_cost DECIMAL(12,2) NOT NULL,
    max_capacity INT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'available',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS PACKAGE_DESTINATIONS (
    package_id INT NOT NULL,
    destination_id INT NOT NULL,
    display_order INT NOT NULL DEFAULT 1,
    PRIMARY KEY (package_id, destination_id),
    CONSTRAINT fk_pd_package FOREIGN KEY (package_id) REFERENCES PACKAGES(id) ON DELETE CASCADE,
    CONSTRAINT fk_pd_destination FOREIGN KEY (destination_id) REFERENCES DESTINATIONS(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS RESERVATIONS (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    package_id INT NOT NULL,
    reservation_date DATETIME NOT NULL,
    number_of_people INT NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'confirmed',
    CONSTRAINT fk_res_customer FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(id) ON DELETE RESTRICT,
    CONSTRAINT fk_res_package FOREIGN KEY (package_id) REFERENCES PACKAGES(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_reservations_customer ON RESERVATIONS(customer_id);
CREATE INDEX idx_reservations_package ON RESERVATIONS(package_id);
CREATE INDEX idx_package_destinations_destination ON PACKAGE_DESTINATIONS(destination_id);
