import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import WithHeadLayout from "@/components/layout/WithHeadLayout";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import RButton from "@/components/ui/rButton";
import { userStore } from "@/lib/store";
import { docUpload } from "@/services/gramsevak";
import { getDocuments } from "@/services/upload";
import { produce } from "immer";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

function DocumentUpload() {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState([]);
  let user = userStore((state) => state.user);
  let markDocumentUploadComplete = userStore(
    (state) => state.markDocumentUploadComplete
  );

  const [isDocumentUplaodInprogress, setIsDocumentUplaodInprogress] =
    useState(false);

  useEffect(() => {
    (async () => {
      let response = await getDocuments();
      if (response.status === "success") {
        setDocuments(response.data);
      } else {
        toast.error("कागदपत्रे मिळवू शकत नाही");
      }
    })();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setIsDocumentUplaodInprogress(true);

    let formData = new FormData();

    documents.forEach((document) => {
      if (document?.documents) {
        formData.append(document?.documentTypeId, document?.documents);
      }
    });

    let response = await docUpload(formData);

    if (response.status === "success") {
      toast.success("यशस्वीरित्या जतन केले");
      markDocumentUploadComplete();
      navigate("/");
    } else {
      toast.error("कागदपत्रे जतन करता आली नाहीत, कृपया पुन्हा प्रयत्न करा");
    }

    setIsDocumentUplaodInprogress(false);
  };

  const handleChange = (index) => (e) => {
    let nextState = produce(documents, (draft) => {
      draft[index]["documents"] = e.target.files[0];
    });

    setDocuments(nextState);
  };

  return (
    <div className="w-full flex justify-center ">
      <div className="min-h-screen flex items-center justify-start to-purple-100  ">
        <div className="w-full max-w-4xl p-8 space-y-6 ">
          <div>
            <h1 className="text-2xl font-bold ">कागदपत्रे अपलोड करा</h1>
            <p className="text-gray-600 mt-2">
              कृपया खालील कागदपत्रे अपलोड करा. तारांकन (*) असलेली क्षेत्रे
              अनिवार्य आहेत.
            </p>
          </div>
          <form className="space-y-6" onSubmit={handleSubmit}>
            {documents?.map((doc, index) => (
              <div key={doc.documentTypeName} className="space-y-2">
                <Label
                  htmlFor={doc.documentTypeName}
                  className="flex items-center"
                >
                  {doc.documentTypeName}
                  {doc.mendatory && (
                    <span className="text-red-500 ml-1">*</span>
                  )}
                </Label>
                <Input
                  onChange={handleChange(index)}
                  id={doc.documentTypeName}
                  type="file"
                  required={doc.mendatory}
                  className="file:mr-4 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
                />
              </div>
            ))}
            <RButton
              type="submit"
              className="w-full"
              isLoading={isDocumentUplaodInprogress}
            >
              कागदपत्रे अपलोड करा
            </RButton>
          </form>
        </div>
      </div>
    </div>
  );
}

export default WithAuthentication(
  WithPermission("uploaddocs")(WithHeadLayout(DocumentUpload))
);
