import { useState } from "react";
import {
  Bot,
  MessageSquare,
  FileText,
  Upload,
  Search,
  Settings,
  LogOut,
  Menu,
  X,
  Send,
  User,
  ShieldCheck,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import api from "../services/api";
import DocumentManager from "../components/DocumentManager";

function Dashboard() {
  const [activeTab, setActiveTab] = useState("chat");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    window.location.href = "/";
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!query.trim() || loading) return;

    const currentQuery = query;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: currentQuery },
    ]);

    setQuery("");
    setLoading(true);

    try {
      const response = await api.post("/api/chat/ask", {
        query: currentQuery,
        top_k: 3,
    });

      const data = response.data.data || response.data;

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer || "No answer received.",
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error.response?.data?.detail ||
            "Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex">

      {/* Mobile Sidebar Button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 bg-slate-800 p-2 rounded-lg"
      >
        {sidebarOpen ? <X /> : <Menu />}
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-72 bg-slate-900 border-r border-slate-800 flex flex-col transform transition-transform duration-300 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-xl">
            <Bot size={25} />
          </div>

          <div>
            <h1 className="font-bold text-lg">Company AI</h1>
            <p className="text-xs text-slate-400">Knowledge Assistant</p>
          </div>
        </div>

        <div className="p-4">
          <button
            onClick={() => setMessages([])}
            className="w-full bg-blue-600 hover:bg-blue-700 rounded-xl p-3 flex items-center justify-center gap-2 font-medium"
          >
            <MessageSquare size={18} />
            New Chat
          </button>
        </div>

        <nav className="px-4 space-y-2">
          <button className="w-full flex items-center gap-3 p-3 rounded-lg bg-slate-800 text-blue-400">
            <MessageSquare size={19} />
            AI Assistant
          </button>

          <button
            onClick={() => setActiveTab("documents")}
             className={`w-full flex items-center gap-3 p-3 rounded-lg ${
             activeTab === "documents"
              ? "bg-slate-800 text-blue-400"
              : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
>
           <FileText size={19} />
            Documents
          </button>

          <button className="w-full flex items-center gap-3 p-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white">
            <Upload size={19} />
            Upload Documents
          </button>

          <button className="w-full flex items-center gap-3 p-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white">
            <Settings size={19} />
            Settings
          </button>
        </nav>

        <div className="mt-auto p-4 border-t border-slate-800">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-slate-700 rounded-full p-2">
              <User size={20} />
            </div>

            <div className="overflow-hidden">
              <p className="text-sm font-medium truncate">
                {user.full_name || "User"}
              </p>
              <p className="text-xs text-slate-400 truncate">
                {user.email || "Company Account"}
              </p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 p-3 text-red-400 hover:bg-red-500/10 rounded-lg"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 min-w-0 flex flex-col min-h-screen">

        {/* Header */}
        <header className="h-20 border-b border-slate-800 flex items-center justify-between px-6 lg:px-10 pl-16 lg:pl-10">
          <div>
            <h2 className="text-lg font-semibold">AI Workspace</h2>
            <p className="text-xs text-slate-400">
              Ask questions about your company documents
            </p>
          </div>

          <div className="flex items-center gap-2 text-green-400 text-sm">
            <ShieldCheck size={18} />
            <span>Secure Workspace</span>
          </div>
        </header>

        {/* Chat Area */}
       {activeTab === "chat" ? (
  <section className="flex-1 overflow-y-auto p-6 lg:p-10">

    {/* येथे तुझा आधीचा पूर्ण Chat Area code ठेव */}

  </section>
) : (
  <section className="flex-1 overflow-y-auto p-6 lg:p-10">
    <DocumentManager />
  </section>
)}

        {/* Chat Input */}
        <div className="p-6 lg:px-10 border-t border-slate-800">
          <form
            onSubmit={handleSendMessage}
            className="max-w-4xl mx-auto flex items-center gap-3 bg-slate-900 border border-slate-700 rounded-2xl p-2"
          >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything about your company documents..."
              className="flex-1 bg-transparent px-4 py-3 outline-none text-white placeholder:text-slate-500"
            />

            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-40 p-3 rounded-xl transition"
            >
              <Send size={20} />
            </button>
          </form>

          <p className="text-center text-xs text-slate-600 mt-3">
            AI responses are generated using your uploaded documents.
          </p>
        </div>

      </main>
    </div>
  );
}

export default Dashboard;