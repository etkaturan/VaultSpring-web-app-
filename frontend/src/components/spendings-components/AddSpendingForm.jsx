import React, { useState } from "react";

const AddSpendingForm = ({ categories, handleAddSpending }) => {
  const [newSpending, setNewSpending] = useState({
    category_id: "",
    amount: "",
    currency: "USD",
    description: "",
    date: new Date().toISOString().split("T")[0],
  });

  const renderCategories = (categories) =>
    categories.map((category) => (
      <optgroup key={category.id} label={category.name}>
        {category.subcategories.map((sub) => (
          <option key={sub.id} value={sub.id}>
            {sub.name}
          </option>
        ))}
      </optgroup>
    ));

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validation
    if (!newSpending.category_id || !newSpending.amount || !newSpending.date) {
      alert("Please fill in all required fields.");
      return;
    }

    const spendingData = {
      ...newSpending,
      amount: parseFloat(newSpending.amount), // Convert amount to number
    };

    handleAddSpending(spendingData);

    // Reset form
    setNewSpending({
      category_id: "",
      amount: "",
      currency: "USD",
      description: "",
      date: new Date().toISOString().split("T")[0],
    });
  };

  return (
    <div className="mt-6 bg-white p-4 rounded shadow">
      <h3 className="text-lg font-bold mb-2">Add Spending</h3>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <select
          value={newSpending.category_id}
          onChange={(e) =>
            setNewSpending({ ...newSpending, category_id: e.target.value })
          }
          className="border rounded px-2 py-1"
          required
        >
          <option value="">Select Category</option>
          {renderCategories(categories)}
        </select>
        <input
          type="number"
          placeholder="Amount"
          value={newSpending.amount}
          onChange={(e) => setNewSpending({ ...newSpending, amount: e.target.value })}
          className="border rounded px-2 py-1"
          required
        />
        <select
          value={newSpending.currency}
          onChange={(e) =>
            setNewSpending({ ...newSpending, currency: e.target.value })
          }
          className="border rounded px-2 py-1"
        >
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="KZT">KZT</option>
        </select>
        <input
          type="text"
          placeholder="Description"
          value={newSpending.description}
          onChange={(e) =>
            setNewSpending({ ...newSpending, description: e.target.value })
          }
          className="border rounded px-2 py-1"
        />
        <input
          type="date"
          value={newSpending.date}
          onChange={(e) => setNewSpending({ ...newSpending, date: e.target.value })}
          className="border rounded px-2 py-1"
          required
        />
        <button
          type="submit"
          className="mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Add Spending
        </button>
      </form>
    </div>
  );
};

export default AddSpendingForm;
