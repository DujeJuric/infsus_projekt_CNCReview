import { useState, useEffect } from "react";
import { useLookup } from "./LookupContext";

const Reviews = ({ propertyId }) => {
    const [reviews, setReviews] = useState([]);
    const [editReviewId, setEditReviewId] = useState(null);
    const [editedTitle, setEditedTitle] = useState("");
    const [editedContent, setEditedContent] = useState("");
    const [editedRating, setEditedRating] = useState("");
    const [editedUser, setEditedUser] = useState("");
    const [addReview, setAddReview] = useState(false);
    const [newTitle, setNewTitle] = useState("");
    const [newContent, setNewContent] = useState("");
    const [newRating, setNewRating] = useState("");
    const [newUser, setNewUser] = useState("");
    const [allUsers, setAllUsers] = useState([]);
    const { ratings } = useLookup();

    useEffect(() => {
        if (!propertyId)
            return;
        fetch(`http://localhost:8000/recenzija/getRecenzijeByObjekt/${propertyId}`)
            .then(res => res.json())
            .then(data => {
                if (Array.isArray(data)) {
                    setReviews(data);
                } else {
                    setReviews([]);
                }
                console.log(data);
                setAddReview(false);
            }).catch(err => console.error(err));
    }, [propertyId]);

    useEffect(() => {
        fetch(`http://localhost:8000/korisnik/getAllKorisnik`)
            .then(res => res.json())
            .then(data => {
                if (Array.isArray(data)) {
                    setAllUsers(data);
                } else {
                    setAllUsers([]);
                }
                console.log(data);
            }).catch(err => console.error(err));
    }, []);

    const handleDelete = (id) => {
        fetch(`http://localhost:8000/recenzija/deleteRecenzija/${id}`, {
            method: 'DELETE'
        }).then(res => {
            if (!res.ok) {
                throw new Error("Neuspješno brisanje");
            }
            console.log('Uspješno brisanje!');
            setReviews(prev => prev.filter(r => r.recenzija_id !== id));
        }).catch((err) => console.error('Greška!: ', err));
    }

    const handleEdit = (id, title, rating, content, userId) => {
        setEditReviewId(id);
        setEditedTitle(title);
        setEditedRating(rating);
        setEditedContent(content);
        setEditedUser(userId);
    }

    const handleEditSave = (id) => {
        fetch(`http://localhost:8000/recenzija/updateRecenzija/${id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ naslov: editedTitle, ocjena_id: editedRating, sadrzaj: editedContent, korisnik_id: editedUser, objekt_id: propertyId})
        }).then(res => {
            if (!res.ok) {
                throw new Error("Neuspješno ažuriranje");
            }
            setReviews(prev =>
                prev.map(r =>
                    r.recenzija_id === id
                        ? { ...r, naslov: editedTitle, ocjena_id: editedRating, sadrzaj: editedContent }
                        : r
                )
            );
            setEditReviewId(null);
        }).catch(err => console.error('Greška!', err));
    }

    const handleAdd = () => {
        setAddReview(true);
    }

    const handleAddSave = () => {
        fetch(`http://localhost:8000/recenzija/createRecenzija`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ naslov: newTitle, ocjena_id: newRating, sadrzaj: newContent, korisnik_id: newUser, objekt_id: propertyId })
        }).then(res => {
            if (!res.ok) throw new Error("Neuspješno dodavanje");
            return res.json();
        }).then(newReview => {  //backend mora vratiti novododanu recenziju
            setReviews(prev => [...prev, newReview]);
            setAddReview(false);
            setNewTitle("");
            setNewContent("");
            setNewRating(null);
            setNewUser("");
        }).catch(err => console.error('Greška!', err));
    }

    const getOcjenaText = (id) => {
        const found = ratings.find(r => r.ocjena_id === Number(id));
        return found ? found.ocjena : id;
    };

    const getUser = (id) => {
        const found = allUsers.find(u => u.korisnik_id === id);
        return found ? `${found.ime} ${found.prezime}` : id;
    };

    return (
        <div className="rev-detail-container">
            <h2>Recenzije</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Naslov</th>
                        <th>Ocjena</th>
                        <th>Sadržaj</th>
                        <th>Korisnik</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {reviews.map((review, index) => (
                        <tr key={review.recenzija_id}>
                            <td>{(index + 1)}</td>
                            <td>
                                {editReviewId === review.recenzija_id ? (
                                    <input type="text" value={editedTitle} onChange={(e) => setEditedTitle(e.target.value)} required />
                                ) : (review.naslov)}
                            </td>
                            <td>
                                {editReviewId === review.recenzija_id ? (
                                    <select id="rating-select" value={editedRating} onChange={e => setEditedRating(e.target.value)}>
                                        <option value="">--Odaberi ocjenu--</option>
                                        {ratings.map(rating => (
                                            <option key={rating.ocjena_id} value={rating.ocjena_id}>{rating.ocjena}</option>
                                        ))}
                                    </select>
                                ) : (getOcjenaText(review.ocjena_id))}
                            </td>
                            <td>
                                {editReviewId === review.recenzija_id ? (
                                    <input type="text" value={editedContent} onChange={(e) => setEditedContent(e.target.value)} required />
                                ) : (review.sadrzaj)}
                            </td>
                            <td>
                                {editReviewId === review.recenzija_id ? (getUser(editedUser)) : (getUser(review.korisnik_id))}
                            </td>
                            <td>
                                {editReviewId === review.recenzija_id ? (
                                    <button className="save-button-rd" onClick={() => handleEditSave(review.recenzija_id)}>Spremi</button>
                                ) : (
                                    <button className="edit-button-rd" onClick={() => handleEdit(review.recenzija_id, review.naslov, review.ocjena, review.sadrzaj, review.korisnik_id)}>Uredi</button>
                                )}
                            </td>
                            <td><button className="delete-button-rd" onClick={() => handleDelete(review.recenzija_id)}>Obriši</button></td>
                        </tr>
                    ))}
                    {addReview && (
                        <tr>
                            <td>{(reviews.length + 1)}</td>
                            <td>
                                <input type="text" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} placeholder="Naslov recenzije" />
                            </td>
                            <td>
                                <select id="rating-select" value={newRating} onChange={e => setNewRating(e.target.value)}>
                                    <option value="">--Odaberi ocjenu--</option>
                                    {ratings.map(rating => (
                                        <option key={rating.ocjena_id} value={rating.ocjena_id}>{rating.ocjena}</option>
                                    ))}
                                </select>
                            </td>
                            <td>
                                <input type="text" value={newContent} onChange={(e) => setNewContent(e.target.value)} placeholder="Sadržaj recenzije" />
                            </td>
                            <td>
                                <input type="text" value={newUser} onChange={(e) => setNewUser(e.target.value)} placeholder="Korisnik" />
                            </td>
                            <td>
                                <button className="save-button-rd" onClick={handleAddSave}>Spremi</button>
                            </td>
                            <td></td>
                        </tr>
                    )}
                </tbody>
            </table>
            {!addReview && <button className="add-button-rd" onClick={handleAdd}>Dodaj novu recenziju</button>}
        </div>
    );
}

export default Reviews;