import ProductionStartForm from "./components/ProductionStartForm";
import ProductionCompletionForm from "./components/ProductionCompletionForm";
import ProductionList from "./components/ProductionList";
import CreateProductionOrder from "./components/CreateProductionOrder";

function App() {
  return (
    <div className="max-w-3xl mx-auto mt-10">
      <ProductionStartForm />
      <ProductionCompletionForm />
      <ProductionList />
      <CreateProductionOrder/> 
    </div>
  );
}

export default App;
