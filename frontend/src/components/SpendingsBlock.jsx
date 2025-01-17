import React, { useState, useEffect } from "react";
import AddSpendingForm from "./spendings-components/AddSpendingForm";
import SpendingsList from "./spendings-components/SpendingsList";
import AddCategoryModal from "./spendings-components/AddCategoryModal";
import AnalyticsButton from "./spendings-components/AnalyticsButton";
import axios from "axios";

const SpendingsBlock = ({ token }) => {
  const [categories, setCategories] = useState([]);
  const [spendings, setSpendings] = useState([]);
  const [error, setError] = useState(null);

  const fetchCategories = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/api/categories/nested/",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setCategories(response.data);
    } catch (err) {
      setError("Failed to fetch categories.");
    }
  };

  useEffect(() => {
    fetchCategories();
  }, [token]);

  const fetchSpendings = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/api/spendings/",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setSpendings(response.data);
    } catch (err) {
      setError("Failed to fetch spendings.");
    }
  };

  useEffect(() => {
    fetchSpendings();
  }, [token]);

  const handleAddSpending = async (newSpending) => {
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
      fetchSpendings();
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

      {/* Add Category Modal */}
      <AddCategoryModal
        token={token}
        onCategoryAdded={fetchCategories}
        categories={categories}
      />

      {/* Spendings List */}
      <SpendingsList spendings={spendings} categories={categories} />

      {/* Analytics Button */}
      <AnalyticsButton token={token} />
    </div>
  );
};

export default SpendingsBlock;
