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
import { usePermissionStore, usePolicyStore, userStore } from "@/lib/store";
import useLocationHistory from "@/lib/useLocationHistory";
import { CircleUser, LogOut } from "lucide-react";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function HeadLayout({ children }) {
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
  // Add this at the top level of your HeadLayout component
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
    localStorage.clear();
    removeUser();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Desktop Sidebar */}

        {/* Main Content */}
        <main className="flex-1 ">
          {/* Desktop Header */}
          <header className="hidden md:flex h-14 items-center justify-end border-b bg-slate-800 text-white px-4">
            <div className="flex items-center gap-4">
              {user?.firstName && (
                <span className="font-medium">Hello, {user.firstName}</span>
              )}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="rounded-full">
                    <CircleUser className="h-6 w-6 text-white hover:text-white" />
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

HeadLayout.propTypes = {
  children: PropTypes.element,
};

HeadLayout.defaultProps = {
  children: <></>,
};
