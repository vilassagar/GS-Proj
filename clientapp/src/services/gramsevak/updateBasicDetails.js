// For the BasicDetails form submission
import { handleApiError, httpClient, Result } from "@/utils";
const updateBasicDetails = async (formData) => {
  const response = await httpClient.put('/v1/profile/basic-details', {
 
    
    body: JSON.stringify({
      firstName: formData.firstName,
      lastName: formData.lastName,
      designation: formData.designation,
      districtId: formData.district,
      blockId: formData.block,
      gramPanchayatId: formData.gramPanchayat,
      mobileNumber: formData.mobileNumber,
      whatsappNumber: formData.whatsappNumber,
      email: formData.email
    })
  });
  return response.json();
};

export default updateBasicDetails;