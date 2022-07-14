import Header from "../components/Header"
import Sidebar from "../components/Sidebar"
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Cards from "../components/Cards/Cards"
import Categorys from "../components/Categorys";
import Button from 'react-bootstrap/Button';
import { useAppState } from "../contexts/AppContext";
import { useState, useEffect } from "react";
import SignIn from "./SignIn";


function Home() {

  const {data } = useAppState()

  return (
    <>
    <SignIn />
    <Header  />
    <Sidebar/>
    <Container className="mt-5">
        <Row>
            <Col md={12} lg={{ span: 5,  order: 'last' }}>
                <Categorys/>
            </Col>
            <Col md={12} lg={{ span: 7,  order: 'first' }}>
                { data ? 
                data.map((blogCard)=> (
                <Cards blog={blogCard}/> 
                )) 
                :
                <h2>Loading</h2> }

            </Col>
      </Row>
    </Container>
 
    </>
  );
}

export default Home;