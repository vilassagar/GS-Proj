import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import WithLayout from "@/components/layout/WithLayout";
import { CategorySection, maharashtraGovCategories, SearchBar } from "./Books";

function Dashboard() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">
        महाराष्ट्र शासन पुस्तके आणि शासन निर्णय शोध
      </h1>
      <SearchBar />
      <div className="mt-12 space-y-8 flex w-full justify-center">
        <div>
          {maharashtraGovCategories.map((category) => (
            <CategorySection key={category.category} category={category} />
          ))}
        </div>
      </div>
    </main>
  );
}

export default WithAuthentication(
  WithPermission("home")(WithLayout(Dashboard))
);
