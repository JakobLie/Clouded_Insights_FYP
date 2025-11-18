"use client";

import { useState } from "react";

export default function FileUploadModal({ isOpen, onClose, onSubmit }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMonth, setUploadMonth] = useState(""); // Add month state
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    validateAndSetFile(file);
  };

  const validateAndSetFile = (file) => {
    setError(null);
    
    if (!file) return;

    // Validate file type - update to match your backend
    const validTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
      'application/vnd.ms-excel', // .xls
      'text/csv' // .csv
    ];
    
    const validExtensions = ['.xlsx', '.xls', '.csv'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      setError('Please upload an Excel (.xlsx, .xls) or CSV (.csv) file');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    validateAndSetFile(file);
  };

  const validateMonth = (month) => {
    // Validate MM-YYYY format
    const monthRegex = /^(0[1-9]|1[0-2])-\d{4}$/;
    return monthRegex.test(month);
  };

  const handleSubmit = async () => {
    if (!selectedFile || !uploadMonth) {
      setError('Please select a file and enter a month');
      return;
    }

    if (!validateMonth(uploadMonth)) {
      setError('Please enter month in MM-YYYY format (e.g., 11-2025)');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      await onSubmit(selectedFile, uploadMonth);
      // Reset on success
      setSelectedFile(null);
      setUploadMonth("");
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleClose = () => {
    setSelectedFile(null);
    setUploadMonth("");
    setError(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full mx-4 p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Upload P&L Report</h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
            disabled={uploading}
          >
            ×
          </button>
        </div>

        {/* Month Input */}
        <div className="mb-4">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Report Month <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            placeholder="MM-YYYY (e.g., 11-2025)"
            className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
            value={uploadMonth}
            onChange={(e) => setUploadMonth(e.target.value)}
            disabled={uploading}
          />
          <p className="text-xs text-gray-500 mt-1">
            Enter the month for this P&L report in MM-YYYY format
          </p>
        </div>

        {/* File Drop Zone */}
        <div
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragActive
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 bg-gray-50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {selectedFile ? (
            <div className="space-y-3">
              <div className="text-5xl">📄</div>
              <div className="font-semibold text-gray-700">{selectedFile.name}</div>
              <div className="text-sm text-gray-500">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </div>
              <button
                onClick={() => setSelectedFile(null)}
                className="text-sm text-red-600 hover:text-red-700 font-medium"
                disabled={uploading}
              >
                Remove file
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="text-5xl">📁</div>
              <div className="text-gray-600">
                <span className="font-semibold">Drag and drop</span> your file here
              </div>
              <div className="text-sm text-gray-500">or</div>
              <label className="inline-block">
                <span className="px-4 py-2 bg-indigo-600 text-white rounded-lg cursor-pointer hover:bg-indigo-700 transition">
                  Browse files
                </span>
                <input
                  type="file"
                  className="hidden"
                  accept=".xlsx,.xls,.csv"
                  onChange={handleFileChange}
                  disabled={uploading}
                />
              </label>
              <div className="text-xs text-gray-400 mt-2">
                Supported formats: Excel (.xlsx, .xls) or CSV
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={handleClose}
            className="px-5 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
            disabled={uploading}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!selectedFile || !uploadMonth || uploading}
            className={`px-5 py-2 rounded-lg font-semibold transition ${
              !selectedFile || !uploadMonth || uploading
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-indigo-600 text-white hover:bg-indigo-700 cursor-pointer'
            }`}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
}