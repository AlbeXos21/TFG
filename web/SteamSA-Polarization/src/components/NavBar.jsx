import React, { useState, useEffect } from "react";
import "./NavBar.css"


function NavBar({ onFocus, onBlur, valor, onChange}) {
  return (
    <div className="navbar">
        <a href="../"><img src="../Logo_TFG_inicio.png" alt="" /></a>
      <div className="barra_busqueda">

        <input 
          type="text"
          value={valor} // Recibe el valor desde las props
          onChange={onChange} // Recibe la función onChange desde las props
          onFocus={onFocus}  // Llama a handleFocus en Home cuando el input tiene foco
          onBlur={onBlur}    // Llama a handleBlur en Home cuando el input pierde el foco
        />
      </div>
      
    </div>
  );
}


export default NavBar;