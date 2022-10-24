import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import axios from "axios";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);
  const [hello, setHello] = useState([{}]);

  useEffect(() => {
    axios
      .get("/redis")
      .then((response) => setHello(response.data.data))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div className="App">
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src="/vite.svg" className="logo" alt="Vite logo" />
        </a>
        <a href="https://reactjs.org" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <h1>{hello[0].hello || "hello"}</h1>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  );
}

export default App;
