"""Modelo inicial de reserva."""


class Reservation:
    def __init__(self, customer_id: int, package_id: int, number_of_people: int):
        self.customer_id = customer_id
        self.package_id = package_id
        self.number_of_people = number_of_people
