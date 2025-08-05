import React, { useState } from "react";
import axios from "axios";

const CreateProductionOrder = () => {
  const [itemId, setItemId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [operations, setOperations] = useState([
  { name: "", sequence: 1, duration_minutes: 0 }
  ]);

const addOperation = () => {
  setOperations([...operations, { name: "", sequence: operations.length + 1, duration_minutes: 0 }]);
};

const updateOperation = (index, updatedOp) => {
  const newOps = [...operations];
  newOps[index] = updatedOp;
  setOperations(newOps);
};

const removeOperation = (index) => {
  const newOps = operations.filter((_, i) => i !== index);
  setOperations(newOps);
};

{operations.map((op, index) => (
  <div key={index} className="mb-4 p-2 border rounded">
    <input
      type="text"
      placeholder="Operation Name"
      value={op.name}
      onChange={(e) =>
        updateOperation(index, { ...op, name: e.target.value })
      }
      className="border p-2 mr-2"
    />
    <input
      type="number"
      placeholder="Sequence"
      value={op.sequence}
      onChange={(e) =>
        updateOperation(index, { ...op, sequence: parseInt(e.target.value) })
      }
      className="border p-2 mr-2"
    />
    <input
      type="number"
      placeholder="Duration (mins)"
      value={op.duration_minutes}
      onChange={(e) =>
        updateOperation(index, { ...op, duration_minutes: parseFloat(e.target.value) })
      }
      className="border p-2 mr-2"
    />
    <button onClick={() => removeOperation(index)} className="text-red-500">
      Remove
    </button>
  </div>
))}
<button
  onClick={addOperation}
  className="bg-blue-500 text-white px-3 py-1 rounded mb-4"
>
  + Add Operation
</button>


const handleSubmit = async () => {
  try {
    const payload = {
      item_id: parseInt(itemId),
      quantity: parseFloat(quantity),
      operations: operations.filter(op => op.name.trim()) // remove empty ops
    };
    await axios.post("http://localhost:8000/production/", payload);
    alert("Production order created!");
  } catch (error) {
    console.error("Submission failed", error);
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
