import {
  useRef,
  useState
} from "react";

import {
  motion
} from "framer-motion";

import {
  Upload,
  FileUp
} from "lucide-react";


function UploadZone({
  onUpload,
  uploading
}) {

  const inputRef = useRef(null);

  const [dragging, setDragging] =
    useState(false);


  function processFile(file) {

    if (!file) return;

    if (
      file.type !== "application/pdf" &&
      !file.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {

      alert(
        "Please select a PDF file."
      );

      return;
    }

    if (
      file.size >
      100 * 1024 * 1024
    ) {

      alert(
        "PDF must be smaller than 100MB."
      );

      return;
    }

    onUpload(file);
  }


  return (

    <motion.div
      className={`upload-zone ${
        dragging
          ? "upload-zone-dragging"
          : ""
      }`}
      initial={{
        opacity: 0,
        y: 20
      }}
      animate={{
        opacity: 1,
        y: 0
      }}
      transition={{
        delay: 0.2
      }}
      onDragOver={(event) => {

        event.preventDefault();

        setDragging(true);

      }}
      onDragLeave={() =>
        setDragging(false)
      }
      onDrop={(event) => {

        event.preventDefault();

        setDragging(false);

        processFile(
          event.dataTransfer.files?.[0]
        );

      }}
      onClick={() =>
        inputRef.current?.click()
      }
    >

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        hidden
        onChange={(event) =>
          processFile(
            event.target.files?.[0]
          )
        }
      />


      <motion.div
        className="upload-icon"
        animate={
          dragging
            ? {
                scale: 1.1,
                y: -5
              }
            : {
                scale: 1,
                y: 0
              }
        }
      >

        {uploading
          ? <FileUp size={27} />
          : <Upload size={27} />}

      </motion.div>


      <h3>

        {uploading
          ? "Processing your document..."
          : "Drop your PDF here"}

      </h3>


      <p>

        {uploading
          ? "Extracting, chunking and indexing"
          : "or click to browse your files"}

      </p>


      {!uploading && (

        <span className="upload-limit">
          PDF • Maximum 100MB
        </span>

      )}

    </motion.div>
  );
}

export default UploadZone;