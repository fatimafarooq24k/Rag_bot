import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import UploadZone from "./components/UploadZone";
import EmptyState from "./components/EmptyState";

import {
  getDocuments,
  uploadDocument,
  deleteDocument,
  askQuestion
} from "./services/api";


function App() {

  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [mobileSidebar, setMobileSidebar] = useState(false);

  // NEW: chat history per document, keyed by doc_id
  const [chatsByDoc, setChatsByDoc] = useState({});


  async function loadDocuments() {

    try {
      setLoadingDocuments(true);
      setError("");

      const data = await getDocuments();
      setDocuments(data);

      if (data.length > 0 && !selectedDocument) {
        setSelectedDocument(data[0]);
      }

    } catch (err) {
      setError(err.message || "Unable to load documents.");
    } finally {
      setLoadingDocuments(false);
    }
  }


  useEffect(() => {
    loadDocuments();
  }, []);


  async function handleUpload(file) {

    try {
      setUploading(true);
      setError("");

      const document = await uploadDocument(file);

      setDocuments((previous) => [document, ...previous]);
      setSelectedDocument(document);

    } catch (err) {
      setError(err.message || "Failed to upload document.");
    } finally {
      setUploading(false);
    }
  }


  async function handleDelete(docId) {

    try {
      setError("");

      await deleteDocument(docId);

      setDocuments((previous) =>
        previous.filter((doc) => doc.doc_id !== docId)
      );

      // NEW: also clean up that document's chat history
      setChatsByDoc((previous) => {
        const next = { ...previous };
        delete next[docId];
        return next;
      });

      if (selectedDocument?.doc_id === docId) {
        setSelectedDocument(null);
      }

    } catch (err) {
      setError(err.message || "Failed to delete document.");
    }
  }


  function handleSelect(document) {
    setSelectedDocument(document);
    setMobileSidebar(false);
  }


  // NEW: helper passed to ChatWindow so it can update this doc's messages
  function updateMessages(docId, updater) {

    setChatsByDoc((previous) => {

      const current = previous[docId] || [];
      const nextMessages =
        typeof updater === "function" ? updater(current) : updater;

      return {
        ...previous,
        [docId]: nextMessages
      };
    });
  }


  return (

    <div className="app">

      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />

      <Sidebar
        documents={documents}
        selectedDocument={selectedDocument}
        onSelect={handleSelect}
        onDelete={handleDelete}
        loading={loadingDocuments}
        onUpload={handleUpload}
        uploading={uploading}
        mobileOpen={mobileSidebar}
        onClose={() => setMobileSidebar(false)}
      />

      <main className="main-content">

        <header className="mobile-header">
          <button className="menu-button" onClick={() => setMobileSidebar(true)}>
            ☰
          </button>
          <div className="mobile-logo">
            <span>✦</span>
            DocuMind
          </div>
        </header>

        <AnimatePresence>
          {error && (
            <motion.div
              className="error-banner"
              initial={{ opacity: 0, y: -15 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -15 }}
            >
              <span>⚠</span>
              {error}
              <button onClick={() => setError("")}>×</button>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="content-wrapper">

          {!selectedDocument ? (

            <motion.div
              className="welcome-screen"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <EmptyState />
              <UploadZone onUpload={handleUpload} uploading={uploading} />
            </motion.div>

          ) : (

            <ChatWindow
              document={selectedDocument}
              onAsk={askQuestion}
              messages={chatsByDoc[selectedDocument.doc_id] || []}
              onUpdateMessages={(updater) =>
                updateMessages(selectedDocument.doc_id, updater)
              }
            />

          )}

        </div>

      </main>

    </div>
  );
}

export default App;