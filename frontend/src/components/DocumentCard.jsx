import {
  motion
} from "framer-motion";

import {
  FileText,
  Trash2,
  CheckCircle
} from "lucide-react";

import {
  formatFileSize,
  formatDate
} from "../utils/format";


function DocumentCard({
  document,
  selected,
  onSelect,
  onDelete
}) {

  function handleDelete(event) {

    event.stopPropagation();

    const confirmed =
      window.confirm(
        `Delete "${document.filename}"?`
      );

    if (confirmed) {
      onDelete(document.doc_id);
    }
  }


  return (

    <motion.div
      className={`document-card ${
        selected
          ? "document-card-selected"
          : ""
      }`}
      whileHover={{
        x: 3
      }}
      whileTap={{
        scale: 0.98
      }}
      onClick={() =>
        onSelect(document)
      }
      layout
    >

      <div className="document-icon">

        <FileText size={20} />

      </div>


      <div className="document-info">

        <div
          className="document-name"
          title={document.filename}
        >
          {document.filename}
        </div>

        <div className="document-meta">

          {formatFileSize(
            document.file_size
          )}

          <span>•</span>

          {document.chunk_count || 0}
          {" chunks"}

        </div>

      </div>


      {selected && (

        <CheckCircle
          className="selected-icon"
          size={17}
        />

      )}


      <button
        className="delete-button"
        onClick={handleDelete}
        title="Delete document"
      >
        <Trash2 size={15} />
      </button>

    </motion.div>
  );
}

export default DocumentCard;