import "./Table.css";

type props = {
  data: Array<any>;
};

type Tr = {
  row: Object;
};

const TableRow = (props: Tr) => {
  const row = props.row;
  return (
    <tr>
      {Object.values(row).map((rowData) => (
        <td>{rowData}</td>
      ))}
    </tr>
  );
};

const Table = (props: props) => {
  const data = props.data;
  const columns = Object.keys(data[0]);
  console.log(columns);
  // const columnHelper = createColumnHelper();
  // const columns = Object.keys(props.data[0]).map(key => {
  //   columnHelper.accessor
  // })
  // const table = useReactTable({props.data, });
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
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <TableRow row={row} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
