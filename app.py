from flask import Flask, render_template, request, jsonify

# ---------------------------
# Data Classes
# ---------------------------

class TransportDepartment:
    def __init__(self, department_name):
        self.department_name = department_name

    def add_vehicle(self, vehicle):
        raise NotImplementedError

    def add_owner(self, owner):
        raise NotImplementedError

class Person:
    def __init__(self, owner_id, name):
        self.owner_id = owner_id
        self.name = name

class Owner(Person):
    def __init__(self, owner_id, name, license_number):
        super().__init__(owner_id, name)
        self.license_number = license_number

class Vehicle:
    def __init__(self, vehicle_id, model, owner_name):
        self.vehicle_id = vehicle_id
        self.model = model
        self.owner_name = owner_name

class TransportOffice(TransportDepartment):
    def __init__(self, office_id, office_name):
        super().__init__("State Vehicle Registration Department")
        self.office_id = office_id
        self.office_name = office_name
        self.vehicles = []
        self.owners = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_owner(self, owner):
        self.owners.append(owner)

# ---------------------------
# Flask App
# ---------------------------

app = Flask(__name__)
transport_offices = {}

# ---------------------------
# Page Routes
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_office_page')
def add_office_page():
    return render_template('add_office.html')

@app.route('/register_owner_page')
def register_owner_page():
    return render_template('register_owner.html')

@app.route('/register_vehicle_page')
def register_vehicle_page():
    return render_template('register_vehicle.html')

@app.route('/display_data_page')
def display_data_page():
    return render_template('display_data.html')

# ---------------------------
# API Endpoints
# ---------------------------

@app.route('/add_office', methods=['POST'])
def add_office():
    office_id = request.form['office_id']
    office_name = request.form['office_name']
    if office_id in transport_offices:
        return jsonify({'status': 'error', 'message': 'Office ID already exists'})
    office = TransportOffice(office_id, office_name)
    transport_offices[office_id] = office
    return jsonify({'status': 'success', 'message': f'Office {office_name} added.'})

@app.route('/add_owner', methods=['POST'])
def add_owner():
    office_id = request.form['office_id']
    owner_id = request.form['owner_id']
    name = request.form['name']
    license_number = request.form['license_number']
    office = transport_offices.get(office_id)
    if office:
        owner = Owner(owner_id, name, license_number)
        office.add_owner(owner)
        return jsonify({'status': 'success', 'message': f'Owner {name} added.'})
    else:
        return jsonify({'status': 'error', 'message': 'Office not found.'})

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    office_id = request.form['office_id']
    vehicle_id = request.form['vehicle_id']
    model = request.form['model']
    owner_name = request.form['owner_name']
    office = transport_offices.get(office_id)
    if office:
        vehicle = Vehicle(vehicle_id, model, owner_name)
        office.add_vehicle(vehicle)
        return jsonify({'status': 'success', 'message': f'Vehicle {vehicle_id} added.'})
    else:
        return jsonify({'status': 'error', 'message': 'Office not found.'})

@app.route('/get_owners', methods=['POST'])
def get_owners():
    office_id = request.form['office_id']
    office = transport_offices.get(office_id)
    if office:
        owners = [{'owner_id': o.owner_id, 'name': o.name, 'license_number': o.license_number} for o in office.owners]
        return jsonify({'status': 'success', 'owners': owners})
    else:
        return jsonify({'status': 'error', 'message': 'Office not found.'})

@app.route('/get_vehicles', methods=['POST'])
def get_vehicles():
    office_id = request.form['office_id']
    office = transport_offices.get(office_id)
    if office:
        vehicles = [{'vehicle_id': v.vehicle_id, 'model': v.model, 'owner_name': v.owner_name} for v in office.vehicles]
        return jsonify({'status': 'success', 'vehicles': vehicles})
    else:
        return jsonify({'status': 'error', 'message': 'Office not found.'})

# ---------------------------
# Run the App
# ---------------------------

if __name__ == '__main__':
    app.run(debug=True)
