import React, { useState } from 'react';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import { Rating } from 'primereact/rating';

export default function Results({ products, currentCategory }) {
  const [showDescription, setShowDescription] = useState({});

  const handleDescriptionClick = (id) => {
    setShowDescription(prevState => ({...prevState, [id]: !prevState[id]}));
  };

  return (
      <Row xs={1} md={2} className="g-4">
        {products.map((producto) => (
            <Col key={producto.id}>
              <Card>
                <Card.Img variant="top" src={`${producto.image}`}/>
                <Card.Body>
                  <Card.Title>{producto.title}</Card.Title>
                  {showDescription[producto.id] && <Card.Text>{producto.description}</Card.Text>}
                </Card.Body>
                <div className="d-flex justify-content-center align-items-center">
                  <Rating value={producto.rating.rate} readOnly cancel={false}/>
                </div>
                <div className="d-flex justify-content-center align-items-center">
                  <p>{producto.rating.rate}</p>
                </div>
                <p className="m-0">{producto.price}€</p>
                <Card.Footer>
                  <div className="d-flex justify-content-center align-items-center">
                    <Button className="btn-description"
                            onClick={() => handleDescriptionClick(producto.id)}>Description</Button>
                  </div>
                </Card.Footer>
              </Card>
            </Col>
        ))}
      </Row>
  );
}