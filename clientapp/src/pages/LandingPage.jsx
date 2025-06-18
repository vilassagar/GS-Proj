import { Button } from "@/components/ui/button";
import ResolutionCard from "@/components/ui/ResolutionCard";
import { ChevronRight, Globe, Menu, Search } from "lucide-react";
import { useNavigate } from "react-router-dom";
// import Image from "next/image";

function HeroBanner() {
  return (
    <div className="relative bg-gradient-to-r from-amber-500 to-amber-600 py-12 md:py-16">
      <div className="absolute inset-0 bg-[url('/placeholder.svg?height=500&width=1000')] bg-cover bg-center opacity-10"></div>
      <div className="container mx-auto px-4">
        <div className="grid items-center gap-8 md:grid-cols-2">
          <div className="text-white">
            <h1 className="mb-4 text-3xl font-bold leading-tight md:text-4xl lg:text-5xl">
              सरकारी ठराव
            </h1>
            <p className="mb-6 text-lg md:text-xl">
              अधिकृत दस्तऐवज, धोरणे आणि सरकारी ठराव प्रवेश करा. नवीन निर्णय आणि
              उपक्रमांविषयी माहिती मिळवा.
            </p>
            <div className="flex flex-col space-y-3 sm:flex-row sm:space-x-4 sm:space-y-0">
              <a
                href="#"
                className="inline-flex items-center justify-center rounded-md bg-white px-5 py-2.5 text-sm font-medium text-amber-600 shadow-md hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-amber-500"
              >
                ठराव शोधा
              </a>
              <a
                href="#"
                className="inline-flex items-center justify-center rounded-md border border-white bg-transparent px-5 py-2.5 text-sm font-medium text-white hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-amber-500"
              >
                अधिक जाणून घ्या
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-sky-50">
      {/* शीर्षलेख */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="hidden md:block">
                <h1 className="text-xl font-bold text-slate-800">
                  शासकीय ठराव
                </h1>
                <p className="text-sm text-slate-600">अधिकृत दस्तऐवज संग्रह</p>
              </div>
            </div>
            <div>
              <Button
                className="mr-5"
                onClick={() => {
                  navigate("/register");
                }}
              >
                नोंदणी करा
              </Button>
              <Button
                onClick={() => {
                  navigate("/login");
                }}
              >
                प्रवेश करा / लॉगिन करा
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* मार्गदर्शक पट्टी */}

      <HeroBanner />

      {/* मुख्य मजकूर */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 rounded-lg bg-white p-6 shadow-md">
          <h2 className="mb-4 text-2xl font-bold text-slate-800">
            सद्यस्थितीतले ठराव
          </h2>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[
              {
                title: "शैक्षणिक धोरण अद्यतन",
                department: "शिक्षण",
                date: "१५ मार्च २०२५",
              },
              {
                title: "आरोग्य उपक्रम",
                department: "आरोग्य",
                date: "१२ मार्च २०२५",
              },
              {
                title: "पायाभूत सुविधा विकास",
                department: "शहरी विकास",
                date: "१० मार्च २०२५",
              },
              {
                title: "कृषी अनुदान",
                department: "कृषी",
                date: "०८ मार्च २०२५",
              },
              {
                title: "डिजिटल प्रशासन फ्रेमवर्क",
                department: "माहिती तंत्रज्ञान",
                date: "०५ मार्च २०२५",
              },
              {
                title: "पर्यावरण संरक्षण कायदा",
                department: "पर्यावरण",
                date: "०१ मार्च २०२५",
              },
            ].map((resolution, index) => (
              <ResolutionCard key={index} {...resolution} />
            ))}
          </div>
        </div>
      </main>

      {/* तळटीप */}
      <footer className="bg-slate-800 py-8 text-white">
        <div className="container mx-auto px-4">
          <div className="grid gap-8 md:grid-cols-4">
            <div>
              <h3 className="mb-3 text-lg font-semibold">आमच्याबद्दल</h3>
              <p className="text-sm text-slate-300">
                शासकीय ठराव आणि धोरण दस्तऐवजांसाठी अधिकृत पोर्टल. नवीन निर्णय
                आणि परिपत्रके पहा.
              </p>
            </div>

            <div>
              <h3 className="mb-3 text-lg font-semibold">महत्त्वाचे दुवे</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                {[
                  "गोपनीयता धोरण",
                  "वापरण्याच्या अटी",
                  "साइट नकाशा",
                  "सुलभता",
                  "संपर्क करा",
                ].map((a) => (
                  <li key={a}>
                    <a href="#" className="hover:text-amber-300">
                      {a}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="mt-8 border-t border-slate-700 pt-6 text-center text-sm text-slate-400">
            <p>© {new Date().getFullYear()} शासकीय पोर्टल. सर्व हक्क राखीव.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
