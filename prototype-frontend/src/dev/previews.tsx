import {ComponentPreview, Previews} from "@react-buddy/ide-toolbox";
import {PaletteTree} from "./palette";
import App from "../App";
import Dashboard from "../pages/Dashboard";
import Configuration from "../pages/Configuration";
import Navigation from "../components/Navigation";
import AllGraphs from "../components/AllGraphs";

const ComponentPreviews = () => {
    return (
      <Previews palette={<PaletteTree />}>
        <ComponentPreview path="/App">
          <App />
        </ComponentPreview>
        <ComponentPreview path="/Dashboard">
          <Dashboard />
        </ComponentPreview>
        <ComponentPreview path="/Configuration">
          <Configuration />
        </ComponentPreview>
        <ComponentPreview path="/Navigation">
          <Navigation />
        </ComponentPreview>
        <ComponentPreview path="/AllGraphs">
          <AllGraphs />
        </ComponentPreview>
      </Previews>
    );
};

export default ComponentPreviews;
