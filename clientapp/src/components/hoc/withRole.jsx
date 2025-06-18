import { userStore } from "@/lib/store";
import { useEffect } from "react";

const WithRole = (WrappedComponent) => {
  return function Hoc(props) {
    let user = userStore((state) => state.user);

    useEffect(() => {
      if (
        user !== null &&
        user?.userType?.name?.toLowerCase().trim() !== "pensioner"
      ) {
        window.location.href = "/dashboard";
        return null;
      }
    }, [user]);

    return <WrappedComponent {...props} />;
  };
};

export default WithRole;
