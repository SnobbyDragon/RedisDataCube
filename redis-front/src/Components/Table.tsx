import React from "react";
import { useReactTable } from "@tanstack/react-table";

type props = {
  columns: Array<String>;
  rows: Array<Map<String, String>>;
};

const Table = (props: props) => {
  const columns: ColumnDef<TData> = props.columns;
  const table = useReactTable();
  // const columns: Array<String> = props.columns;
  // const rows: Array<Map<String, String>> = props.rows;
  return (
    <div id="table">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <td>{column}</td>
            ))}
            <td>Key</td>
            <td>Value</td>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => {
            return (
              <tr key={i}>
                {[row.values()].map((rowData) => (
                  <td>{rowData}</td>
                ))}
                <td></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
// {rows.map((row, i) => {
//   <tr key={i}>
//   {[...row.values()].forEach(data => {
//     return <td>{data}</td>
//   })}
// })}
// </tr>

export default Table;
