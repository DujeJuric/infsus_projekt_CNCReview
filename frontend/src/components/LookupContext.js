import { createContext, useContext, useEffect, useState } from "react";

const LookupContext = createContext();

export const useLookup = () => useContext(LookupContext);

export const LookupProvider = ({ children }) => {
  const [cities, setCities] = useState([]);
  const [ratings, setRatings] = useState([]);

  const refreshLookup = () => {
    fetch('http://localhost:8000/grad/getAllGradovi')
      .then(res => res.json())
      .then(data => {
        setCities(data);
        console.log('refresh lookup: ', data);
    }).catch(err => console.error(err));
  };

  useEffect(() => {
    refreshLookup();
  }, []);

  useEffect(() => {
    fetch('http://localhost:8000/ocjena/getAllOcjena')
      .then(res => res.json())
      .then(data => {
        setRatings(data);
        console.log('ratings from lookup: ', data);
    }).catch(err => console.error(err));
  }, []);

  return (
    <LookupContext.Provider value={{ cities, refreshLookup, ratings }}>
      {children}
    </LookupContext.Provider>
  );
};
