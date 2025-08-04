import React, { useState } from "react";
import axios from "axios";

const CreateProductionOrder = () => {
  const [itemId, setItemId] = useState("");
  const [quantity, setQuantity] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://localhost:8000/production/", {
        item_id: parseInt(itemId),
        quantity: parseFloat(quantity),
      });

      alert("Production order created successfully!");
      setItemId("");
      setQuantity("");
    } catch (err) {
      console.error(err);
      alert("Failed to create production order.");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-4 border rounded mb-4 shadow-sm bg-white"
    >
      <h2 className="text-lg font-semibold mb-2">Create Production Order</h2>

      <div className="mb-2">
        <label className="block text-sm font-medium">Item ID</label>
        <input
          type="number"
          value={itemId}
          onChange={(e) => setItemId(e.target.value)}
          className="w-full border px-3 py-1 rounded"
          required
        />
      </div>

      <div className="mb-2">
        <label className="block text-sm font-medium">Quantity</label>
        <input
          type="number"
          step="0.01"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          className="w-full border px-3 py-1 rounded"
          required
        />
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
      >
        Create
      </button>
    </form>
  );
};

export default CreateProductionOrder;
