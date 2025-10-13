/* eslint-disable react/prop-types */
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Check, Eye, X } from "lucide-react";
function GramSevakTable({ data, onApprove, onView }) {
  return (
    <div className="border rounded-lg shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-slate-100">
              <TableHead className="font-semibold">पहिले</TableHead>
              <TableHead className="font-semibold">ई-मेल</TableHead>
              <TableHead className="font-semibold">ग्राम पंचायत</TableHead>
              <TableHead className="font-semibold">ब्लॉक</TableHead>
              <TableHead className="font-semibold">जिल्हा</TableHead>
              <TableHead className="font-semibold">सेवा आयडी</TableHead>
              <TableHead className="font-semibold">स्थिती</TableHead>
              <TableHead className="font-semibold text-center">
                क्रिया
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data && data.length > 0 ? (
              data.map((gramSevak, index) => (
                <TableRow
                  key={gramSevak.id || index}
                  className="hover:bg-slate-50"
                >
                  <TableCell className="font-medium">
                    {gramSevak.firstName || "-"} {gramSevak.lastName || "-"}
                  </TableCell>
                  <TableCell>{gramSevak.email || "-"}</TableCell>
                  <TableCell>{gramSevak.gramPanchayat || "-"}</TableCell>
                  <TableCell>{gramSevak.block || "-"}</TableCell>
                  <TableCell>{gramSevak.district || "-"}</TableCell>
                  <TableCell>{gramSevak.serviceId || "-"}</TableCell>
                  <TableCell>
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        gramSevak.isApproved
                          ? "bg-green-100 text-green-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {gramSevak.isApproved ? "मंजूर" : "प्रलंबित"}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center justify-center gap-2">
                      {!gramSevak.isApproved && (
                        <>
                          <Button
                            variant="outline"
                            size="sm"
                            className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                            onClick={() => onApprove(index, "APPROVED")}
                            title="मंजूर करा"
                          >
                            <Check className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                            onClick={() => onApprove(index, "REJECTED")}
                            title="नाकारा"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        className="h-8 w-8 p-0 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                        onClick={() => onView(index)}
                        title="तपशील पहा"
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={8}
                  className="h-24 text-center text-gray-500"
                >
                  कोणतेही परिणाम नाहीत
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
export default GramSevakTable;
