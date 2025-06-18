/* eslint-disable react/prop-types */
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import routes from "./routes";
import { useEffect, useState } from "react";
import { useDateStore, usePermissionStore, userStore } from "./lib/store";
import { getYears, months } from "./lib/data";
import { formatMonths, formatYears } from "./lib/helperFunctions";
import { Toaster } from "react-hot-toast";
import { useTranslation } from "react-i18next";

// const resources = {
//   mr: { translation: { greeting: "नमस्कार! तुमचं स्वागत आहे" } },
// };

// function App() {
//   const { t, i18n } = useTranslation();

//   return (
//     <div>
//       <button onClick={() => i18n.changeLanguage("mr")}>मराठी</button>
//       <p>{t("greeting")}</p>
//     </div>
//   );
// }

function App() {
  const setPermissions = usePermissionStore((state) => state.setPermissions);
  const user = userStore((state) => state.user);
  const setMonths = useDateStore((state) => state.setMonths);
  const setYears = useDateStore((state) => state.setYears);

  useEffect(() => {
    (async () => {
      const fMonths = formatMonths(months);
      const fYears = formatYears(getYears());
      setMonths(fMonths);
      setYears(fYears);
    })();
  }, [user, setPermissions, setMonths, setYears]);
  return (
    <div>
      <Toaster />
      <Router>
        <Routes>
          {routes.map((route, index) => (
            <Route
              key={index + route.path}
              path={route.path}
              element={route.component}
            />
          ))}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
