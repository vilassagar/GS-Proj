import AuthLayout from "./AuthLayout";

function WithAuthLayout(WrappedComponent) {
  return function hoc(props) {
    return (
      <AuthLayout>
        <WrappedComponent {...props} />
      </AuthLayout>
    );
  };
}

export default WithAuthLayout;
