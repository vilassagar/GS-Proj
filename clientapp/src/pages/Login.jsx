import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import WithAuthLayout from "@/components/layout/WithAuthLayout";
import { useNavigate } from "react-router-dom";
import { produce } from "immer";
import { login, sendOtp } from "@/services/auth";
import toast from "react-hot-toast";
import { userStore } from "@/lib/store";

function Login() {
  const navigate = useNavigate();
  const [otpSent, setOtpSent] = useState(false);
  const [loginDetails, setLoginDetails] = useState({
    mobileNumber: "",
    otp: "",
  });

  const [timer, setTimer] = useState(0); // Timer state
  const updateUser = userStore((state) => state.updateUser);

  // Timer countdown effect
  useEffect(() => {
    let countdown;
    if (timer > 0) {
      countdown = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    }
    return () => clearInterval(countdown);
  }, [timer]);

  const handleChange = (name) => (e) => {
    const nextState = produce(loginDetails, (draft) => {
      draft[name] = e.target.value;
    });
    setLoginDetails(nextState);
  };

  const handleSendOtp = async () => {
    const { mobileNumber } = loginDetails;

    if (!mobileNumber || mobileNumber.trim().length !== 10) {
      toast.error("कृपया वैध 10-अंकी मोबाइल क्रमांक प्रविष्ट करा");
      return;
    }

    const fullMobileNumber = `+91${mobileNumber}`;

    try {
      let response = await sendOtp(fullMobileNumber);

      if (response?.status === "success") {
        setOtpSent(true);
        setTimer(30); // Start 30-second timer
        toast.success("OTP यशस्वीरित्या पाठवला गेला!");
      } else {
        toast.error("OTP पाठवता आला नाही, कृपया पुन्हा प्रयत्न करा.");
      }
    } catch (error) {
      toast.error("सेवा अनुपलब्ध आहे. कृपया नंतर पुन्हा प्रयत्न करा.");
    }
  };

  const handleLogin = async () => {
    if (!loginDetails.otp) {
      toast.error("कृपया OTP प्रविष्ट करा");
      return;
    }
    let details = {
      mobileNumber: `+91${loginDetails?.mobileNumber}`,
      otp: loginDetails?.otp,
    };

    let response = await login(details);
    if (response?.status === "success") {
      updateUser(response?.data);
      navigate("/");
    } else {
      toast.error("लॉगिन अयशस्वी, कृपया तपासा");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>लॉगिन</CardTitle>
          <CardDescription>
            लॉगिन करण्यासाठी आपला मोबाइल क्रमांक आणि OTP प्रविष्ट करा.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="mobile">मोबाइल क्रमांक</Label>
                <div
                  style={{
                    position: "relative",
                    width: "100%",
                    maxWidth: "300px",
                  }}
                >
                  <span
                    style={{
                      position: "absolute",
                      left: "12px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      color: "#555",
                      fontSize: "16px",
                      pointerEvents: "none",
                    }}
                  >
                    +91
                  </span>
                  <input
                    id="mobile"
                    name="mobile"
                    type="tel"
                    placeholder="आपला मोबाइल क्रमांक प्रविष्ट करा"
                    value={loginDetails?.mobileNumber}
                    onChange={handleChange("mobileNumber")}
                    style={{
                      width: "100%",
                      padding: "10px 10px 10px 45px",
                      fontSize: "16px",
                      border: "1px solid #ccc",
                      borderRadius: "4px",
                    }}
                  />
                </div>
              </div>
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="otp">वन-टाइम पासवर्ड</Label>
                <Input
                  id="otp"
                  name="otp"
                  placeholder="OTP प्रविष्ट करा"
                  disabled={!otpSent}
                  value={loginDetails?.otp}
                  onChange={handleChange("otp")}
                />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex flex-col space-y-2">
          <Button
            className="w-full"
            onClick={handleSendOtp}
            disabled={timer > 0}
          >
            {timer > 0 ? `OTP पुन्हा पाठवा (${timer} सेकंद)` : "OTP पाठवा"}
          </Button>
          <Button className="w-full" type="button" onClick={handleLogin}>
            लॉगिन
          </Button>
          <div className="pt-4 text-center w-full">
            <p className="text-sm text-gray-600 mb-2">खाते नाही?</p>
            <button
              onClick={() => {
                navigate("/register");
              }}
              className="w-full bg-emerald-600 text-white py-3 rounded-md hover:bg-emerald-700 transition-all duration-200 font-medium flex items-center justify-center gap-2 shadow-md"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="lucide lucide-user-plus"
              >
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <line x1="19" x2="19" y1="8" y2="14" />
                <line x1="16" x2="22" y1="11" y2="11" />
              </svg>
              नोंदणी करा
            </button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}

export default WithAuthLayout(Login);
