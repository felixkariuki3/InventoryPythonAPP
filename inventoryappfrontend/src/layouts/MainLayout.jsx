// Basic React + Tailwind frontend layout with sidebar, topbar, and module routing

import { Routes, Route, NavLink, Outlet } from "react-router-dom";
import { Home, Package, Settings, ShoppingCart } from "lucide-react";
import Production from "../pages/Production.jsx"; // adjust path as needed


const SidebarLayout = () => (
  <div className="flex min-h-screen bg-gray-100">
    <aside className="w-64 bg-white shadow-md">
      <div className="p-4 text-xl font-bold text-blue-600">FinanceApp</div>
      <nav className="flex flex-col gap-2 p-4">
        <NavItem name="Dashboard" to="/dashboard" icon={Home} />
        <NavItem name="Inventory" to="/inventory" icon={Package} />
        <NavItem name="Production" to="/production" icon={Package} />
        <NavItem name="Purchasing" to="/purchasing" icon={ShoppingCart} />
        <NavItem name="Sales" to="/sales" icon={Package} />
        <NavItem name="Finance" to="/finance" icon={Settings} />
        <NavItem name="Reports" to="/reports" icon={Settings} />
      </nav>
    </aside>

    <main className="flex-1 p-6">
      <Topbar />
      <div className="mt-6">
        <Outlet />
      </div>
    </main>
  </div>
);

const Topbar = () => (
  <div className="flex justify-between items-center p-4 bg-white rounded-xl shadow">
    <div>
      <h1 className="text-lg font-semibold">GegoHub Financials</h1>
      <p className="text-sm text-gray-500">Empowering Smart Decisions</p>
    </div>
    <div className="flex items-center gap-4">
      <span className="text-sm text-gray-700">Felix Kariuki</span>
      <img
        src="https://ui-avatars.com/api/?name=Felix+Kariuki"
        alt="Profile"
        className="w-8 h-8 rounded-full"
      />
    </div>
  </div>
);

const NavItem = ({ name, to, icon: Icon }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      `flex items-center gap-2 px-3 py-2 rounded hover:bg-blue-100 ${
        isActive ? "bg-blue-200 text-blue-700 font-semibold" : "text-gray-700"
      }`
    }
  >
    <Icon className="w-4 h-4" />
    {name}
  </NavLink>
);

const Dashboard = () => <div>Dashboard Page</div>;
const Inventory = () => <div>Inventory Module</div>;
const Purchasing = () => <div>Purchasing Module</div>;
const Sales = () => <div>Sales Module</div>;
const Finance = () => <div>Finance Module</div>;
const Reports = () => <div>Reports Module</div>;

export default function App() {
  return (
      <Routes>
        <Route path="/" element={<SidebarLayout />}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="production" element={<Production />} />
          <Route path="purchasing" element={<Purchasing />} />
          <Route path="sales" element={<Sales />} />
          <Route path="finance" element={<Finance />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
   
  );
}
