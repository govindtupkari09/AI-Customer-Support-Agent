import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Bot, Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post(
        "/api/auth/login",
        formData
      );

      const token =
        response.data.access_token ||
        response.data.data?.access_token;

      if (!token) {
        throw new Error("Access token not found in response.");
      }

      localStorage.setItem("access_token", token);
      localStorage.setItem("user", JSON.stringify(response.data.user));
      

      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        "Login failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-10">

      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="text-center mb-8">

          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-600 mb-4">
            <Bot size={34} className="text-white" />
          </div>

          <h1 className="text-3xl font-bold text-white">
            Company AI Assistant
          </h1>

          <p className="text-slate-400 mt-2">
            Your intelligent company knowledge assistant
          </p>

        </div>

        {/* Login Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">

          <h2 className="text-2xl font-semibold text-white mb-2">
            Welcome Back
          </h2>

          <p className="text-slate-400 text-sm mb-7">
            Login to access your AI workspace.
          </p>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm mb-5">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">

            {/* Email */}
            <div>

              <label className="text-sm text-slate-300 block mb-2">
                Email Address
              </label>

              <div className="relative">

                <Mail
                  size={18}
                  className="absolute left-3 top-3.5 text-slate-500"
                />

                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter your email"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white outline-none focus:border-blue-500"
                />

              </div>

            </div>

            {/* Password */}
            <div>

              <label className="text-sm text-slate-300 block mb-2">
                Password
              </label>

              <div className="relative">

                <Lock
                  size={18}
                  className="absolute left-3 top-3.5 text-slate-500"
                />

                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg py-3 pl-11 pr-12 text-white outline-none focus:border-blue-500"
                />

                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3.5 text-slate-500"
                >
                  {showPassword ? (
                    <EyeOff size={18} />
                  ) : (
                    <Eye size={18} />
                  )}
                </button>

              </div>

            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              {loading ? "Signing In..." : "Sign In"}
              {!loading && <ArrowRight size={18} />}
            </button>

          </form>

          <div className="mt-7 text-center text-sm text-slate-400">

            Don't have an account?

            <Link
              to="/register"
              className="text-blue-400 hover:text-blue-300 font-semibold ml-1"
            >
              Create Account
            </Link>

          </div>

        </div>

        <p className="text-center text-slate-600 text-xs mt-6">
          © 2026 Company AI Assistant. All rights reserved.
        </p>

      </div>

    </div>
  );
}

export default Login;