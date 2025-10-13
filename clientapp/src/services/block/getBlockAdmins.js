import { handleApiError, httpClient, Result } from "@/utils";

const getBlockAdmins = async (districtId, searchTerm = "", page = 1, pageSize = 50) => {
  try {
    // Build query parameters
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    // Add optional search term if provided
    if (searchTerm && searchTerm.trim() !== "") {
      params.append("searcTerm", searchTerm); // Note: API has typo "searcTerm"
    }

    const response = await httpClient.get(
      `/block/getBlockAdmins?${params.toString()}`
    );
    
    const { data } = response;
    
    // Return data with pagination info
    // Note: Adjust based on actual API response structure
    return Result.success({
      data: data,
      total: data.length, // If API returns total separately, use that instead
    });
  } catch (e) {
    return handleApiError(e);
  }
};

export default getBlockAdmins;