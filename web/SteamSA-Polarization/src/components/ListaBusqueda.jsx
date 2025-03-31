import React, { useState, useEffect } from "react";
import "./ListaBusqueda.css"



function ListaBusqueda({input}) {

  const [busqueda, setBusqueda] = useState(null);


  useEffect(() => {
        if(input != ''){
          enviarABackend(input);
        }
    }, [input]);


useEffect(() => {
    if (busqueda) {
      console.log("Respuesta del servidor:", busqueda);
      // Aquí puedes hacer algo con la respuesta, por ejemplo, mostrarla en el UI
    }
  }, [busqueda]);

    return (
      <ul className="ul_lista_busqueda">
          {input != "" ? (
        // Mostrar resultados de búsqueda aquí
        busqueda && busqueda.map((item, index) => (
          <a href={`/producto/${item.IDAPP}`} key={index}>
            <li>
              <div className="container_imagen">
                <img src={`https://cdn.akamai.steamstatic.com/steam/apps/${item.IDAPP}/library_600x900.jpg`} alt={item.nombre} />
              </div>
              <p>{item.NOMBRE}</p>
              <div className="container_nota" ><p style={{
                                                backgroundColor: 
                                                    item.NOTA >= 8.5
                                                        ? 'rgb(14, 172, 0)' 
                                                        : item.NOTA >= 7.5 
                                                            ? 'rgb(95, 240, 82)' 
                                                            : item.NOTA >= 6
                                                                ? "rgb(252, 249, 59)"
                                                                : item.NOTA >= 5
                                                                    ? "rgb(247, 164, 11)"
                                                                    : "rgb(226, 38, 38)"
                                                            }}>{item.NOTA ? item.NOTA : "N/A"}</p></div>
            </li>
          </a>
        ))
      ) : (
        <li></li>  // Mostrar un mensaje de carga mientras no haya respuesta
      )}
         

      </ul>
    );


    function enviarABackend(valor) {
      // Solo enviar cuando 'valor' haya cambiado después del debounce
      fetch('http://localhost:5000/busqueda', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ valor: valor }) // Enviar el valor al backend
      })
        .then(response => response.json()) // Procesar la respuesta del backend
        .then(data => {
          setBusqueda(data["juegos"]);
        })
        .catch(error => {
          console.error("Error al enviar datos:", error);
        });
    }
    



  }
  



  
  export default ListaBusqueda;