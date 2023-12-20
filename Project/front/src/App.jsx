import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navigation from './components/Navigation.jsx'
import Results from './components/Results.jsx'
import { useEffect } from 'react'; // Add missing import statement
import { PrimeReactProvider, PrimeReactContext } from 'primereact/api';

function App() {
  const [productos, setProductos] = useState([])
  const [productosF, setProductosF] = useState([])

  const cambiado = (evento) => {
    if (evento.target.value !== "") {
      const filteredProductos = productos.filter((producto) => producto.category.includes(evento.target.value))
      setProductosF(filteredProductos)
    } else {
      setProductosF(productos)
    }

    console.log(evento.target.value)
  }

  useEffect(() => {
    fetch("http://localhost:8000/etienda/api/products?start=0&end=100")
      .then((response) => response.json())
      .then((prods) => {
        setProductos(prods)
        setProductosF(prods)
      });
  }, [])

  return (
    <>
      <Navigation cambiado={cambiado} setProductosF={setProductosF}/>
      <Results productos={productosF}/>
    </>
  )
}

export default App