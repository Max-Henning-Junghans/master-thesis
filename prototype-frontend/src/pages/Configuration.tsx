import React from "react";
import Navigation from "../components/Navigation";
import ConfigurationInput from "../components/ConfigurationInput";

function Configuration(props: any) {
  return (
    <div className="d-flex justify-content-center">
      <div className="d-flex flex-column align-items-center">
        <Navigation />
        <br />
        <h1>Configuration</h1>
        <p>
            This is the configuration page.
            Here you can configure the rules for the system.
        </p>
        <ConfigurationInput />
      </div>
    </div>
  );
}

export default Configuration;
