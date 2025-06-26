import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import WithLayout from "@/components/layout/WithLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import RButton from "@/components/ui/rButton";
import { RPagination } from "@/components/ui/RPagination";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { getDocumentList } from "@/services/documentList/getDocumentList";
import { Download, EyeIcon } from "lucide-react";
import { useEffect, useState } from "react";

function Dashboard() {
  const [formData, setFormData] = useState({
    docType: null,
  });
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [documents, setDocuments] = useState([]);

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  // const paginatedDocs = filteredDocs.slice(indexOfFirstItem, indexOfLastItem);

  useEffect(() => {
    fetchDocumentList();
  }, []);
  useEffect(() => {
    if (
      !documents ||
      !Array.isArray(documents.books) ||
      !Array.isArray(documents.grs)
    )
      return;

    const newDocs =
      filter === "all"
        ? [...documents.books, ...documents.grs]
        : filter === "book"
        ? documents.books
        : documents.grs;

    setDocuments(newDocs);
  }, [filter, documents]);

  const fetchDocumentList = async () => {
    try {
      const response = await getDocumentList();

      setDocuments(response.data);
    } catch (error) {}
  };

  const handleChange = (name) => async (e) => {
    let nextState = produce(formData, (draft) => {
      switch (name) {
        case "docType":
          draft[name] = e.target.value;
          break;

        default:
          break;
      }
    });
    setFormData(nextState);
  };

  const handleChangeFilter = (value) => {
    setFilter(value);
  };

  const handleSearch = (e) => {
    setSearch(e.target.value);
  };

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">
        महाराष्ट्र शासन पुस्तके आणि शासन निर्णय शोध
      </h1>
      <div className="flex gap-2">
        <div className="w-1/4">
          {/* <Label htmlFor="docType">
            पदनाम <span className="text-red-500 ml-1">*</span>
          </Label> */}
          <Select value={filter} onValueChange={handleChangeFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="प्रकारानुसार फिल्टर करा" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">सर्व कागदपत्रे</SelectItem>
              <SelectItem value="book">पुस्तके</SelectItem>
              <SelectItem value="gr">शासकीय ठराव</SelectItem>
            </SelectContent>
          </Select>
        </div>
        {/* <div className="ml-0"> */}
        <Input
          placeholder="कागदपत्रे शोधा..."
          className="pl-4"
          value={search}
          onChange={handleSearch}
        />
        <Button
          variant="outline"
          // onClick={handleApprove(index, "APPROVED")}
        >
          Clear
        </Button>
        <Button
          variant="outline"
          // onClick={handleApprove(index, "APPROVED")}
        >
          Search
        </Button>

        {/* </div> */}
      </div>
      <div className="mt-12 space-y-0 flex w-full justify-center">
        <div className="flex justify-between ">
          {/* <h3 className="text-2xl font-bold mb-5">{filter}</h3> */}
        </div>

        <div className="border rounded-lg shadow-lg border-gray-200 max-h-[500px] overflow-y-auto">
          <Table className="min-w-full table-fixed">
            <TableHeader className="sticky top-0 bg-white z-10 shadow-sm">
              <TableRow>
                <TableHead className="p-2">कागदपत्राचे नाव</TableHead>
                <TableHead className="p-2">कागदपत्रांचे प्रकार</TableHead>

                <TableHead className="p-2">वर्णन</TableHead>
                <TableHead className="w-[150px] p-2">क्रिया</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {documents?.length ? (
                documents?.map((doc, index) => (
                  <TableRow key={doc?.id}>
                    <TableCell className="p-2">{doc.legaldocname}</TableCell>
                    <TableCell className="p-2">{doc.docType}</TableCell>
                    <TableCell className="p-2">{doc.description}</TableCell>
                    <TableCell className="p-2">
                      <div className="flex">
                        <RButton
                          variant="ghost"
                          className="flex items-center gap-2 "
                          // onClick={handleViewBlocks(district?.districtId)}
                        >
                          <EyeIcon className="h-4 w-4" />
                        </RButton>
                        <RButton
                          variant="ghost"
                          className="flex items-center gap-2 "
                          // onClick={handleViewBlocks(district?.districtId)}
                        >
                          <Download size={20} />
                        </RButton>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center">
                    कोणतेही परिणाम नाहीत.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
        <div className="mt-4 flex justify-center">
          <RPagination
            // totalItems={filteredDocs.length}
            itemsPerPage={itemsPerPage}
            currentPage={currentPage}
            onPageChange={setCurrentPage}
          />
        </div>
      </div>
    </main>
  );
}

export default WithAuthentication(
  WithPermission("home")(WithLayout(Dashboard))
);
