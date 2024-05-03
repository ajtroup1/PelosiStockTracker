import { useState, useEffect } from "react";
import "../css/PelosiProfile.css";

function PelosiProfile() {
  const [nancy, setNancy] = useState({});

  useEffect(() => {
    getNancy();
  }, []);

  const getNancy = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/nancypelosi");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const jsonData = await response.json();
      // console.log(jsonData);
      setNancy(jsonData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const ScrapeNancyPelosi = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/run-pelosi-bot`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      const jsonData = await response.json();
      fetchData();
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <>
      <div className="pelosi-profile-container">
        <div className="update-container">
          <img src="https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/sync-circle-blue-512.png" id="update-icon" onClick={ScrapeNancyPelosi}/>
          <p className="update-text">Update Nancy Pelosi</p>
        </div>
        <div className="img-container">
          <img src="../src/assets/pelosi-photo.png" id="pelosi-pic" />
        </div>
        <div className="info-container">
          <p>Net Worth: {nancy.net_worth}</p>
          <p>Trade Volume: {nancy.trade_volume}</p>
          <p>Total Trades: {nancy.total_trades}</p>
          <p>Last Traded: {nancy.last_traded}</p>
        </div>
      </div>
    </>
  );
}

export default PelosiProfile;
