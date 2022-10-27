import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Table from "./Components/Table";

type data = {
  hello?: string;
};

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");
  const [hello, setHello] = useState<Array<any>>([{}]);
  const [redisKeys, setRedisKeys] = useState<Array<string>>([]);
  const [waiting, setWaiting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (query.length > 0) {
      const result = await axios.get(`/redis/${query}`);
      setWaiting(true);
      if (result.status === 200) {
        setResult(result.data);
        setWaiting(false);
      } else {
        console.log(result.request);
      }
      // .then((response) => {
      //   setResult(response.data);
      // })
      // .catch((err) => console.log(err));
    }
  };

  const columns = ["c1", "c2", "c3", "c4", "c5", "c6"];
  const rows = [{ c1: "c1", c2: "c2", c3: "c3", c4: "c4", c5: "c5", c6: "c6" }];

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
    <div className="Addpp">
      <h1>Redis Cuber</h1>
      <div id="search-container">
        <form onSubmit={(e) => handleSubmit(e)}>
          <input
            id="query-input"
            type={"search"}
            placeholder="SELECT ..."
            name="query"
            onChange={(box) => setQuery(box.target.value)}
          ></input>
        </form>
      </div>
      <div className="card">
        {waiting ? (
          <div>
            <img src="../loading.gif"></img>
          </div>
        ) : (
          <Table columns={columns} rows={rows} />
        )}
        <div id="table">
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
        <br></br>
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
