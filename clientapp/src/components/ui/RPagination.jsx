import {
  ChevronFirst,
  ChevronLast,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "lucide-react";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import RButton from "./rButton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./select";

export function RPagination({ paginationModel, onPageChange }) {
  const [paging, setPaging] = useState({
    numberOfPages: 0,
    pageNumber: 0,
    recordsPerPage: 0,
    nextPageNumber: 0,
    previousPageNumber: 0,
  });

  useEffect(() => {
    if (paginationModel !== null) {
      setPaging(paginationModel);
    }
  }, [paginationModel]);

  const handleNextClick = () => {
    let nextState = { ...paging };
    nextState["pageNumber"] = nextState["pageNumber"] + 1;
    setPaging(nextState);
    onPageChange(nextState);
  };

  const handlePreviousClick = () => {
    let nextState = { ...paging };
    nextState["pageNumber"] = nextState["pageNumber"] - 1;
    setPaging(nextState);
    onPageChange(nextState);
  };

  const handleFirstClick = () => {
    let nextState = { ...paging };
    nextState["pageNumber"] = 1;
    setPaging(nextState);
    onPageChange(nextState);
  };

  const handleLastClick = () => {
    let nextState = { ...paging };
    nextState["pageNumber"] = nextState["numberOfPages"];
    setPaging(nextState);
    onPageChange(nextState);
  };

  const handlePageSizeChange = (event) => {
    let nextState = { ...paging };
    nextState["recordsPerPage"] = Number(event);
    setPaging(nextState);
    onPageChange(nextState);
  };

  if (paging.pageNumber !== undefined && paging.numberOfPages !== undefined) {
    return (
      <div className="flex items-center">
        <div>
          <Select
            value={`${paging.recordsPerPage}`}
            onValueChange={handlePageSizeChange}
          >
            <SelectTrigger className="h-8 w-[70px]">
              <SelectValue value={paging.recordsPerPage} />
            </SelectTrigger>
            <SelectContent side="top">
              {[10, 20, 30, 40, 50, 100].map((pageSize) => (
                <SelectItem key={pageSize} value={`${pageSize}`}>
                  {pageSize}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex w-[100px] items-center justify-center text-sm font-medium ml-5">
          {`Page ${paging.pageNumber} of ${paging.numberOfPages}`}
        </div>
        <div className="flex items-center space-x-2 my-5">
          <RButton
            variant="outline"
            className="hidden h-8 w-8 p-0 lg:flex"
            onClick={handleFirstClick}
            isDisabled={paging.pageNumber == 1}
          >
            <span className="sr-only">Go to first page</span>
            <ChevronFirst className="h-4 w-4" />
          </RButton>
          <RButton
            variant="outline"
            className="h-8 w-8 p-0"
            onClick={handlePreviousClick}
            isDisabled={paging.pageNumber == 1}
          >
            <span className="sr-only">Go to previous page</span>
            <ChevronLeftIcon className="h-4 w-4" />
          </RButton>
          <RButton
            variant="outline"
            className="h-8 w-8 p-0"
            onClick={handleNextClick}
            isDisabled={paging.pageNumber == paging.numberOfPages}
          >
            <span className="sr-only">Go to next page</span>
            <ChevronRightIcon className="h-4 w-4" />
          </RButton>
          <RButton
            variant="outline"
            className="hidden h-8 w-8 p-0 lg:flex"
            onClick={handleLastClick}
            isDisabled={paging.pageNumber == paging.numberOfPages}
          >
            <span className="sr-only">Go to last page</span>
            <ChevronLast className="h-4 w-4" />
          </RButton>
        </div>
      </div>
    );
  }
}

RPagination.defaultProps = {
  paginationModel: {},
  onPageChange: () => {},
};

RPagination.propTypes = {
  paginationModel: PropTypes.object,
  onPageChange: PropTypes.func,
};
