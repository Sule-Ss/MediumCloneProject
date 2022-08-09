import Header from "../components/Header";
import Sidebar from "../components/Sidebar/Sidebar";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Cards from "../components/Cards/Cards";
import Categorys from "../components/Categorys";
import { useAppState } from "../contexts/AppContext";
import SignIn from "./SignIn";
import LogIn from "./LogIn";
import { useEffect } from "react";
import Images from "../assets/Images";

function Home() {
  const { data, trendList } = useAppState();

  return (
    <>
      <SignIn />
      <LogIn />
      <Header />
      <Sidebar trendList={trendList} />
      <Container className="mt-5">
        <Row>
          <Col md={12} lg={{ span: 5, order: "last" }}>
            <Categorys />
          </Col>
          <Col md={12} lg={{ span: 7, order: "first" }}>
            {data ? (
              data.map((blogCard) => <Cards blog={blogCard} />)
            ) : (
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <img src={Images.loading} alt="loading gif" />
              </div>
            )}
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default Home;
