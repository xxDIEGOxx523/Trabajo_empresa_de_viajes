from typing import List, Optional
from src.domain.destination import Destination
from src.persistence.database import DatabaseConnection


class DestinationDAO:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        self.ph = db.get_placeholder()

    def _row_to_entity(self, row) -> Destination:
        if isinstance(row, dict):
            return Destination(
                id=row["id"],
                name=row["name"],
                country=row["country"],
                description=row["description"] or "",
                base_cost=float(row["base_cost"]),
                is_active=bool(row["is_active"]),
            )
        return Destination(
            id=row[0],
            name=row[1],
            country=row[2],
            description=row[3] or "",
            base_cost=float(row[4]),
            is_active=bool(row[5]),
        )

    def create(self, destination: Destination) -> Destination:
        query = f"""
            INSERT INTO destinations (name, country, description, base_cost, is_active)
            VALUES ({self.ph}, {self.ph}, {self.ph}, {self.ph}, {self.ph})
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    destination.name,
                    destination.country,
                    destination.description,
                    destination.base_cost,
                    1 if destination.is_active else 0,
                ),
            )
            conn.commit()
            destination.id = cursor.lastrowid
            return destination
        finally:
            conn.close()

    def get_all(self, include_retired: bool = False) -> List[Destination]:
        query = (
            "SELECT id, name, country, description, base_cost, is_active "
            "FROM destinations"
        )
        if not include_retired:
            query += " WHERE is_active = 1"
        query += " ORDER BY id ASC"

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
        finally:
            conn.close()

    def get_by_id(self, destination_id: int) -> Optional[Destination]:
        query = f"""
            SELECT id, name, country, description, base_cost, is_active
            FROM destinations
            WHERE id = {self.ph}
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (destination_id,))
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
        finally:
            conn.close()

    def search(self, term: str, include_retired: bool = True) -> List[Destination]:
        pattern = f"%{term.strip()}%"
        query = f"""
            SELECT id, name, country, description, base_cost, is_active
            FROM destinations
            WHERE (LOWER(name) LIKE LOWER({self.ph}) OR LOWER(country) LIKE LOWER({self.ph}))
        """
        if not include_retired:
            query += " AND is_active = 1"
        query += " ORDER BY id ASC"

        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (pattern, pattern))
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
        finally:
            conn.close()

    def update(self, destination: Destination) -> bool:
        query = f"""
            UPDATE destinations
            SET name = {self.ph},
                country = {self.ph},
                description = {self.ph},
                base_cost = {self.ph},
                is_active = {self.ph}
            WHERE id = {self.ph}
        """
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    destination.name,
                    destination.country,
                    destination.description,
                    destination.base_cost,
                    1 if destination.is_active else 0,
                    destination.id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def set_active_status(self, destination_id: int, is_active: bool) -> bool:
        query = f"UPDATE destinations SET is_active = {self.ph} WHERE id = {self.ph}"
        conn = self.db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (1 if is_active else 0, destination_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
