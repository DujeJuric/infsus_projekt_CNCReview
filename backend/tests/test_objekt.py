import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app


client = TestClient(app)


@pytest.fixture
def create_admin():
    response = client.post("/admin/createAdmin", json={
        "lozinka": "admin123",
        "email": "test_admin@gmail.com",
    })
    assert response.status_code == 200
    print("Admin created with ID:", response.json()["admin_id"])
    return response.json()["admin_id"]


@pytest.fixture
def create_vlasnik():
    response = client.post("/vlasnik/createVlasnik", json={
        "lozinka": "vlasnik123",
        "email": "test_vlasnik@gmail.com",
        "naziv": "Test Vlasnik",
    })
    assert response.status_code == 200
    print("Vlasnik created with ID:", response.json()["vlasnik_id"])
    return response.json()["vlasnik_id"]


@pytest.fixture
def create_grad():
    response = client.post("/grad/createGrad", json={"naziv": "Test Grad"})
    assert response.status_code == 200
    print("Grad created with ID:", response.json()["grad_id"])
    return response.json()["grad_id"]


@pytest.fixture
def create_vlasnistvo(create_vlasnik, create_admin):
    response = client.post("/vlasnistvo/createVlasnistvo", json={
        "vlasnik_id": create_vlasnik,
        "admin_id": create_admin,
    })
    assert response.status_code == 200
    print("Vlasnistvo created with ID:", response.json()["vlasnistvo_id"])
    return response.json()["vlasnistvo_id"]


def test_create_edit_delete_objekt(create_admin, create_vlasnik, create_vlasnistvo, create_grad):
    print("Starting test for Objekt creation, editing, and deletion")
    # Create objekt
    response = client.post("/objekt/createObjekt", json={
        "naziv": "Test Objekt",
        "adresa": "Test Adresa",
        "opis": "Test Opis",
        "radno_vrijeme": "09:00-17:00",
        "radni_dani": "Ponedjeljak-Petak",
        "mobilni_broj": "+1234567890",
        "vlasnistvo_id": create_vlasnistvo,
        "grad_id": create_grad,
    })
    assert response.status_code == 200
    print("Objekt created with ID:", response.json()["objekt_id"])
    objekt = response.json()
    objekt_id = objekt["objekt_id"]

    # Get objekt
    get_resp = client.get(f"/objekt/getObjektById/{objekt_id}")
    assert get_resp.status_code == 200
    print("Objekt retrieved:", get_resp.json())

    # Update objekt
    new_name = "Updated Objekt"
    edit_resp = client.post(f"/objekt/editObjekt/{objekt_id}", json={
        "naziv": new_name,
        "adresa": objekt["adresa"],
        "opis": objekt["opis"],
        "radno_vrijeme": objekt["radno_vrijeme"],
        "radni_dani": objekt["radni_dani"],
        "mobilni_broj": objekt["mobilni_broj"],
        "vlasnistvo_id": create_vlasnistvo,
        "grad_id": create_grad,
    })
    assert edit_resp.status_code == 200
    print("Objekt updated:", edit_resp.json())
    assert edit_resp.json()["naziv"] == new_name

    # Delete objekt
    del_resp = client.delete(f"/objekt/deleteObjekt/{objekt_id}")
    assert del_resp.status_code == 200
    print("Objekt deleted successfully")

    # Check objekt deleted
    not_found = client.get(f"/objekt/getObjektById/{objekt_id}")
    assert not_found.status_code == 404
    print("Objekt not found after deletion:", not_found.json())

    # Cleanup
    client.delete(f"/vlasnistvo/deleteVlasnistvo/{create_vlasnistvo}")
    client.delete(f"/grad/deleteGrad/{create_grad}")
    client.delete(f"/vlasnik/deleteVlasnik/{create_vlasnik}")
    client.delete(f"/admin/deleteAdmin/{create_admin}")
