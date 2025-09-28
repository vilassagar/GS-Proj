import ApprovalPending from "@/pages/ApprovalPending";
import BlockAdmins from "@/pages/BlockAdmins";
import Books from "@/pages/Books";
import Dashboard from "@/pages/Dashboard";
import MyDashboard from "@/pages/MyDashboard";

import DistrictAdmins from "@/pages/DistrictAdmins";
import DocumentUpload from "@/pages/DocumentUpload_";
import GramSevaks from "@/pages/GramSevaks";
import LandingPage from "@/pages/LandingPage";
import Login from "@/pages/Login";
import Profile from "@/pages/Profile";
import Register from "@/pages/Register";
import UnauthorisedAccess from "@/pages/UnauthorisedAccess";
import UploadBooks from "@/pages/UploadBooks";

const routes = [
  {
    exact: true,
    path: "/login",
    component: <Login />,
  },
  {
    exact: true,
    path: "/register",
    component: <Register />,
  },
  {
    exact: true,
    path: "/",
    component: <Dashboard />,
  },
  {
    exact: true,
    path: "/mydashboard",
    component: <MyDashboard />,
  },

  {
    exact: true,
    path: "/books",
    component: <Books />,
  },

  {
    exact: true,
    path: "/profile",
    component: <Profile />,
  },
  {
    exact: true,
    path: "/uploaddocs",
    component: <DocumentUpload />,
  },
  {
    exact: true,
    path: "/block-admins",
    component: <BlockAdmins />,
  },
  {
    exact: true,
    path: "/district-admins",
    component: <DistrictAdmins />,
  },
  {
    exact: true,
    path: "/gram-sevaks",
    component: <GramSevaks />,
  },
  {
    exact: true,
    path: "/upload-books",
    component: <UploadBooks />,
  },
  {
    exact: true,
    path: "/approval-pending",
    component: <ApprovalPending />,
  },
  {
    exact: true,
    path: "/unauthorized",
    component: <UnauthorisedAccess />,
  },
  {
    exact: true,
    path: "/land",
    component: <LandingPage />,
  },
];

export default routes;
