import { useState } from "react";
import axios from "axios";
import "./App.css";
import Table from "./Components/Table";
import RedisP from "./assets/redisearch.png";

function App() {
  const [query, setQuery] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [searchEnabled, setSearchEnabled] = useState(false);
  const [apiData, setApiData] = useState<Array<any>>([]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setApiData([]);
    if (query.length > 0) {
      try {
        const response = await axios.get(`/redis/${query}`);
        setErrorMsg("");
        const data: Object = response.data.data;
        for (const [key, value] of Object.entries(data)) {
          setApiData((arr) => [...arr, value]);
        }
      } catch (e) {
        setErrorMsg("Invalid query");
      }
    } else {
      setErrorMsg("A query needs to be provided");
    }
  };

  return (
    <div className="App">
      <h1>Redis Cuber</h1>
      <div id="search-container">
        {!searchEnabled ? (
          <div id="glass">
            <img src={RedisP} onClick={() => setSearchEnabled(true)}></img>
          </div>
        ) : (
          <form onSubmit={(e) => handleSubmit(e)}>
            <input
              id="query-input"
              type={"search"}
              placeholder="SELECT ... Press Enter to submit"
              name="query"
              className={errorMsg.length > 0 ? "error-box" : ""}
              onChange={(box) => setQuery(box.target.value)}
            ></input>
            <div className="error-msg">{errorMsg}</div>
          </form>
        )}
      </div>
      <div className="card">
        {apiData.length > 0 && <Table data={apiData} />}
        {searchEnabled && errorMsg.length === 0 ? (
          <div>Query: {query}</div>
        ) : (
          <></>
        )}
        {searchEnabled && apiData.length > 0 ? (
          <a href="#top">Go to top</a>
        ) : (
          <></>
        )}
      </div>
    </div>
  );
}

export default App;
