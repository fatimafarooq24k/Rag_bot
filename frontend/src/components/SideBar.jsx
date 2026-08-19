import {
  AnimatePresence,
  motion
} from "framer-motion";

import {
  FileText,
  Plus,
  X
} from "lucide-react";

import DocumentList from "./DocumentList";


function Sidebar({
  documents,
  selectedDocument,
  onSelect,
  onDelete,
  loading,
  onUpload,
  uploading,
  mobileOpen,
  onClose
}) {

  return (

    <>

      <AnimatePresence>

        {mobileOpen && (

          <motion.div
            className="sidebar-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

        )}

      </AnimatePresence>


      <aside
        className={`sidebar ${
          mobileOpen
            ? "sidebar-open"
            : ""
        }`}
      >

        <div className="sidebar-header">

          <div className="brand">

            <div className="brand-icon">
              ✦
            </div>

            <div>

              <h1>DocuMind</h1>

              <span>
                AI Document Assistant
              </span>

            </div>

          </div>


          <button
            className="close-sidebar"
            onClick={onClose}
          >
            <X size={20} />
          </button>

        </div>


        <button
          className="upload-button"
          onClick={() => {
            document
              .getElementById(
                "sidebar-file-input"
              )
              ?.click();
          }}
          disabled={uploading}
        >

          <Plus size={19} />

          {uploading
            ? "Processing..."
            : "Upload PDF"}

        </button>


        <input
          id="sidebar-file-input"
          type="file"
          accept=".pdf"
          hidden
          onChange={(event) => {

            const file =
              event.target.files?.[0];

            if (file) {
              onUpload(file);
            }

            event.target.value = "";

          }}
        />


        <div className="documents-heading">

          <span>
            YOUR DOCUMENTS
          </span>

          <span className="document-count">
            {documents.length}
          </span>

        </div>


        <DocumentList
          documents={documents}
          selectedDocument={selectedDocument}
          onSelect={onSelect}
          onDelete={onDelete}
          loading={loading}
        />


        <div className="sidebar-footer">

          <FileText size={15} />

          <span>
            Private document workspace
          </span>

        </div>

      </aside>

    </>
  );
}

export default Sidebar;