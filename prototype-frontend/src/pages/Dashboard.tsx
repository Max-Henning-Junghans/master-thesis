import React from "react";
import Navigation from "../components/Navigation";
import AllGraphs from "../components/AllGraphs";

function Dashboard(props: any) {
  return (
    <div className="d-flex justify-content-center ">
      <div className="d-flex flex-column align-items-center">
        <Navigation />
        <br />
        <h1>Dashboard</h1>
        <AllGraphs />
      </div>
    </div>
  );
}

export default Dashboard;
