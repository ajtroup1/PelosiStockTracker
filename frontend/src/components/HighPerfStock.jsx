import { useState, useEffect } from "react";
import { LineChart } from "@mui/x-charts";

import "../css/HighPerfStock.css";

function HighPerfStock() {
  const [stock, setStock] = useState({});
  const [histData, setHistData] = useState([]);
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getStock();
  }, []);

  const getStock = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/highest-stock");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const jsonData = await response.json();
      setStock(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    if (Object.keys(stock).length > 0) {
      getHistData();
    }
  }, [stock]);

  // useEffect(() => {
  //   setLoading(false)
  // }, [histData]);

  const getHistData = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/historicaldata/${stock.stock_symbol}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const jsonData = await response.json();
      console.log(jsonData)
      setHistData(jsonData);
      setLoading(false)
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const formatDate = (key) => {
    return key
  }; //incredible coding right here


  if (loading) {
    return <h1>Loading</h1>;
  } else {
    return (
      <>
        <div className="high-stock-container">
          <p className="line-head">{stock.name}</p>
          <p className="line-head">Stock price over the last 8 months</p>
          <div className="line-chart-container">
            <LineChart
              xAxis={[
                {
                  data: histData.map((data, key) => formatDate(key)),
                },
              ]}
              series={[
                {
                  data: histData.map((data) =>
                    parseFloat(data.close.replace(",", ""))
                  ),
                  area: true,
                },
              ]}
              width={550}
              height={200}
              className="line-chart"
            />
          </div>
        </div>
      </>
    );
  }
}

export default HighPerfStock;
