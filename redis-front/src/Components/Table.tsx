import { useState } from "react";
import "./Table.css";

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
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(Infinity);
  const [dataSlice, setDataSlice] = useState(props.data);
  const [numPages, setNumPages] = useState(props.data.length);
  const data = props.data;
  const columns = Object.keys(data[0]);

  const usePaginator = (numRecords: number) => {
    switch (numRecords) {
      case Infinity:
        setCurrentPage(1);
        setPageSize(Infinity);
        setDataSlice(props.data);
        break;
      case 10:
        setCurrentPage(1);
        setPageSize(10);
        setNumPages(Math.ceil(data.length / 10));
        setDataSlice(props.data.slice(0, 10));
        break;
      case 100:
        setCurrentPage(1);
        setPageSize(100);
        setNumPages(Math.ceil(data.length / 100));
        setDataSlice(props.data.slice(0, 100));
        break;
      default:
        setCurrentPage(1);
        setPageSize(Infinity);
        setDataSlice(props.data);
    }
  };

  const moveBackward = () => {
    if (pageSize !== Infinity) {
      setCurrentPage(currentPage - 1);
      const startOfSlice = data.indexOf(dataSlice[0]) - pageSize;
      const endOfSlice = data.indexOf(dataSlice.at(-1)) - pageSize + 1;

      setDataSlice(data.slice(startOfSlice, endOfSlice));

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

      setDataSlice(data.slice(startOfSlice, endOfSlice));

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
        <button id="start-paginator-suite" onClick={() => moveForward()}>
          {String.fromCodePoint(8594)}
        </button>
        <div>{getPages()}</div>
        <button onClick={() => moveBackward()}>
          {String.fromCodePoint(8592)}
        </button>
      </div>
      <table>
        <thead>
          <tr>
            {columns.map((column, i) => (
              <td key={i}>{column}</td>
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
