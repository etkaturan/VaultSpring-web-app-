import React from "react";

const AddCategoryModal = ({
  showModal,
  setShowModal,
  newCategory,
  setNewCategory,
  handleAddCategory,
  categories,
}) => {
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

  if (!showModal) return null;

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-lg font-bold mb-2">Add Category</h3>
        <input
          type="text"
          placeholder="Category Name"
          value={newCategory.name}
          onChange={(e) => setNewCategory({ ...newCategory, name: e.target.value })}
          className="border rounded px-2 py-1 mb-4 w-full"
        />
        <select
          value={newCategory.parent_id || ""}
          onChange={(e) =>
            setNewCategory({ ...newCategory, parent_id: e.target.value || null })
          }
          className="border rounded px-2 py-1 mb-4 w-full"
        >
          <option value="">Top-Level Category</option>
          {renderCategories(categories)}
        </select>
        <div className="flex gap-2">
          <button
            onClick={handleAddCategory}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Add
          </button>
          <button
            onClick={() => setShowModal(false)}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddCategoryModal;
