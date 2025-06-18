/* eslint-disable react/prop-types */
import PropTypes from "prop-types";

export default function AuthLayout({ children }) {
  return (
    <div className=" bg-gray-50">
      {/* Mobile Header */}

      <div className="flex">
        {/* Main Content */}
        <main className="flex-1">
          {/* Desktop Header */}
          <header className="hidden md:flex h-14 items-center justify-end border-b bg-slate-800 text-white "></header>

          {/* Page Content */}
          <div>{children}</div>
        </main>
      </div>
    </div>
  );
}

AuthLayout.propTypes = {
  children: PropTypes.element,
};

AuthLayout.defaultProps = {
  children: <></>,
};
