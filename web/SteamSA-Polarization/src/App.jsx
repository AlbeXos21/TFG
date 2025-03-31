import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import ProductDetail from "./pages/ProductDetail";

function App() {
  return (

    <Router>
      <Routes>
        <Route path="/" element={<Home />} ></Route> {/* Página principal */}
        <Route path="/producto/:id" element={<ProductDetail />} ></Route> {/* Página producto plantilla */}
      </Routes>
      
    </Router>
  );
}

export default App;