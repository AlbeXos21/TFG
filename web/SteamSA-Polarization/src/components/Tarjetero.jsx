import React, { useEffect, useState } from 'react';
import "./Tarjetero.css"

function Tarjetero({titulo}) {
    
    return(
        <a href={`/producto/${titulo.IDAPP}`}><article className='carta_titulo'>
            <div className='imagen_titulo'>
                <img src={`https:\/\/shared.akamai.steamstatic.com\/store_item_assets\/steam\/apps\/${titulo.IDAPP}\/header.jpg`} alt="" />
            </div>
            <div className='info_titulo'>
                <p className='titulo'>{titulo.NOMBRE}</p>
               
                <div className='puntuacion'>
                    <div className='contenedor_reseñas'>
                        <div>RESEÑAS POSITIVAS{"\u00A0"} {titulo.RPOS}</div>
                        <div>RESEÑAS NEGATIVAS {titulo.RNEG}</div>
                    </div>
                    <div className='contenedor_nota' style={{
                                                backgroundColor: 
                                                    titulo.MEDIA >= 8.5
                                                        ? 'rgb(14, 172, 0)' 
                                                        : titulo.MEDIA >= 7.5 
                                                            ? 'rgb(95, 240, 82)' 
                                                            : titulo.MEDIA >= 6
                                                                ? "rgb(252, 249, 59)"
                                                                : titulo.MEDIA >= 5
                                                                    ? "rgb(247, 164, 11)"
                                                                    : "red"
                                                            }}><p className='nota' >{titulo.MEDIA}</p></div>
                </div>
            </div>
            <div></div>
        </article>
        </a>
    )

}

export default Tarjetero;