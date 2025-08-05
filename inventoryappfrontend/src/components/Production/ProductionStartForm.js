import React, { useState } from "react";
import { startProduction } from "../../api/production";

const ProductionStartForm = () => {
  const [orderId, setOrderId] = useState("");

  const handleStart = async () => {
    try {
      await startProduction(Number(orderId));
      alert("Production Started Successfully");
    } catch (err) {
      console.error(err);
      alert("Failed to start production");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Start Production</h2>
      <input
        className="border px-2 py-1 mr-2"
        type="number"
        placeholder="Order ID"
        value={orderId}
        onChange={(e) => setOrderId(e.target.value)}
      />
      <button onClick={handleStart} className="bg-blue-600 text-white px-4 py-1 rounded">
        Start
      </button>
    </div>
  );
};

export default ProductionStartForm;
