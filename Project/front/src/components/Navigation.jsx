import React, { useState, useEffect } from 'react'
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

export default function Navigation({changed, setProducts}) {
    const [searchTerm, setSearchTerm] = useState("");
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/etienda/api/categories")
            .then((response) => response.json())
            .then((cats) => {
                setCategories(cats);
            });
    }, []);

    const handleSearch = async (event) => {
        event.preventDefault();
        const response = await fetch(`http://localhost:8000/etienda/api/searchproduct?product_info=${searchTerm}`);
        const data = await response.json();
        setProducts(data);
    };

    const handleCategoryClick = async (category) => {
        const response = await fetch(`http://localhost:8000/etienda/api/category/${category}`);
        const data = await response.json();
        setProducts(data);
    };

    return (
        <Navbar expand="lg" className="navbar-dark" fixed="top">
        <Container fluid>
            <Navbar.Brand href="#" onClick={() => window.location.href = window.location.origin}>DAI Commerce</Navbar.Brand>
            <Navbar.Toggle aria-controls="navbarScroll" />
            <Navbar.Collapse id="navbarScroll">
                <Nav
                    className="me-auto my-2 my-lg-0"
                    style={{ maxHeight: '100px' }}
                    navbarScroll
                >
                    <NavDropdown title="Categories" id="navbarScrollingDropdown">
                        {categories.map((category, index) => (
                            <NavDropdown.Item key={index} onClick={() => handleCategoryClick(category)}>
                                {category}
                            </NavDropdown.Item>
                        ))}
                    </NavDropdown>
                </Nav>
                <Form className="d-flex" onSubmit={handleSearch}>
                    <Form.Control
                        type="search"
                        placeholder="Search"
                        className="me-2"
                        aria-label="Search"
                        onChange={ (evento) => {setSearchTerm(evento.target.value)}}
                    />
                    <Button className="btn btn-success" type="submit">Search</Button>
                </Form>
            </Navbar.Collapse>
        </Container>
    </Navbar>
    )
}