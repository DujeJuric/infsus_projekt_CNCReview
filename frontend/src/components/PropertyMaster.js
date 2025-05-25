import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useLookup } from './LookupContext';
import Reviews from './ReviewsDetail';

const Property = () => {
    const { id } = useParams();
    const [property, setProperty] = useState(null);
    const [position, setPosition] = useState(null);
    const [allIds, setAllIds] = useState([]);
    const navigate = useNavigate();

    const [description, setDescription] = useState("");
    const [name, setName] = useState("");
    const [address, setAddress] = useState("");
    const [city, setCity] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [workingHours, setWorkingHours] = useState("");
    const [workingDays, setWorkingDays] = useState("");
    const { cities } = useLookup();
    const [succUpdate, setSuccUpdate] = useState(null);
    const [succDelete, setSuccDelete] = useState(null);

    useEffect(() => {
        const idsLS = localStorage.getItem("ids");
        const ids = idsLS ? JSON.parse(idsLS) : [];
        console.log('svi id-jevi: ', ids);
        setAllIds(ids);

        const index = ids.indexOf(Number(id));
        setPosition(index);

        setSuccDelete(null);
        setSuccUpdate(null);

        fetch(`http://localhost:5000/getProperties/${id}`)
            .then(res => res.json())
            .then(data => {
                setProperty(data);
                setName(data.naziv);
                setDescription(data.opis);
                setAddress(data.adresa);
                setPhoneNumber(data.mobilni_broj);
                setWorkingHours(data.radno_vrijeme);
                setWorkingDays(data.radni_dani);
                setCity(data.grad_id);
            }).catch(err => console.error(err));


    }, [id]);

    const prevNext = (i) => {
        if (i >= 0 && i < allIds.length) {
            navigate(`/objekt/${allIds[i]}`);
        }
    };

    if (!property) {
        return <p>Učitavanje...</p>;
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        setSuccUpdate(null);
        const propertyData = { name, description, address, phoneNumber, workingDays, workingHours, city };
        console.log(propertyData);

        fetch(`http://localhost:5000/changeProperty/${id}`, {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(propertyData)
        }).then(res => {
            console.log(res);
            if (!res.ok) {
                throw new Error("Neuspješno ažuriranje");
            }
            return res.json();
        }).then(() => {
            console.log('Uspješno ažuriranje!');
            setSuccUpdate(true);
        }).catch((err) => console.error('Greška!: ', err));
    }

    const handleDelete = () => {
        const object_id = id;
        setSuccDelete(null);

        fetch(`http://localhost:5000/delete/${object_id}`, {
            method: 'DELETE'
        }).then(res => {
            if (!res.ok) {
                throw new Error("Neuspješno brisanje");
            }
            console.log('Uspješno brisanje!');

            const updatedIds = [...allIds];
            updatedIds.splice(position, 1);

            setAllIds(updatedIds);
            localStorage.setItem("ids", JSON.stringify(updatedIds));
            setSuccDelete(true);

            if (updatedIds.length > 0) {
                const newPos = position >= updatedIds.length ? updatedIds.length - 1 : position;
                navigate(`/objekt/${updatedIds[newPos]}`);
            } else {
                navigate('/objekt');
            }

            return res.json();
        }).catch((err) => console.error('Greška!: ', err));
    }

    return (
        <div className="master-container">
            <div className="prev-next-cont">
                <button onClick={() => prevNext(position - 1)} disabled={position === 0}>Prethodni</button>
                <button onClick={() => prevNext(position + 1)} disabled={position === allIds.length - 1}>Sljedeći</button>
            </div>

            <div className="master-form-container">
                <form className="prop-details-form" onSubmit={handleSubmit}>
                    <label htmlFor="name">Naziv objekta: </label>
                    <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required />
                    <label htmlFor="description">Opis: </label>
                    <input type="text" id="description" value={description} onChange={(e) => setDescription(e.target.value)} required />
                    <label htmlFor="address">Adresa: </label>
                    <input type="text" id="address" value={address} onChange={(e) => setAddress(e.target.value)} required />
                    <label htmlFor="city-select">Grad:</label>
                    <select id="city-select" value={city} onChange={e => setCity(e.target.value)}>
                        <option value="">--Odaberi grad--</option>
                        {cities.map(c => (
                            <option key={c.grad_id} value={c.grad_id}>{c.naziv}</option>
                        ))}
                    </select>
                    <label htmlFor="phoneNumber">Broj mobitela: </label>
                    <input type="text" id="phoneNumber" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} required />
                    <label htmlFor="workingHours">Radno vrijeme: </label>
                    <input type="text" id="workingHours" value={workingHours} onChange={(e) => setWorkingHours(e.target.value)} required />
                    <label htmlFor="workingDays">Radni dani: </label>
                    <input type="text" id="workingDays" value={workingDays} onChange={(e) => setWorkingDays(e.target.value)} required />
                    <div className="save-del-mst">
                        <button type="submit" className='save-button'>Spremi</button>
                        <button className="delete-button-mt" onClick={handleDelete}>Obriši</button>
                    </div>
                </form>
                {succDelete && <div className="delete-msg"><p>Objekt je uspješno obrisan!</p></div>}
                {succUpdate && <div className="update-msg"><p>Promjene su uspješno spremljene!</p></div>}
            </div>
            <hr></hr>
            <Reviews propertyId={id} />
        </div>
    );
};

export default Property;
