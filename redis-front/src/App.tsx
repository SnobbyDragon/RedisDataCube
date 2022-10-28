import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import Table from "./Components/Table";

type data = {
  hello?: string;
};

function App() {
  const [query, setQuery] = useState("");
  const [apiData, setApiData] = useState<Array<any>>([]);
  const [hello, setHello] = useState<Array<any>>([{}]);
  const [redisKeys, setRedisKeys] = useState<Array<string>>([]);
  const [waiting, setWaiting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (query.length > 0) {
      const response = await axios.get(`/redis/${query}`);
      setWaiting(true);
      if (response.status === 200) {
        const data: Object = response.data.data;
        for (const [key, value] of Object.entries(data)) {
          setApiData((arr) => [...arr, value]);
        }
        setWaiting(false);
      } else {
        console.log(response.request);
      }
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
        {apiData.length > 0 && <Table data={apiData} />}
        {/* {waiting ? (
          <div>
            <img src="../loading.gif"></img>
          </div>
        ) : (
          <Table columns={columns} rows={rows} />
        )} */}
        <br></br>
        {query.length === 0 ? <></> : <div>Query: {query}</div>}
        {/* {result.length === 0 ? <></> : <div>Result: {result}</div>} */}
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
