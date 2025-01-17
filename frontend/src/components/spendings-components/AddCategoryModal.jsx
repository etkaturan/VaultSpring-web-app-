import React, { useState, useEffect } from "react";
import axios from "axios";

const AddCategoryModal = ({ token, onCategoryAdded, categories }) => {
  const [showModal, setShowModal] = useState(false);
  const [categoryName, setCategoryName] = useState("");
  const [parentCategory, setParentCategory] = useState("");
  const [error, setError] = useState(null);

  const handleAddCategory = async () => {
    if (!categoryName) {
      setError("Category name is required.");
      return;
    }

    try {
      const parentCategoryId = parentCategory || null;

      const payload = {
        name: categoryName,
        parent_id: parentCategoryId,
      };

      const response = await axios.post(
        "http://127.0.0.1:5000/api/categories/",
        payload,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      console.log(response.data.message);
      onCategoryAdded(); // Refresh categories in SpendingsBlock
      setShowModal(false);
      setCategoryName("");
      setParentCategory("");
    } catch (err) {
      setError("Failed to add category. Please try again.");
    }
  };

  return (
    <div>
      <button
        onClick={() => setShowModal(true)}
        className="bg-blue-500 text-white px-4 py-2 rounded shadow-md"
      >
        Add Category
      </button>

      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
          <div className="bg-white p-6 rounded shadow-md w-96">
            <h2 className="text-lg font-semibold mb-4">Add Category</h2>

            {error && <p className="text-red-500 mb-2">{error}</p>}

            {/* Category Name Input */}
            <div className="mb-4">
              <label htmlFor="categoryName" className="block font-medium">
                Category Name
              </label>
              <input
                type="text"
                id="categoryName"
                value={categoryName}
                onChange={(e) => setCategoryName(e.target.value)}
                className="border rounded px-2 py-1 w-full"
              />
            </div>

            {/* Parent Category Dropdown */}
            <div className="mb-4">
              <label htmlFor="parentCategory" className="block font-medium">
                Parent Category (Optional)
              </label>
              <select
                id="parentCategory"
                value={parentCategory}
                onChange={(e) => setParentCategory(e.target.value)}
                className="border rounded px-2 py-1 w-full"
              >
                <option value="">None</option>
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex justify-end">
              <button
                onClick={handleAddCategory}
                className="bg-green-500 text-white px-4 py-2 rounded mr-2"
              >
                Add
              </button>
              <button
                onClick={() => setShowModal(false)}
                className="bg-red-500 text-white px-4 py-2 rounded"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AddCategoryModal;
