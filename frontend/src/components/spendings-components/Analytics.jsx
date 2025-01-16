import React from "react";
import { Pie } from "react-chartjs-2";

const Analytics = ({ analytics, chartData }) => (
  <div className="mt-6 bg-white p-4 rounded shadow">
    <h3 className="text-lg font-bold mb-2">Analytics</h3>
    <Pie data={chartData} />
    <ul className="mt-4">
      {analytics.map((item) => (
        <li key={item.category} className="text-sm">
          <span className="font-bold">{item.category}:</span> {item.total_spent}{" "}
          {item.currency}
        </li>
      ))}
    </ul>
  </div>
);

export default Analytics;
