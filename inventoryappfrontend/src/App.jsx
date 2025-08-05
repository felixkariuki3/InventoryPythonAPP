import React from "react";
import {Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";

// Import your module components
import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import Production from "./pages/Production";
import Purchasing from "./pages/Purchasing";
import Finance from "./pages/Finance";
import Sales from "./pages/Sales";
import Reports from "./pages/Reports";

function App() {
  return (
    
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="production" element={<Production />} />
          <Route path="purchasing" element={<Purchasing />} />
          <Route path="finance" element={<Finance />} />
          <Route path="sales" element={<Sales/>} />
          <Route path="reports" element={<Reports/>} />
        </Route>
      </Routes>
    
  );
}

export default App;
