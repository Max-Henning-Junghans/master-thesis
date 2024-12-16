import React from "react";
import Navigation from "../components/Navigation";

function Home(props: any) {
    return (
      <div className="d-flex justify-content-center">
        <div className="d-flex flex-column align-items-center">
          <Navigation />
          <br />
          <h1>Home</h1>
        </div>
      </div>
    );
}

export default Home;
