import { usePermissionStore, userStore } from "@/lib/store";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const WithPermission = (pageName) => (WrappedComponent) => {
  return function Hoc(props) {
    let permissions = usePermissionStore((state) => state.permissions);
    let user = userStore((state) => state.user);
    const role = user?.roleName;

    const navigate = useNavigate();

    useEffect(() => {
      if (user?.isApprovalPending && !user?.isDocumentUploadComplete) {
        navigate("/approval-pending");
      }

      if (!user?.isApprovalPending && !user?.isDocumentUploadComplete) {
        navigate("/uploaddocs");
      }

      if (permissions !== null && !permissions?.[role]?.includes(pageName)) {
        navigate("/unauthorized");
      }
    }, [navigate, permissions]);

    return <WrappedComponent {...props} />;
  };
};

export default WithPermission;
