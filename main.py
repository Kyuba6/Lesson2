from pydantic import BaseModel
from typing import Dict

import json


class Parameters(BaseModel):
    apartments_json_path: str = 'data/apartments.json'
    tenants_json_path: str = 'data/tenants.json'


class Room(BaseModel):
    name: str
    area_m2: float


class Apartment(BaseModel):
    key: str
    name: str
    location: str
    area_m2: float
    rooms: Dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Apartment']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}

    
class Tenant(BaseModel):
    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Tenant']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}
    

class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)

class Bill:
    def __init__(self, kwota, date, type, apartment):
        self.kwota=kwota
        self.date=date
        self.type=type
        self.apartment=apartment

    def __repr__(self):
        return f"Bill({self.kwota}, {self.date}, {self.type}, {self.apartment})"

def load_bills(filename):
    with open(filename, 'r') as file:
        bills_data=json.load(file)
        bills=[]
        for bill_data in bills_data:
            bill=Bill(
                bill_data['kwota'],
                datetime.strptime(bill_data['date'], '%Y-%m-%d'),
                bill_data['type'],
                bill_data['apartment']
            )
            bills.append(bill)
        return bills

bills = load_bills('bills.json')
for bill in bills:
    print(bill)

if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    for apartment in manager.apartments.values():
        print(apartment.key, apartment.name, apartment.location, apartment.area_m2)
        for room in apartment.rooms.values():
            print('  ', room.name, room.area_m2)

    for tenant in manager.tenants.values():
        print(tenant.name, tenant.apartment, tenant.room, tenant.rent_pln, tenant.deposit_pln, tenant.date_agreement_from, tenant.date_agreement_to)
    