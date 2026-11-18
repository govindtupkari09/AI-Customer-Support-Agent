import { useEffect, useState } from "react";
import {
  Upload,
  FileText,
  File,
  Trash2,
  Search,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Loader2,
  X,
} from "lucide-react";

import api from "../services/api";

function DocumentManager() {
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Fetch documents
  const fetchDocuments = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await api.get(
        "/api/documents/list-documents"
      );

      const data = response.data.data;

      setDocuments(
        Array.isArray(data)
          ? data
          : data?.documents || []
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load documents."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Select file
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];

    if (!file) return;

    const extension = file.name.split(".").pop().toLowerCase();

    if (!["pdf", "docx"].includes(extension)) {
      setError("Only PDF and DOCX files are supported.");
      return;
    }

    setError("");
    setMessage("");
    setSelectedFile(file);
  };

  // Upload and process document
  const handleUpload = async () => {
  if (!selectedFile) return;

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await api.post(
      "/api/documents/process-document",
      formData
    );

    alert(response.data.message);
    setSelectedFile(null);
    fetchDocuments();

  } catch (error) {
    console.error("Upload Error:", error.response?.data || error);

    const detail = error.response?.data?.detail;

    setError(
      typeof detail === "string"
        ? detail
        : JSON.stringify(detail || error.message)
    );
  }
};

  // Delete document
  const handleDelete = async (documentId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmed) return;

    setDeletingId(documentId);
    setError("");
    setMessage("");

    try {
      const response = await api.delete(
        "/api/documents/delete-document",
        {
          params: {
            document_id: documentId,
          },
        }
      );

      setMessage(
        response.data.message ||
        "Document deleted successfully."
      );

      await fetchDocuments();

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to delete document."
      );
    } finally {
      setDeletingId(null);
    }
  };

  // Search documents locally
  const filteredDocuments = documents.filter((doc) =>
    (doc.filename || doc.source || "")
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">

        <div>
          <h1 className="text-2xl font-bold text-white">
            Document Management
          </h1>

          <p className="text-slate-400 text-sm mt-1">
            Upload, search and manage your knowledge base.
          </p>
        </div>

        <button
          onClick={fetchDocuments}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm"
        >
          <RefreshCw size={16} />
          Refresh
        </button>

      </div>

      {/* Notifications */}
      {message && (
        <div className="flex items-center gap-2 bg-green-500/10 border border-green-500/30 text-green-400 p-4 rounded-xl">
          <CheckCircle size={19} />
          {message}
        </div>
      )}

      {error && (
        <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl">
          <AlertCircle size={19} />
          {error}
        </div>
      )}

      {/* Upload Section */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

        <h2 className="text-lg font-semibold text-white mb-5">
          Upload Documents
        </h2>

        <label className="block border-2 border-dashed border-slate-700 hover:border-blue-500 rounded-2xl p-10 text-center cursor-pointer transition">

          <input
            type="file"
            accept=".pdf,.docx"
            onChange={handleFileChange}
            className="hidden"
          />

          <div className="inline-flex bg-blue-600/10 p-4 rounded-xl mb-4">
            <Upload size={30} className="text-blue-400" />
          </div>

          <p className="text-white font-medium">
            Click to select a document
          </p>

          <p className="text-slate-500 text-sm mt-2">
            Supported formats: PDF and DOCX
          </p>

        </label>

        {selectedFile && (
          <div className="mt-5 flex flex-col sm:flex-row items-center justify-between gap-4 bg-slate-800 p-4 rounded-xl">

            <div className="flex items-center gap-3 min-w-0">
              <FileText className="text-blue-400 shrink-0" />

              <div className="min-w-0">
                <p className="text-white text-sm truncate">
                  {selectedFile.name}
                </p>

                <p className="text-slate-400 text-xs">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">

              <button
                onClick={() => setSelectedFile(null)}
                className="p-2 text-slate-400 hover:text-white"
                title="Remove selected file"
              >
                <X size={18} />
              </button>

              <button
                onClick={handleUpload}
                disabled={uploading}
                className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 px-5 py-2 rounded-lg text-white text-sm flex items-center gap-2"
              >
                {uploading ? (
                  <>
                    <Loader2 size={17} className="animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload size={17} />
                    Upload
                  </>
                )}
              </button>

            </div>
          </div>
        )}

      </div>

      {/* Documents List */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

        <div className="flex flex-col sm:flex-row justify-between gap-4 mb-6">

          <div>
            <h2 className="text-lg font-semibold text-white">
              Uploaded Documents
            </h2>

            <p className="text-slate-400 text-sm mt-1">
              {documents.length} documents available
            </p>
          </div>

          <div className="relative">
            <Search
              size={18}
              className="absolute left-3 top-3 text-slate-500"
            />

            <input
              type="text"
              placeholder="Search documents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg py-2 pl-10 pr-4 text-white outline-none focus:border-blue-500 w-full sm:w-64"
            />
          </div>

        </div>

        {loading ? (
          <div className="text-center py-12 text-blue-400">
            <Loader2 className="animate-spin mx-auto mb-3" />
            Loading documents...
          </div>
        ) : filteredDocuments.length === 0 ? (
          <div className="text-center py-12">

            <File size={38} className="text-slate-600 mx-auto mb-3" />

            <p className="text-slate-300">
              No documents found.
            </p>

            <p className="text-slate-500 text-sm mt-1">
              Upload your first PDF or DOCX document.
            </p>

          </div>
        ) : (
          <div className="overflow-x-auto">

            <table className="w-full text-left">

              <thead>
                <tr className="text-slate-500 text-xs border-b border-slate-800">
                  <th className="pb-4 font-medium">DOCUMENT</th>
                  <th className="pb-4 font-medium">TYPE</th>
                  <th className="pb-4 font-medium">CHUNKS</th>
                  <th className="pb-4 font-medium">ACTION</th>
                </tr>
              </thead>

              <tbody>

                {filteredDocuments.map((doc, index) => {

                  const documentId =
                    doc.document_id || doc.id;

                  return (
                    <tr
                      key={documentId || index}
                      className="border-b border-slate-800 last:border-0"
                    >

                      <td className="py-4">
                        <div className="flex items-center gap-3">

                          <div className="bg-blue-600/10 p-2 rounded-lg">
                            <FileText className="text-blue-400" size={20} />
                          </div>

                          <span className="text-sm text-white">
                            {doc.filename || doc.source || "Document"}
                          </span>

                        </div>
                      </td>

                      <td className="py-4 text-sm text-slate-400">
                        {doc.file_type || "Document"}
                      </td>

                      <td className="py-4 text-sm text-slate-400">
                        {doc.total_chunks ?? "-"}
                      </td>

                      <td className="py-4">

                        <button
                          onClick={() => handleDelete(documentId)}
                          disabled={!documentId || deletingId === documentId}
                          className="text-red-400 hover:bg-red-500/10 p-2 rounded-lg disabled:opacity-50"
                          title="Delete document"
                        >
                          {deletingId === documentId ? (
                            <Loader2 size={18} className="animate-spin" />
                          ) : (
                            <Trash2 size={18} />
                          )}
                        </button>

                      </td>

                    </tr>
                  );
                })}

              </tbody>

            </table>

          </div>
        )}

      </div>

    </div>
  );
}

export default DocumentManager;