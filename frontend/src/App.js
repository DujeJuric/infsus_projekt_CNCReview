import './App.css';
import Navbar from './components/Navbar';
import Header from './components/Header';
import Properties from './components/Properties';
import Property from './components/PropertyMaster';
import HomePage from './components/HomePage';
import Cities from './components/CitiesLookup';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="app-content">
        <Header />
        <Navbar />
        <div className="page-container">
          <Routes>
            <Route path="/objekti" element={<Properties />} />
            <Route path="/objekt/:id" element={<Property />} />
            <Route path="/gradovi" element={<Cities />} />
            <Route path="/" element={<HomePage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
