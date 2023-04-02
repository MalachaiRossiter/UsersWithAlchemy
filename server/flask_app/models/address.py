from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

DB = "test_schema"

class Address:
    def __init__(self, address):
        self.id = address['id']
        self.address = address['address']
        self.city = address['city']
        self.state = address['state']

    #create new address
    @classmethod
    def create_address(cls, address):
        
        parsed_data = {
            'address' : address['address'],
            'city' : address['city'],
            'state' : address['state']
        }
        query = 'INSERT INTO addresses (address, city, state) VALUES (%(address)s, %(city)s, %(state)s)'
        new_address = connectToMySQL(DB).query_db(query,parsed_data)
        address_id = cls.get_id(new_address)
        print('address_id: ', address_id)
        return address_id
    
    #turns object into dictionary
    def to_dict(self):
        return {
            'address': self.address,
            'city': self.city,
            'state': self.state
        }

    # get all addresses for a given list of IDs
    @classmethod
    def get_all_for_ids(cls, ids):
        query = "SELECT * FROM addresses WHERE id IN %(ids)s"
        data = {'ids': tuple(ids)}
        results = connectToMySQL(DB).query_db(query, data)
        return [cls(result) for result in results]

    #get address by id
    @classmethod
    def get_id(cls, address_id):
        data = {'id': address_id}
        query = 'SELECT * FROM addresses WHERE id = %(id)s'
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])
    
    #get all addresses
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM test_schema.addresses;"
        result = connectToMySQL(DB).query_db(query)
        
        addresses = []
        for address_dict in result:
            address = cls(address_dict)
            addresses.append(address)

        return addresses
    