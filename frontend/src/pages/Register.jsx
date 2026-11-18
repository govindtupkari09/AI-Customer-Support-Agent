import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Bot, User, Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";
import api from "../services/api";

function Register() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await api.post(
        "/api/auth/register",
        formData
      );

      setSuccess(
        response.data.message || "Registration successful!"
      );

      setTimeout(() => {
        navigate("/");
      }, 1500);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Registration failed. Please try again."
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
            Create your intelligent workspace
          </p>

        </div>

        {/* Register Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl">

          <h2 className="text-2xl font-semibold text-white mb-2">
            Create Account
          </h2>

          <p className="text-slate-400 text-sm mb-7">
            Register to access your company knowledge assistant.
          </p>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg text-sm mb-5">
              {error}
            </div>
          )}

          {success && (
            <div className="bg-green-500/10 border border-green-500/30 text-green-400 p-3 rounded-lg text-sm mb-5">
              {success}
            </div>
          )}

          <form onSubmit={handleRegister} className="space-y-5">

            {/* Full Name */}
            <div>

              <label className="text-sm text-slate-300 block mb-2">
                Full Name
              </label>

              <div className="relative">

                <User
                  size={18}
                  className="absolute left-3 top-3.5 text-slate-500"
                />

                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  required
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg py-3 pl-11 pr-4 text-white outline-none focus:border-blue-500"
                />

              </div>

            </div>

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
                  placeholder="Create a password"
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

            {/* Register Button */}
            <button
              type="submit"
              disabled={loading || !!success}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              {loading ? "Creating Account..." : "Create Account"}

              {!loading && <ArrowRight size={18} />}
            </button>

          </form>

          <div className="mt-7 text-center text-sm text-slate-400">

            Already have an account?

            <Link
              to="/"
              className="text-blue-400 hover:text-blue-300 font-semibold ml-1"
            >
              Sign In
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

export default Register;