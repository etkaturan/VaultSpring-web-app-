import React from "react";

const AnalyticsButton = ({ fetchAnalytics }) => (
  <button
    onClick={fetchAnalytics}
    className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
  >
    View Analytics
  </button>
);

export default AnalyticsButton;
