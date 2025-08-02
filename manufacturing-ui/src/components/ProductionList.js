import React, { useEffect, useState } from "react";
import axios from "axios";

const ProductionList = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/production/")
      .then((res) => setOrders(res.data))
      .catch((err) => {
        console.error(err);
        alert("Failed to fetch production orders");
      });
  }, []);

  return (
    <div className="p-4 mt-4">
      <h2 className="text-xl font-bold mb-2">Production Orders</h2>
      {orders.length === 0 ? (
        <p>No production orders found.</p>
      ) : (
        <table className="min-w-full border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-4 py-2">ID</th>
              <th className="border px-4 py-2">Item</th>
              <th className="border px-4 py-2">Qty</th>
              <th className="border px-4 py-2">Status</th>
              <th className="border px-4 py-2">Start</th>
              <th className="border px-4 py-2">End</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td className="border px-4 py-1">{order.id}</td>
                <td className="border px-4 py-1">{order.item_id}</td>
                <td className="border px-4 py-1">{order.quantity}</td>
                <td className="border px-4 py-1">{order.status}</td>
                <td className="border px-4 py-1">{order.start_date || "-"}</td>
                <td className="border px-4 py-1">{order.end_date || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ProductionList;
