import React, { useState } from "react";
import Analytics from "./Analytics";

const AnalyticsButton = ({ token }) => {
  const [showAnalytics, setShowAnalytics] = useState(false);

  return (
    <div className="mt-4">
      <button
        onClick={() => setShowAnalytics((prev) => !prev)}
        className="bg-purple-500 text-white px-4 py-2 rounded shadow-md"
      >
        {showAnalytics ? "Hide Analytics" : "Show Analytics"}
      </button>

      {showAnalytics && <Analytics token={token} />}
    </div>
  );
};

export default AnalyticsButton;
