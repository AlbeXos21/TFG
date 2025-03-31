import { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import Tarjetero from "../components/Tarjetero";
import "./Home.css";
import ListaBusqueda from "../components/ListaBusqueda";

function Home() {
  const [titulos, setTitulos] = useState([]);
  const [imagenfondo, setImagenFondo] = useState("./fondo_web.jpg");
  const [mostrarlistabusqueda, setMostrarLista] = useState(false);
  const [inputTemporal, setInputTemporal] = useState(""); // Estado inmediato
  const [valor, setValor] = useState(""); // Estado con delay

  // ✅ Aplica un delay para actualizar "valor" cuando el usuario deja de escribir
  useEffect(() => {
    const timeout = setTimeout(() => {
      setValor(inputTemporal);
    }, 1000);

    return () => clearTimeout(timeout); // Cancela el timeout si el usuario sigue escribiendo
  }, [inputTemporal]);

  const manejarCambio = (event) => {
    setInputTemporal(event.target.value); // Captura el valor sin delay
  };

  useEffect(() => {
    ObtenerTitulosHome()
      .then((data) => {
        setTitulos(data["juegos"]);

      })
      .catch((error) => {
        console.error("Error al obtener los datos:", error);

      });
  }, []);

  const handleFocus = () => {
    const timeout = setTimeout(() => {
      setMostrarLista(true); // Muestra la lista de búsqueda después de un delay
    }, 100); // Puedes ajustar el tiempo en milisegundos
    return () => clearTimeout(timeout); // Limpiar el timeout si el componente se desmonta
  };


  const handleBlur = () => {
    const timeout = setTimeout(() => {
      setMostrarLista(false); // Oculta la lista de búsqueda después de un delay
    }, 100); // Puedes ajustar el tiempo en milisegundos
    return () => clearTimeout(timeout); // Limpiar el timeout si el componente se desmonta
  };



    
  return (
    <>
    
      <div className="contenedor_inicio" style={{ backgroundImage: `url(${imagenfondo})` }}>
        <NavBar valor={inputTemporal} onChange={manejarCambio} onFocus={handleFocus} onBlur={handleBlur} />

        
        { mostrarlistabusqueda && <ListaBusqueda input={valor} />}


        <section className="contenedor_imagen">
          <a href="" target="_blank" rel="noopener noreferrer">
            <img src="./Logo_TFG_inicio.png" alt="Logo" />
          </a>
        </section>

        <section className="contenedor_texto">
          <div className="contenedor_titulo">
            <p>SteamSA/Polarization</p>
          </div>
          <div className="contenedor_autor">
            <p>Alberto Contreras Puerto</p>
          </div>
        </section>
      </div>

      <div className="contenedor_recomendados2">
        <h1>ÚLTIMOS RESEÑADOS</h1>
        <ul className="lista_contenedor">
          {titulos.slice(0, 4).map((titulo) => (
            <li key={titulo.IDAPP}>
              <Tarjetero titulo={titulo} />
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

function ObtenerTitulosHome() {
  return fetch("http://localhost:5000/")
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error al obtener los datos:", error);
      throw error;
    });
}

export default Home;
