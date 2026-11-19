"""Modelo inicial de cliente."""


class Customer:
    def __init__(self, full_name: str, email: str, phone: str = ""):
        self.full_name = full_name
        self.email = email
        self.phone = phone
