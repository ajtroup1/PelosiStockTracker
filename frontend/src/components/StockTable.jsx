import React from "react";
import "../css/StockTable.css";
import ShowMore from "./ShowMore";

function StockTable({ stocks }) {

  return (
    <div className="stocks-table-container">
      <p>Pelosi's traded stocks</p>
      {/* Name (SYMBL) */}
      <table className="table" id="stocks-table">
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Trade type</th>
            <th>Sale/Purchase</th>
            <th>Trade date</th>
            <th>Trade price</th>
            <th>% since transaction</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock, index) => (
            <tr key={index}>
              <td><img src={stock.photo_url} id="stock-table-picture"/></td>
              <td>{`${stock.name} (${stock.stock_symbol})`}</td>
              <td>{stock.trade_type}</td>
              <td>{stock.transaction_type}</td>
              <td>{stock.trade_date}</td>
              <td>{stock.trade_price}</td>
              {parseFloat(stock.since_transaction) > 0 ? (
                <td style={{ color: "green" }}>{stock.since_transaction}</td>
              ) : (
                <td style={{ color: "red" }}>{stock.since_transaction}</td>
              )}
              {/* <td><p id="link" onClick={() => handleShowMore(stock.stock_symbol)}>Show more</p></td> */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StockTable;
