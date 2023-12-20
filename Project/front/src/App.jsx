import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navigation from './components/Navigation.jsx'
import Results from './components/Results.jsx'
import { useEffect } from 'react'; // Add missing import statement
import { PrimeReactProvider, PrimeReactContext } from 'primereact/api';

function App() {
  const [products, setProducts] = useState([])
  const [productsF, setProductsF] = useState([])

  const changed = (evento) => {
    if (evento.target.value !== "") {
      const filteredProductos = products.filter((producto) => producto.category.includes(evento.target.value))
      setProductsF(filteredProductos)
    } else {
      setProductsF(products)
    }

    console.log(evento.target.value)
  }

  useEffect(() => {
    fetch("http://localhost:8000/etienda/api/products?start=0&end=100")
      .then((response) => response.json())
      .then((prods) => {
        setProducts(prods)
        setProductsF(prods)
      });
  }, [])

  return (
    <>
      <Navigation changed={changed} setProducts={setProductsF}/>
      <Results products={productsF}/>
    </>
  )
}

export default App