import React ,{ useEffect, useState } from 'react';
import "./TarjeteroProducto.css";

function TarjeteroProducto({id,rp,rn,media,resumen,generos}) {
    console.log(generos)
    return (
        <div className='tarjetero_producto'>
            <div className='tarjetero_producto_video'>
                <div className='contenedor_video'>
                   
                <video 
                        src={`../${id}/trailer.webm`}
                        controls
                        className="video"
                    />
                </div>

                <div className='contenedor_datos'>
                    <div className='nota_tarjetero'style={{
                                                backgroundColor: 
                                                    media >= 8.5
                                                        ? 'rgb(14, 172, 0)' 
                                                        : media >= 7.5 
                                                            ? 'rgb(95, 240, 82)' 
                                                            : media >= 6
                                                                ? "rgb(252, 249, 59)"
                                                                : media >= 5
                                                                    ? "rgb(247, 164, 11)"
                                                                    : "rgb(226, 38, 38)"
                                                            }}>{media}</div>
                    <div className='resenas_contador'>
                        <div>
                        RESEÑAS POSITIVAS {"\u00A0"}{rp}
                        </div>
                        <div>
                        RESEÑAS NEGATIVAS {rn}
                        </div>
                    </div>
                </div>
            </div>

            <div className='tarjetero_producto_info'>
                <img src={`https:\/\/shared.akamai.steamstatic.com\/store_item_assets\/steam\/apps\/${id}\/header.jpg`} alt="" srcset="" />
                <div>{resumen}</div>
                <div className='generos'>
                          <div><img style={{
                                                filter: parseInt(generos[0]) ? 'grayscale(0%)' : 'grayscale(100%)'
                                            }} src="/iconos/aventuras.png" alt="" /></div>
                            <div><img style={{
                                                filter: parseInt(generos[1]) ? 'grayscale(0%)' : 'grayscale(100%)'
                                            }}src="/iconos/pistola.png" alt="" /></div>
                            <div><img style={{
                                                filter: parseInt(generos[2]) ? 'grayscale(0%)' : 'grayscale(100%)'
                                            }}src="/iconos/rpg.png"  alt="" /></div>
                            <div><img style={{
                                                filter: parseInt(generos[3]) ? 'grayscale(0%)' : 'grayscale(100%)'
                                            }}src="/iconos/estrategia-en-tiempo-real.png" alt="" /></div>
                            <div><img style={{
                                                filter: parseInt(generos[4]) ? 'grayscale(0%)' : 'grayscale(100%)'
                                            }}src="/iconos/simulacion.png" alt="" /></div>
                            <div><img style={{
                                                filter: parseInt(generos[5]) ? 'grayscale(0%)' : 'grayscale(100%)'
                                            }}src="/iconos/bola-de-fuego.png" alt="" /></div>


                </div>
            </div>
        </div>
    );
}

export default TarjeteroProducto;

