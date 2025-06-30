// Add Transport Office
const officeForm = document.getElementById('officeForm');
if (officeForm) {
  officeForm.onsubmit = async function (e) {
    e.preventDefault();
    const formData = new FormData(officeForm);
    const res = await fetch('/add_office', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    alert(data.message);
  };
}

// Register Owner
const ownerForm = document.getElementById('ownerForm');
if (ownerForm) {
  ownerForm.onsubmit = async function (e) {
    e.preventDefault();
    const formData = new FormData(ownerForm);
    const res = await fetch('/add_owner', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    alert(data.message);
  };
}

// Register Vehicle
const vehicleForm = document.getElementById('vehicleForm');
if (vehicleForm) {
  vehicleForm.onsubmit = async function (e) {
    e.preventDefault();
    const formData = new FormData(vehicleForm);
    const res = await fetch('/add_vehicle', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    alert(data.message);
  };
}

// Display Owners
async function fetchOwners() {
  const officeId = document.getElementById('displayOfficeId').value;
  const formData = new FormData();
  formData.append('office_id', officeId);
  const res = await fetch('/get_owners', { method: 'POST', body: formData });
  const data = await res.json();
  const output = document.getElementById('results');
  if (data.status === 'success') {
    output.innerHTML = '<h3>Owners:</h3>' + data.owners.map(o =>
      `<p>${o.owner_id} - ${o.name} (License: ${o.license_number})</p>`).join('');
  } else {
    output.innerText = data.message;
  }
}

// Display Vehicles
async function fetchVehicles() {
  const officeId = document.getElementById('displayOfficeId').value;
  const formData = new FormData();
  formData.append('office_id', officeId);
  const res = await fetch('/get_vehicles', { method: 'POST', body: formData });
  const data = await res.json();
  const output = document.getElementById('results');
  if (data.status === 'success') {
    output.innerHTML = '<h3>Vehicles:</h3>' + data.vehicles.map(v =>
      `<p>${v.vehicle_id} - ${v.model} (Owner: ${v.owner_name})</p>`).join('');
  } else {
    output.innerText = data.message;
  }
}
