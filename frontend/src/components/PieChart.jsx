import { useState, useEffect } from "react";
import { PieChart } from "@mui/x-charts";
import "../css/PieChart.css";
import { Hidden } from "@mui/material";

function PieChartx() {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getSectorCuts();
  }, []);

  const getSectorCuts = async () => {
    try {
      setIsLoading(true);

      const response = await fetch(
        `http://127.0.0.1:8000/api/get-sector-cuts`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      const jsonData = await response.json();
      console.log(jsonData);

      // Transform JSON data into array of series objects required by PieChart component
      const seriesData = Object.entries(jsonData).map(
        ([label, value], index) => ({
          id: index,
          value,
          label,
        })
      );

      const pieData = [{ data: seriesData }]; // Wrap seriesData in an array
      console.log("pie data:", pieData);

      setData(pieData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <h1>Loading</h1>; // Return loading indicator if data is still loading
  } else {
    return (
      <>
        <div className="pie-container">
          <div className="line-head-pie">
            <p>Portfolio Cuts</p>
          </div>
          <div className="pie-chart-container">
            <PieChart series={data} width={300} height={150} />
          </div>
        </div>
      </>
    );
  }
}

export default PieChartx;
