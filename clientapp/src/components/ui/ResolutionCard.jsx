import { FileText, Calendar, Building, ChevronRight } from "lucide-react";

export default function ResolutionCard({ title, department, date }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition-all hover:shadow-md">
      <div className="mb-3 flex items-center text-amber-600">
        <FileText className="mr-2 h-5 w-5" />
        <span className="text-xs font-medium">Resolution</span>
      </div>

      <h3 className="mb-2 text-lg font-semibold text-slate-800">
        <a href="#" className="hover:text-amber-600">
          {title}
        </a>
      </h3>

      <div className="mb-3 space-y-1.5 text-sm text-slate-600">
        <div className="flex items-center">
          <Building className="mr-2 h-4 w-4 text-slate-400" />
          <span>{department}</span>
        </div>
        <div className="flex items-center">
          <Calendar className="mr-2 h-4 w-4 text-slate-400" />
          <span>{date}</span>
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <a
          href="#"
          className="inline-flex items-center text-sm font-medium text-amber-600 hover:text-amber-700"
        >
          View Details <ChevronRight className="ml-1 h-4 w-4" />
        </a>
      </div>
    </div>
  );
}
