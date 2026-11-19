PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS CUSTOMERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS DESTINATIONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    description TEXT,
    base_cost NUMERIC NOT NULL CHECK (base_cost >= 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS PACKAGES (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    total_cost NUMERIC NOT NULL CHECK (total_cost >= 0),
    max_capacity INTEGER NOT NULL CHECK (max_capacity > 0),
    status TEXT NOT NULL DEFAULT 'available',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS PACKAGE_DESTINATIONS (
    package_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    display_order INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (package_id, destination_id),
    FOREIGN KEY (package_id) REFERENCES PACKAGES(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES DESTINATIONS(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS RESERVATIONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    reservation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    number_of_people INTEGER NOT NULL CHECK (number_of_people > 0),
    total_price NUMERIC NOT NULL CHECK (total_price >= 0),
    status TEXT NOT NULL DEFAULT 'confirmed',
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(id) ON DELETE RESTRICT,
    FOREIGN KEY (package_id) REFERENCES PACKAGES(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_reservations_customer ON RESERVATIONS(customer_id);
CREATE INDEX IF NOT EXISTS idx_reservations_package ON RESERVATIONS(package_id);
CREATE INDEX IF NOT EXISTS idx_package_destinations_destination ON PACKAGE_DESTINATIONS(destination_id);
