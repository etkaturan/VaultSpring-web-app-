import React, { useState, useEffect } from "react";
import AddSpendingForm from "./spendings-components/AddSpendingForm";
import axios from "axios";

const SpendingsBlock = ({ token }) => {
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/categories/nested/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setCategories(response.data);
      } catch (err) {
        setError("Failed to fetch categories.");
      }
    };

    fetchCategories();
  }, [token]);

  const handleAddSpending = async (newSpending) => {
    console.log("Payload sent to backend:", newSpending); // Debugging
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/spendings/",
        newSpending,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      console.log(response.data.message);
      alert("Spending added successfully!");
    } catch (err) {
      console.error("Error adding spending:", err.response?.data || err.message);
    }
  };
  

  return (
    <div className="bg-green-100 p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Spendings</h2>

      {error && <p className="text-red-500">{error}</p>}

      {/* Add Spending Form */}
      <AddSpendingForm categories={categories} handleAddSpending={handleAddSpending} />
    </div>
  );
};

export default SpendingsBlock;
