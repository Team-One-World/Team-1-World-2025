import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import api from "./api";

function App() {
  const [planets, setPlanets] = useState([]);

  useEffect(() => {
    getPlanets();
  }, []);

  const getPlanets = () => {
    api.get('/api/planets/')
      .then(res => setPlanets(res.data))
      .catch(err => console.error(err));
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home planets={planets} setPlanets={setPlanets} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
