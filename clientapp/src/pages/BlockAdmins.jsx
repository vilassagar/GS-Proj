import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";

import WithLayout from "@/components/layout/WithLayout";
import { Combobox } from "@/components/ui/comboBox";
import RButton from "@/components/ui/rButton";
import { toast } from "@/components/ui/use-toast";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import RSelect from "@/components/ui/RSelect";
import { Button } from "@/components/ui/button";

import { getBlockAdmins, getUsers, updateBlockAdmin } from "@/services/block";
import { getDistricts } from "@/services/preset";
import { produce } from "immer";
import { FilePenIcon, Search, ChevronLeft, ChevronRight } from "lucide-react";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import { useNavigate, useLocation } from "react-router-dom";

function BlockAdmins() {
  const navigate = useNavigate();
  const location = useLocation();

  const [blocks, setBlocks] = useState([]);
  const [admins, setAdmins] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [isSearching, setIsSearching] = useState(false);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [totalBlocks, setTotalBlocks] = useState(0);

  const totalPages = Math.ceil(totalBlocks / pageSize);

  // Fetch blocks for a district with pagination and search
  const fetchBlocksForDistrict = async (districtId, page = 1, search = "") => {
    try {
      setIsSearching(true);
      const blocksResponse = await getBlockAdmins(
        districtId,
        search,
        page,
        pageSize
      );

      if (blocksResponse?.status === "success") {
        const responseData = blocksResponse.data;
        setBlocks(
          Array.isArray(responseData.data)
            ? responseData.data
            : Array.isArray(responseData)
            ? responseData
            : []
        );
        setTotalBlocks(
          responseData.total ||
            responseData.data?.length ||
            responseData.length ||
            0
        );
      } else {
        setBlocks([]);
        setTotalBlocks(0);
      }
    } catch (error) {
      console.error("Error fetching blocks:", error);
      toast({
        title: "त्रुटी",
        description: "ब्लॉक्स लोड करताना त्रुटी आली",
        variant: "destructive",
      });
      setBlocks([]);
      setTotalBlocks(0);
    } finally {
      setIsSearching(false);
    }
  };

  // Initialize from query params
  useEffect(() => {
    (async () => {
      try {
        setLoading(true);

        // Fetch districts
        const districtsResponse = await getDistricts();
        const districtsList = districtsResponse?.data || [];
        setDistricts(districtsList);

        // Get districtId from query params
        const params = new URLSearchParams(location.search);
        const districtIdFromUrl = params.get("districtId");

        // Select district (from URL or first district)
        let districtToSelect = null;
        if (districtIdFromUrl) {
          districtToSelect = districtsList.find(
            (d) => d.districtId === parseInt(districtIdFromUrl)
          );
        }
        if (!districtToSelect && districtsList.length > 0) {
          districtToSelect = districtsList[0];
        }

        if (districtToSelect) {
          setSelectedDistrict(districtToSelect);
          // Fetch blocks for selected district with initial page
          await fetchBlocksForDistrict(districtToSelect.districtId, 1, "");
        }
      } catch (error) {
        console.error("Error loading data:", error);
        toast({
          title: "त्रुटी",
          description: "डेटा लोड करताना त्रुटी आली",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  // Handle district change
  const handleDistrictChange = async (district) => {
    setSelectedDistrict(district);
    setSearchTerm("");
    setSearchInput("");
    setCurrentPage(1);

    // Update URL query params
    const params = new URLSearchParams(location.search);
    params.set("districtId", district.districtId);
    navigate(`${location.pathname}?${params.toString()}`, { replace: true });

    // Fetch blocks for new district
    await fetchBlocksForDistrict(district.districtId, 1, "");
  };

  // Handle search button click
  const handleSearch = async () => {
    if (!selectedDistrict) {
      toast({
        title: "सूचना",
        description: "कृपया प्रथम जिल्हा निवडा",
        variant: "default",
      });
      return;
    }

    setSearchTerm(searchInput);
    setCurrentPage(1);
    await fetchBlocksForDistrict(selectedDistrict.districtId, 1, searchInput);
  };

  // Handle page change
  const handlePageChange = async (newPage) => {
    if (newPage < 1 || newPage > totalPages) return;

    setCurrentPage(newPage);
    await fetchBlocksForDistrict(
      selectedDistrict.districtId,
      newPage,
      searchTerm
    );
  };

  // Handle page size change
  const handlePageSizeChange = async (newPageSize) => {
    setPageSize(newPageSize);
    setCurrentPage(1);
    if (selectedDistrict) {
      await fetchBlocksForDistrict(selectedDistrict.districtId, 1, searchTerm);
    }
  };

  // Handle Enter key in search input
  const handleSearchKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  // Handle edit block admin
  const handleEditBlockAdmin = (blockIndex) => async (e) => {
    const block = blocks[blockIndex];

    let nextState = produce(blocks, (draft) => {
      if (draft[blockIndex].hasOwnProperty("isEditMode")) {
        draft[blockIndex]["isEditMode"] = !draft[blockIndex]["isEditMode"];
      } else {
        draft[blockIndex]["isEditMode"] = true;
      }
    });

    let adminResponse = await getUsers(block?.blockId);
    setAdmins(adminResponse.data);

    setBlocks(nextState);
  };

  // Handle set block admin
  const handleSetBlockAdmin = (index) => async (e) => {
    const block = blocks[index];
    let response = await updateBlockAdmin(block?.blockId, e);

    if (response.status === "success") {
      let nextState = produce(blocks, (draft) => {
        draft[index]["admin"] = e;
        draft[index]["isEditMode"] = false;
      });

      setBlocks(nextState);
      toast({
        title: "यशस्वी",
        description: "ब्लॉक प्रशासक अद्यतनित केला",
      });
    } else {
      toast({
        title: "त्रुटी",
        description: "ब्लॉक प्रशासक अद्यतनित करू शकत नाही",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">लोड करत आहे...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between mb-5">
        <h1 className="text-2xl font-bold">ब्लॉक व्यवस्थापन</h1>
      </div>

      {/* Filters Section */}
      <div className="mb-6 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* District Dropdown */}
          <div className="space-y-2">
            <Label htmlFor="district">जिल्हा निवडा</Label>
            <RSelect
              id="district"
              options={districts}
              nameProperty="districtName"
              valueProperty="districtId"
              value={selectedDistrict}
              onChange={handleDistrictChange}
              placeholder="जिल्हा निवडा"
            />
          </div>

          {/* Search Box with Button */}
          <div className="space-y-2">
            <Label htmlFor="search">ब्लॉकचे नाव शोधा</Label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  id="search"
                  type="text"
                  placeholder="ब्लॉकचे नाव टाइप करा..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  onKeyPress={handleSearchKeyPress}
                  className="pl-10"
                  disabled={!selectedDistrict}
                />
              </div>
              <Button
                onClick={handleSearch}
                disabled={!selectedDistrict || isSearching}
                className="whitespace-nowrap"
              >
                {isSearching ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    शोधत आहे...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4 mr-2" />
                    शोधा
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>

        {/* Page Size Selector */}
        <div className="flex items-center gap-4">
          <Label htmlFor="pageSize">प्रति पृष्ठ रेकॉर्ड:</Label>
          <select
            id="pageSize"
            value={pageSize}
            onChange={(e) => handlePageSizeChange(parseInt(e.target.value))}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={10}>10</option>
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>

          {totalBlocks > 0 && (
            <span className="text-sm text-gray-600">
              एकूण {totalBlocks} ब्लॉक्स सापडले
            </span>
          )}
        </div>
      </div>

      {/* Table */}
      <div className="border rounded-lg shadow-lg border-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="p-2">ब्लॉकचे नाव</TableHead>
              <TableHead className="p-2">ब्लॉक प्रशासक</TableHead>
              <TableHead className="w-[150px] p-2">क्रिया</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {blocks?.length ? (
              blocks.map((block, index) => (
                <TableRow key={block?.blockId}>
                  <TableCell className="p-2">{block.blockName}</TableCell>
                  <TableCell className="p-2">
                    {block?.isEditMode ? (
                      <Combobox
                        options={admins}
                        labelProperty="userName"
                        valueProperty="userId"
                        value={block?.admin ?? null}
                        onChange={handleSetBlockAdmin(index)}
                      />
                    ) : (
                      <div>{block?.admin?.userName ?? "असाइन केलेले नाही"}</div>
                    )}
                  </TableCell>
                  <TableCell className="p-2">
                    <div className="flex">
                      <RButton
                        variant="ghost"
                        className="flex items-center gap-2"
                        onClick={handleEditBlockAdmin(index)}
                      >
                        <FilePenIcon className="h-4 w-4" />
                      </RButton>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} className="h-24 text-center">
                  {isSearching
                    ? "शोधत आहे..."
                    : searchTerm
                    ? "कोणतेही ब्लॉक सापडले नाहीत"
                    : "कोणतेही परिणाम नाहीत"}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination Controls */}
      {totalBlocks > 0 && (
        <div className="mt-4 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            पृष्ठ {currentPage} / {totalPages} ({totalBlocks} एकूण ब्लॉक्स)
          </div>

          <div className="flex items-center gap-2">
            <Button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1 || isSearching}
              variant="outline"
              size="sm"
            >
              <ChevronLeft className="h-4 w-4" />
              मागील
            </Button>

            <div className="flex gap-1">
              {/* Show first page */}
              {currentPage > 3 && (
                <>
                  <Button
                    onClick={() => handlePageChange(1)}
                    variant="outline"
                    size="sm"
                    className="w-10"
                  >
                    1
                  </Button>
                  {currentPage > 4 && <span className="px-2">...</span>}
                </>
              )}

              {/* Show pages around current page */}
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(
                  (page) =>
                    page === currentPage ||
                    page === currentPage - 1 ||
                    page === currentPage + 1 ||
                    (page === currentPage - 2 && currentPage <= 3) ||
                    (page === currentPage + 2 && currentPage >= totalPages - 2)
                )
                .map((page) => (
                  <Button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    variant={page === currentPage ? "default" : "outline"}
                    size="sm"
                    className="w-10"
                  >
                    {page}
                  </Button>
                ))}

              {/* Show last page */}
              {currentPage < totalPages - 2 && (
                <>
                  {currentPage < totalPages - 3 && (
                    <span className="px-2">...</span>
                  )}
                  <Button
                    onClick={() => handlePageChange(totalPages)}
                    variant="outline"
                    size="sm"
                    className="w-10"
                  >
                    {totalPages}
                  </Button>
                </>
              )}
            </div>

            <Button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages || isSearching}
              variant="outline"
              size="sm"
            >
              पुढील
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

const BlockAdminsPage = WithAuthentication(
  WithPermission("blockAdmins")(WithLayout(BlockAdmins))
);

export default BlockAdminsPage;
