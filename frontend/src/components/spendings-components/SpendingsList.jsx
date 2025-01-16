import React from "react";

const SpendingsList = ({ spendings }) => {
  return (
    <div className="space-y-4">
      {spendings.map((spending) => (
        <div
          key={spending.id}
          className="p-4 bg-white rounded shadow flex justify-between items-center"
        >
          <div>
            <p className="font-bold">{spending.description || "No description"}</p>
            <p className="text-sm text-gray-600">
              {spending.category}
              {spending.subcategory && ` > ${spending.subcategory}`}
            </p>
            <p className="text-sm text-gray-500">Date: {spending.date}</p>
          </div>
          <p className="text-lg font-semibold">
            {spending.amount} {spending.currency}
          </p>
        </div>
      ))}
    </div>
  );
};

export default SpendingsList;
