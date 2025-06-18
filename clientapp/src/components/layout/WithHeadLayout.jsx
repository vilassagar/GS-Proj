import HeadLayout from "./HeadLayout";

function WithHeadLayout(WrappedComponent) {
  return function hoc(props) {
    return (
      <HeadLayout>
        <WrappedComponent {...props} />
      </HeadLayout>
    );
  };
}

export default WithHeadLayout;
