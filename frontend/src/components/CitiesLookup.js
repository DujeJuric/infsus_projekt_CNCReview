import { useState } from "react";
import { useLookup } from "./LookupContext";

const Cities = () => {
    const { cities, refreshLookup } = useLookup();
    const [editCityId, setEditCityId] = useState(null);
    const [editedName, setEditedName] = useState("");
    const [addCity, setAddCity] = useState(false);
    const [newName, setNewName] = useState("");

    // promijeniti path
    const handleDelete = (id) => {
        fetch(`http://localhost:5000/deleteCity/${id}`, {
            method: 'DELETE'
        }).then(res => {
            if (!res.ok) {
                throw new Error("Neuspješno brisanje");
            }
            console.log('Uspješno brisanje!');

            refreshLookup();
        }).catch((err) => console.error('Greška!: ', err));
    }

    const handleEdit = (id, name) => {
        setEditCityId(id);
        setEditedName(name);
    }

    // promijeniti path
    const handleEditSave = (id) => {
        fetch(`http://localhost:5000/updateCity/${id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ naziv: editedName })
        }).then(res => {
            if (!res.ok) {
                throw new Error("Neuspješno ažuriranje");
            }
            setEditCityId(null);
            refreshLookup();
        }).catch(err => console.error('Greška!', err));
    }

    const handleAdd = () => {
        setAddCity(true);
    }

    // promijeniti path
    const handleAddSave = () => {
        fetch(`http://localhost:5000/addCity`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ naziv: newName })
        }).then(res => {
            if (!res.ok) throw new Error("Neuspješno dodavanje");
            setAddCity(false);
            setNewName("");
            refreshLookup();
        }).catch(err => console.error('Greška!', err));
    }


    return (
        <div className="lookup-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Naziv</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {cities.map(city => (
                        <tr key={city.grad_id}>
                            <td>{city.grad_id}</td>
                            <td>
                                {editCityId === city.grad_id ? (
                                <input type="text" value={editedName} onChange={(e) => setEditedName(e.target.value)} required />
                            ) : (city.naziv)}
                            </td>
                            <td>
                                {editCityId === city.grad_id ? (
                                    <button className="button-ct" onClick={() => handleEditSave(city.grad_id)}>Spremi</button>
                                ) : (
                                    <button className="button-ct" onClick={() => handleEdit(city.grad_id, city.naziv)}>Uredi</button>
                                )}
                            </td>
                            <td><button className="button-ct" onClick={() => handleDelete(city.grad_id)}>Obriši</button></td>
                        </tr>
                    ))}
                    {addCity && (
                        <tr>
                            <td></td>
                            <td>
                                <input
                                    type="text"
                                    value={newName}
                                    onChange={(e) => setNewName(e.target.value)}
                                    placeholder="Naziv grada"
                                />
                            </td>
                            <td>
                                <button className="button-ct" onClick={handleAddSave}>Spremi</button>
                            </td>
                            <td></td>
                        </tr>
                    )}
                </tbody>
            </table>
           {!addCity && <button className="button-ct" onClick={handleAdd}>Dodaj novi grad</button>}
        </div>
    );
}

export default Cities;