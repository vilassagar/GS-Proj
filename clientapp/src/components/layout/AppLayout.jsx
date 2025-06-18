/* eslint-disable react/prop-types */
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { usePermissionStore, usePolicyStore, userStore } from "@/lib/store";
import useLocationHistory from "@/lib/useLocationHistory";
import { cn } from "@/lib/utils";
import {
  CircleUser,
  FileCheck,
  LayoutDashboard,
  LogOut,
  Menu,
  Upload,
  Users,
} from "lucide-react";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import RButton from "../ui/rButton";

export default function AppLayout({ children }) {
  const navigate = useNavigate();
  const user = userStore((state) => state.user);
  const removeUser = userStore((state) => state.removeUser);
  const permissions = usePermissionStore((state) => state.permissions);
  const setMode = usePolicyStore((state) => state.setMode);
  const updatePolicyId = usePolicyStore((state) => state.updatePolicyId);
  const [showPensionerMenu, setShowPensionerMenu] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const isPensioner =
    user?.userType?.name?.toLowerCase().trim() === "pensioner";
  // Add this at the top level of your AppLayout component
  const location = useLocation();
  useLocationHistory();

  const role = user?.roleName;

  useEffect(() => {
    const lastVisitedPensioner = JSON.parse(
      sessionStorage.getItem("lastVisitedpensioner")
    );
    setShowPensionerMenu(!isPensioner && !!lastVisitedPensioner?.userId);
  }, [isPensioner]);

  const handleLogout = () => {
    sessionStorage.clear();
    removeUser();
    navigate("/land");
  };

  const MenuItem = ({ icon: Icon, text, onClick, permission, path }) => {
    const isActive = location.pathname === path;
    if (permission) {
      return (
        <div
          className={cn(
            "flex items-center gap-3 rounded-lg px-3 py-2 transition-all cursor-pointer",
            isActive
              ? "bg-black text-white"
              : " hover:bg-black hover:text-white"
          )}
          onClick={() => {
            onClick();
            setIsMobileMenuOpen(false);
          }}
        >
          <Icon className="h-4 w-4" />
          <span className="text-sm">{text}</span>
        </div>
      );
    }
  };

  const AdminMenuItems = () => (
    <div className="space-y-3">
      <div className="space-y-1">
        <MenuItem
          icon={LayoutDashboard}
          text="मुख्यपृष्ठ"
          onClick={() => navigate("/")}
          path="/"
          permission={permissions[role]?.includes("home")}
        />
        <MenuItem
          icon={Users}
          text="प्रोफाईल"
          onClick={() => navigate("/profile")}
          path="/profile"
          permission={permissions[role]?.includes("profile")}
        />
        <MenuItem
          icon={FileCheck}
          text="पुस्तके"
          onClick={() => navigate("/books")}
          path="/books"
          permission={permissions[role]?.includes("books")}
        />
        <MenuItem
          icon={Users}
          text="ब्लॉक प्रशासक"
          onClick={() => navigate("/block-admins")}
          path="/blockadmins"
          permission={permissions[role]?.includes("blockAdmins")}
        />
        <MenuItem
          icon={Users}
          text="जिल्हा प्रशासक"
          onClick={() => navigate("/district-admins")}
          path="/districtadmins"
          permission={permissions[role]?.includes("districtAdmins")}
        />
        <MenuItem
          icon={Users}
          text="ग्राम सेवक"
          onClick={() => navigate("/gram-sevaks")}
          path="/gramsevaks"
          permission={permissions[role]?.includes("gramSevaks")}
        />
        <MenuItem
          icon={Upload}
          text="अपलोड करा"
          onClick={() => navigate("/upload-books")}
          path="/uploadbooks"
          permission={permissions[role]?.includes("upload")}
        />
      </div>
    </div>
  );

  console.log("user : ", user);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Desktop Sidebar */}
        <aside className="hidden md:flex md:w-64 lg:w-72 flex-col fixed h-screen border-r bg-slate-800 text-white">
          <div className="flex h-14 items-center px-4">
            <Button
              variant="ghost"
              className="p-0"
              onClick={() => navigate("/")}
            >
              <div className="container py-3">
                <div className="flex items-center justify-start">
                  <div className="flex items-center space-x-2">
                    <div className="hidden md:block">
                      <h1 className="text-xl font-bold text-white-800">
                        शासकीय ठराव
                      </h1>
                      <p className="text-sm text-white-600">
                        अधिकृत दस्तऐवज संग्रह
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </Button>
          </div>
          <nav className="flex-1 overflow-y-auto p-4 text-white">
            <AdminMenuItems />
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 md:ml-64 lg:ml-72">
          {/* Desktop Header */}
          <header className="hidden md:flex h-14 items-center justify-end border-b bg-slate-800 text-white px-4">
            <div className="flex items-center gap-4">
              {user?.firstName && (
                <span className="font-medium">Hello, {user.firstName}</span>
              )}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="rounded-full">
                    <CircleUser className="h-6 w-6 text-white" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-48">
                  <DropdownMenuLabel>My Account</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onClick={() => navigate(isPensioner ? "/" : "/profile")}
                  >
                    Profile
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={handleLogout}>
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </header>

          {/* Page Content */}
          <div className="p-4 md:p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}

AppLayout.propTypes = {
  children: PropTypes.element,
};

AppLayout.defaultProps = {
  children: <></>,
};
