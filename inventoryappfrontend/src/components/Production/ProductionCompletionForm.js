import React, { useState } from "react";
import { completeProduction } from "../../api/production";

const ProductionCompletionForm = () => {
  const [orderId, setOrderId] = useState("");
  const [qty, setQty] = useState("");

  const handleComplete = async () => {
    try {
      await completeProduction(Number(orderId), Number(qty));
      alert("Production Completed Successfully");
    } catch (err) {
      console.error(err);
      alert("Failed to complete production");
    }
  };

  return (
    <div className="p-4 mt-4">
      <h2 className="text-xl font-bold mb-2">Complete Production</h2>
      <input
        className="border px-2 py-1 mr-2"
        type="number"
        placeholder="Order ID"
        value={orderId}
        onChange={(e) => setOrderId(e.target.value)}
      />
      <input
        className="border px-2 py-1 mr-2"
        type="number"
        placeholder="Quantity"
        value={qty}
        onChange={(e) => setQty(e.target.value)}
      />
      <button onClick={handleComplete} className="bg-green-600 text-white px-4 py-1 rounded">
        Complete
      </button>
    </div>
  );
};

export default ProductionCompletionForm;
