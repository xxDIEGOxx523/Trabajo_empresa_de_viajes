-- ==========================================================
-- Physical Model v2 - Viajes Aventura (SQLite)
-- ==========================================================
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    description TEXT DEFAULT '',
    base_cost REAL NOT NULL DEFAULT 0.0 CHECK (base_cost >= 0),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(name, country)
);

CREATE TABLE IF NOT EXISTS travel_packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS itinerary_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    visit_order INTEGER NOT NULL CHECK (visit_order > 0),
    FOREIGN KEY (package_id) REFERENCES travel_packages(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES destinations(id),
    UNIQUE(package_id, visit_order)
);

CREATE TABLE IF NOT EXISTS package_departures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    max_capacity INTEGER NOT NULL CHECK (max_capacity > 0),
    status TEXT NOT NULL DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED', 'CANCELLED')),
    FOREIGN KEY (package_id) REFERENCES travel_packages(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'CLIENT' CHECK (role IN ('CLIENT', 'ADMIN'))
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    departure_id INTEGER NOT NULL,
    reserved_at TEXT NOT NULL DEFAULT (datetime('now')),
    contracted_unit_price REAL NOT NULL CHECK (contracted_unit_price >= 0),
    status TEXT NOT NULL DEFAULT 'CONFIRMED' CHECK (status IN ('PENDING', 'CONFIRMED', 'CANCELLED')),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (departure_id) REFERENCES package_departures(id)
);

CREATE TABLE IF NOT EXISTS reservation_passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    document_id TEXT NOT NULL,
    trip_status TEXT NOT NULL DEFAULT 'PENDING' CHECK (trip_status IN ('PENDING', 'TRAVELING', 'COMPLETED')),
    FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS passenger_stage_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER NOT NULL,
    stop_id INTEGER NOT NULL,
    stage_status TEXT NOT NULL DEFAULT 'PENDING' CHECK (stage_status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_by_admin_id INTEGER,
    FOREIGN KEY (passenger_id) REFERENCES reservation_passengers(id) ON DELETE CASCADE,
    FOREIGN KEY (stop_id) REFERENCES itinerary_stops(id),
    FOREIGN KEY (updated_by_admin_id) REFERENCES customers(id),
    UNIQUE(passenger_id, stop_id)
);
