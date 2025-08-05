import React from "react";
import CreateProductionOrder from "../components/Production/CreateProductionOrder";
import ProduProductionCompletionForm from "../components/Production/ProductionCompletionForm";
import ProductionList from "../components/Production/ProductionList";
import ProductionStartForm from "../components/Production/ProductionStartForm";

const Production = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4">Production Functions</h1>
      <CreateProductionOrder />
      <ProductionStartForm/>
      <ProduProductionCompletionForm/>
      <ProductionList/>
    </div>
  );
};

export default Production; 