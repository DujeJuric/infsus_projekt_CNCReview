import { createContext, useContext, useEffect, useState } from "react";

const LookupContext = createContext();

export const useLookup = () => useContext(LookupContext);

export const LookupProvider = ({ children }) => {
  const [cities, setCities] = useState([]);

  const refreshLookup = () => {
    fetch('http://localhost:5000/getCities')
      .then(res => res.json())
      .then(data => {
        setCities(data);
        console.log('refresh lookup: ', data);
    }).catch(err => console.error(err));
  };

  useEffect(() => {
    refreshLookup();
  }, []);

  return (
    <LookupContext.Provider value={{ cities, refreshLookup }}>
      {children}
    </LookupContext.Provider>
  );
};
