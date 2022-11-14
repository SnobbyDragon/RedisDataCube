import { useState } from "react";
import "./Table.css";
import Fuse from "fuse.js";

type props = {
  data: Array<any>;
};

type Tr = {
  row: Object;
  index: string;
  columns: Array<string>;
};

const TableRow = (props: Tr) => {
  const row = props.row;
  return (
    <tr>
      {Object.values(row).map((rowData, i) => (
        <td key={`row-${props.index}-${props.columns[i]}`}>{rowData}</td>
      ))}
    </tr>
  );
};

const Table = (props: props) => {
  const data = props.data;
  const columns = Object.keys(data[0]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(Infinity);
  const [dataSlice, setDataSlice] = useState(props.data);
  const [numPages, setNumPages] = useState(props.data.length);
  const [fuse, setFuse] = useState(new Fuse(dataSlice, { keys: columns }));

  const searchFor = (search: string) => {
    if (search.length === 0) {
      usePaginator(pageSize);
      return;
    }
    const data = fuse.search(search);
    let searched: any[] = [];
    data.forEach((entry) => {
      searched.push(entry.item);
    });
    setDataSlice(searched);
  };

  const usePaginator = (numRecords: number) => {
    switch (numRecords) {
      case Infinity: {
        setCurrentPage(1);
        setPageSize(Infinity);
        let slice = props.data;
        setDataSlice(slice);
        setFuse(new Fuse(slice, { keys: columns }));
        break;
      }
      case 10: {
        setCurrentPage(1);
        setPageSize(10);
        setNumPages(Math.ceil(data.length / 10));
        let slice = props.data.slice(0, 10);
        setDataSlice(slice);
        setFuse(new Fuse(slice, { keys: columns }));
        break;
      }
      case 100: {
        setCurrentPage(1);
        setPageSize(100);
        setNumPages(Math.ceil(data.length / 100));
        let slice = props.data.slice(0, 100);
        setDataSlice(slice);
        setFuse(new Fuse(slice, { keys: columns }));
        break;
      }
      default: {
        setCurrentPage(1);
        setPageSize(Infinity);
        let slice = props.data;
        setDataSlice(slice);
        setFuse(new Fuse(slice, { keys: columns }));
      }
    }
  };

  const moveBackward = () => {
    if (pageSize !== Infinity) {
      setCurrentPage(currentPage - 1);
      const startOfSlice = data.indexOf(dataSlice[0]) - pageSize;
      const endOfSlice = data.indexOf(dataSlice.at(-1)) - pageSize + 1;

      const slice = data.slice(startOfSlice, endOfSlice);
      setDataSlice(slice);
      setFuse(new Fuse(slice, { keys: columns }));

      if (currentPage <= 1) {
        usePaginator(pageSize);
      }
    }
  };

  const moveForward = () => {
    if (pageSize !== Infinity) {
      setCurrentPage(currentPage + 1);
      const startOfSlice = data.indexOf(dataSlice[0]) + pageSize;
      const endOfSlice = data.indexOf(dataSlice.at(-1)) + pageSize + 1;

      const slice = data.slice(startOfSlice, endOfSlice);
      setDataSlice(slice);
      setFuse(new Fuse(slice, { keys: columns }));

      if (currentPage >= numPages) {
        usePaginator(pageSize);
      }
    }
  };

  const getPages = () => {
    return pageSize === Infinity
      ? String.fromCodePoint(8734)
      : `${currentPage}/${numPages}`;
  };

  return (
    <div id="table">
      <div id="paginator">
        <button onClick={() => usePaginator(Infinity)}>All</button>
        <button onClick={() => usePaginator(100)}>100</button>
        <button onClick={() => usePaginator(10)}>10</button>
        {/* <form onSubmit={(e) => searchFor(e)}> */}
        <input
          id="query-input"
          type={"search"}
          placeholder="Search for a record"
          name="search"
          onChange={(box) => {
            searchFor(box.target.value);
          }}
        ></input>
        {/* </form> */}
        <button id="start-paginator-suite" onClick={() => moveForward()}>
          {String.fromCodePoint(8594)}
        </button>
        <div>{getPages()}</div>
        <button onClick={() => moveBackward()}>
          {String.fromCodePoint(8592)}
        </button>
      </div>
      <table className="styled-table">
        <thead>
          <tr>
            {columns.map((column, i) => (
              <td
                key={i}
                // onClick={(e) => clickHeader(column, e)}
                // id={`${column}-unsorted`}
              >
                {column}
              </td>
            ))}
          </tr>
        </thead>
        <tbody>
          {dataSlice.map((row, i) => (
            <TableRow
              row={row}
              index={i.toString()}
              columns={columns}
              key={i}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
