import WithLayout from "@/components/layout/WithLayout";
import { useState } from "react";
import { Search, Download } from "lucide-react";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";

export function MaterialCard({ material }) {
  const handleDownload = () => {
    console.log("डाउनलोड करत आहे:", material.title);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md flex justify-between items-center">
      <div>
        <h3 className="font-semibold">{material.title}</h3>
        <p className="text-sm text-gray-500 capitalize">
          {material.type === "book" ? "अधिकृत दस्तऐवज" : "शासन निर्णय"}
        </p>
      </div>
      <button
        onClick={handleDownload}
        className="text-blue-500 hover:text-blue-700 transition-colors"
        aria-label={`डाउनलोड करा ${material.title}`}
      >
        <Download size={20} />
      </button>
    </div>
  );
}

export function CategorySection({ category }) {
  const getCategoryDescription = (categoryName) => {
    switch (categoryName) {
      case "सामान्य प्रशासन":
        return "महाराष्ट्राच्या एकूण प्रशासकीय धोरणे आणि नियमावली.";
      case "शहरी विकास":
        return "महाराष्ट्रातील शहरी क्षेत्रांसाठी मार्गदर्शक तत्त्वे आणि योजना.";
      case "ग्रामीण विकास":
        return "महाराष्ट्रातील ग्रामीण विकासासाठी योजना आणि उपक्रम.";
      case "शिक्षण":
        return "महाराष्ट्रातील शैक्षणिक धोरणे आणि कार्यक्रम.";
      case "सार्वजनिक आरोग्य":
        return "महाराष्ट्रातील सार्वजनिक आरोग्य सुधारण्यासाठी नियम आणि उपक्रम.";
      default:
        return "महाराष्ट्र शासनासाठी महत्त्वाचे दस्तऐवज आणि शासन निर्णय.";
    }
  };

  return (
    <section>
      <h2 className="text-2xl font-semibold my-5">{category.category}</h2>
      <p className="text-gray-600 mb-4">
        {getCategoryDescription(category.category)}
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {category.materials.map((material) => (
          <MaterialCard key={material.id} material={material} />
        ))}
      </div>
    </section>
  );
}

export function SearchBar() {
  const [query, setQuery] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    console.log("शोधत आहे:", query);
  };

  return (
    <form onSubmit={handleSearch} className="w-full max-w-3xl mx-auto">
      <div className="relative">
        <input
          type="text"
          placeholder="पुस्तके आणि शासन निर्णय शोधा..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full px-4 py-3 pr-12 text-lg border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
        >
          <Search size={24} />
        </button>
      </div>
    </form>
  );
}

export const maharashtraGovCategories = [
  {
    category: "सामान्य प्रशासन",
    materials: [
      { id: 1, title: "महाराष्ट्र नागरी सेवा नियम", type: "book" },
      { id: 2, title: "शासन निर्णय: ई-शासन अंमलबजावणी", type: "gr" },
    ],
  },
  {
    category: "शहरी विकास",
    materials: [
      { id: 3, title: "महाराष्ट्र प्रादेशिक व नगररचना अधिनियम", type: "book" },
      { id: 4, title: "शासन निर्णय: स्मार्ट सिटी मिशन महाराष्ट्र", type: "gr" },
    ],
  },
  {
    category: "ग्रामीण विकास",
    materials: [
      { id: 5, title: "महाराष्ट्र ग्रामपंचायत अधिनियम", type: "book" },
      { id: 6, title: "शासन निर्णय: मनरेगा अंमलबजावणी महाराष्ट्र", type: "gr" },
    ],
  },
  {
    category: "शिक्षण",
    materials: [
      { id: 7, title: "महाराष्ट्र शैक्षणिक संस्था अधिनियम", type: "book" },
      {
        id: 8,
        title: "शासन निर्णय: मध्याह्न भोजन योजना अंमलबजावणी",
        type: "gr",
      },
    ],
  },
  {
    category: "सार्वजनिक आरोग्य",
    materials: [
      { id: 9, title: "महाराष्ट्र सार्वजनिक आरोग्य अधिनियम", type: "book" },
      { id: 10, title: "शासन निर्णय: कोविड-१९ लसीकरण मोहीम", type: "gr" },
    ],
  },
];

function Books() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">
        महाराष्ट्र शासन पुस्तके आणि शासन निर्णय शोध
      </h1>
      <SearchBar />
      <div className="mt-12 space-y-8">
        {maharashtraGovCategories.map((category) => (
          <CategorySection key={category.category} category={category} />
        ))}
      </div>
    </main>
  );
}

export default WithAuthentication(WithPermission("books")(WithLayout(Books)));
