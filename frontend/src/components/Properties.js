import { Link, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Properties = () => {
    const [properties, setProperties] = useState([]);
    const location = useLocation();

    useEffect(() => {
        fetch('http://localhost:8000/objekt/getAllObjekt')
        .then(res => res.json())
        .then(data => {
            console.log(data);
            setProperties(data);
            if (data.length > 0) {
                const ids = data.map(obj => obj.objekt_id);
                localStorage.setItem("ids", JSON.stringify(ids));
                console.log('Properties je promijenjena, dohvaćeni su objekti: ', data);
            }
        }).catch(err => console.error(err));
    }, [location]);

    return (
        <div className="properties-container">
            <ul>
                {properties.map((obj, index) => (
                    <li key={obj.objekt_id}>
                        <Link to={`/objekt/${obj.objekt_id}`}>{(index + 1)}. {obj.naziv}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Properties;