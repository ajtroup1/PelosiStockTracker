import React, { useEffect, useState } from "react";
import "../css/App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import StockTable from "./StockTable.jsx";
import PelosiProfile from "./PelosiProfile.jsx";
import Navbar from "./Navbar.jsx";
import HighPerfStock from "./HighPerfStock.jsx";
import PieChart from "./PieChart.jsx";
import ShowMore from "./ShowMore.jsx";

function App() {
  const [stocks, setStocks] = useState([]);
  const [stockSymbol, setStockSybmol] = useState(null);
  const [displayMore, setDisplayMore] = useState(false);

  useEffect(() => {
    getStocks();
  }, []);

  const getStocks = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/pelositrades");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const jsonData = await response.json();
      // console.log(jsonData);
      setStocks(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    setDisplayMore(true);
  }, [stockSymbol]);

  const handleShowMore = (stock_symbol) => {
    setStockSybmol(stock_symbol);
  };

  return (
    <>
      <div className="main-app">
        <Navbar />
        <PelosiProfile />
        <PieChart />
        <HighPerfStock />
        <StockTable stocks={stocks} />
        {!displayMore ? <ShowMore stock_symbol={stockSymbol} /> : <p></p>}
      </div>
    </>
  );
}

export default App;
