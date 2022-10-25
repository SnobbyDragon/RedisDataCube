import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import axios from "axios";
import "./App.css";

type data = {
  hello?: string;
};

function App() {
  const [count, setCount] = useState(0);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");
  const [hello, setHello] = useState<Array<any>>([{}]);
  const [redisKeys, setRedisKeys] = useState<Array<string>>([]);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (query.length > 0) {
      axios
        .get(`/redis/${query}`)
        .then((response) => {
          setResult(response.data);
        })
        .catch((err) => console.log(err));
    }
  };

  useEffect(() => {
    axios
      .get("/redis")
      .then((response) => setHello(response.data.data))
      .catch((err) => console.log(err));
    axios
      .get("/redis/keys")
      .then((response) => setRedisKeys(response.data.data))
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
        <div id="table">
          <h1>Redis DB Keys</h1>
          {redisKeys.map((str) => (
            <b key={redisKeys.indexOf(str)}>{str}, </b>
          ))}
          <table>
            <thead>
              <tr>
                <td>Key</td>
                <td>Value</td>
              </tr>
            </thead>
            <tbody>
              {hello.map((o, i) => {
                return (
                  <tr key={i}>
                    <td>{Object.keys(o)}</td>
                    <td>{o.hello}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <br></br>
        <form onSubmit={(e) => handleSubmit(e)}>
          <input
            id="query-input"
            type={"search"}
            placeholder="SELECT ..."
            name="query"
            onChange={(box) => setQuery(box.target.value)}
          ></input>
        </form>
        {query.length === 0 ? <></> : <div>Query: {query}</div>}
        {result.length === 0 ? <></> : <div>Result: {result}</div>}
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
