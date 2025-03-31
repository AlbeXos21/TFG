import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import "./ProductDetail.css"
import TarjeteroProducto from "../components/TarjeteroProducto";
import NavBar from "../components/NavBar"
import ListaBusqueda from "../components/ListaBusqueda";
function ProductDetail() {
  const { id } = useParams();  // 'id' es el parámetro de la ruta
  const [mostrarlistabusqueda, setMostrarLista] = useState(false);
  const [inputTemporal, setInputTemporal] = useState(""); // Estado inmediato
  const [valor, setValor] = useState(""); // Estado con delay
  const [titulo,setTitulo] = useState("");
  const [tf,setTF] = useState("1");
  const [generos,setGeneros] = useState("000000");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setValor(inputTemporal);
    }, 1000);

    return () => clearTimeout(timeout); 
  }, [inputTemporal]);

  const manejarCambio = (event) => {
    setInputTemporal(event.target.value); // Captura el valor sin delay
  };

 
  const handleFocus = () => {
    const timeout = setTimeout(() => {
      setMostrarLista(true); 
    }, 100); 
    return () => clearTimeout(timeout); 
  };


  const handleBlur = () => {
    const timeout = setTimeout(() => {
      setMostrarLista(false); 
    }, 100); 
    return () => clearTimeout(timeout); 
  };



  useEffect(() => {
    ObtenerDatosTitulo(id)
      .then((data) => {
        setTitulo(data);
        setGeneros(data["GENEROS"])
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error al obtener los datos:", error);
        setError("Error al cargar los datos.");
        setLoading(false);
      });
  }, []);

  const cambiarGrafica = () => {
    if(tf == "1"){
      setTF("2")
    }else{
      setTF("1")
    }
  };



    // Si está cargando o hubo un error, mostramos un mensaje o un spinner
    if (loading || error)
      return (
        <>
          <div className="wrapper">
            {loading ? (
              <div className="space">
                <div className="loading"></div>
              </div>
            ) : (
              <p className="texto_carga">{error}</p>
            )}
          </div>
        </>
      );



  return (
    <>
    <div className='contenedor_tarjetero' style={{ backgroundImage: `url(https://store.fastly.steamstatic.com/images/storepagebackground/app/${id})` }}>
      <NavBar valor={inputTemporal} onChange={manejarCambio} onFocus={handleFocus} onBlur={handleBlur} ></NavBar>  
      { mostrarlistabusqueda && <ListaBusqueda input={valor} />}

      <TarjeteroProducto id={id} rp={titulo.RPOS} rn={titulo.RNEG} media={titulo.MEDIA} resumen={titulo.RESUMEN} generos={generos}></TarjeteroProducto>
      
    </div>
    <div className='contenedor_estadisticas'>
      <h1> ESTADÍSTICAS</h1>

      <div className='contenedor_graficos'>
        <div className='contenedor_TF_IDF_BM25'>
          <h1>TF-IDF</h1>
          <div><img src={`../${id}/graficoTF_IDF_${tf}.png`} alt="" /><button onClick={cambiarGrafica}>CAMBIAR GRÁFICA</button></div>
          
        </div>
        <div className='contenedor_TF_IDF_BM25'>
        <h1>BM-25</h1>
        <div><img src={`../${id}/graficoBM25.png`} alt="" /></div>
        </div>
      </div>
    </div>

    <div className='contenedor_estadisticas' >
    <h1>GRÁFICOS DE CRITERIOS</h1>

      <div className='contenedor_graficos_criterios'>
        <img src={`../${id}/grafico_criterios.svg`} alt="" />
      </div>
    </div>

    </>
  );
}

function ObtenerDatosTitulo(id) {
  return fetch(`http://localhost:5000/producto/${id}`)
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error al obtener los datos:", error);
      throw error;
    });
}



export default ProductDetail;
