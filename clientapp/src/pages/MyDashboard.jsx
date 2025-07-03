import WithAuthLayout from "@/components/layout/WithAuthLayout";
function MyDashboard() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">My Dashboard</h1>
      <p className="text-gray-700">
        This is a placeholder for your dashboard content. You can add components
        and features as needed.
      </p>
      {/* Add more components or features here */}
    </main>
  );
}

export default WithAuthLayout(MyDashboard);
//   <h1 className="text-2xl font-bold mb-4">My Dashboard</h1>
