import React, { useState, useEffect } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";

// Register required components
ChartJS.register(ArcElement, Tooltip, Legend, Title);

const Analytics = ({ token }) => {
  const [analytics, setAnalytics] = useState([]);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(
    new Date().toISOString().split("T")[0] // Default to today's date
  );
  const [endDate, setEndDate] = useState(
    new Date().toISOString().split("T")[0] // Default to today's date
  );

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/spendings/analytics/", {
          headers: { Authorization: `Bearer ${token}` },
          params: {
            start_date: startDate,
            end_date: endDate,
          },
        });
        setAnalytics(response.data);
      } catch (err) {
        setError("Failed to fetch analytics.");
        console.error(err.response?.data || err.message);
      }
    };

    fetchAnalytics();
  }, [token, startDate, endDate]);

  const data = {
    labels: analytics.map((item) => item.category),
    datasets: [
      {
        label: "Total Spendings",
        data: analytics.map((item) => item.total_spent),
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
        hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
      },
    ],
  };

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Analytics</h2>
      {error && <p className="text-red-500">{error}</p>}

      <div className="flex gap-2 mb-4">
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="border rounded px-2 py-1"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="border rounded px-2 py-1"
        />
      </div>

      {analytics.length > 0 ? (
        <>
          <Pie data={data} />
          <ul className="mt-4">
            {analytics.map((item) => (
              <li key={item.category} className="mb-2">
                <strong>{item.category}:</strong> {item.total_spent.toFixed(2)}{" "}
                {item.currency}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p>No analytics data available.</p>
      )}
    </div>
  );
};

export default Analytics;
