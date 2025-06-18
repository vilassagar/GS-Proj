import { userStore } from "@/lib/store";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const WithAuthentication = (WrappedComponent) => {
  return function Hoc(props) {
    const navigate = useNavigate();
    const user = userStore((state) => state.user);

    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isCheckingAuth, setIsCheckingAuth] = useState(true);

    useEffect(() => {
      (() => {
        if (user) {
          setIsAuthenticated(true);
        } else {
          window.location.href = "/login";
        }

        setIsCheckingAuth(false);
      })();
    }, []);

    if (isCheckingAuth) {
      return null;
    }

    if (!isAuthenticated) {
      return null;
    }

    if (isAuthenticated) {
      return <WrappedComponent {...props} />;
    }
  };
};

export default WithAuthentication;
