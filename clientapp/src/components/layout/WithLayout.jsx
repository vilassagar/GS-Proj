import AppLayout from "./AppLayout";

function WithLayout(WrappedComponent) {
  return function hoc(props) {
    return (
      <AppLayout>
        <WrappedComponent {...props} />
      </AppLayout>
    );
  };
}

export default WithLayout;
