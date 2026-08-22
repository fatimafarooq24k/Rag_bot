import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import {
  Send,
  FileText,
  Sparkles,
  Loader2
} from "lucide-react";

import MessageBubble from "./MessageBubble";
import MetadataBar from "./MetadataBar";


function ChatWindow({ document, onAsk, messages, onUpdateMessages }) {

  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);

  const messagesEndRef = useRef(null);

  // NOTE: no more "clear messages on doc change" effect —
  // messages now come from the parent, keyed by doc_id.

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, asking]);


  async function handleSubmit(event) {

    event.preventDefault();

    const trimmed = question.trim();
    if (!trimmed || asking) return;

    setQuestion("");

    onUpdateMessages((previous) => [
      ...previous,
      { id: Date.now(), role: "user", content: trimmed }
    ]);

    try {

      setAsking(true);

      const result = await onAsk(document.doc_id, trimmed);

      onUpdateMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: result.answer
        }
      ]);

    } catch (error) {

      onUpdateMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          role: "assistant",
          error: true,
          content:
            error.message ||
            "Something went wrong while generating the answer."
        }
      ]);

    } finally {
      setAsking(false);
    }
  }


  return (

    <motion.div
      className="chat-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      key={document.doc_id}
    >

      <header className="chat-header">

        <div className="active-document">
          <div className="active-document-icon">
            <FileText size={22} />
          </div>
          <div>
            <h2>{document.filename}</h2>
          </div>
        </div>

        <div className="ai-badge">
          <Sparkles size={15} />
          AI Ready
        </div>

      </header>

      <MetadataBar document={document} />

      <div className="chat-messages">

        {messages.length === 0 ? (

          <motion.div
            className="chat-welcome"
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="welcome-icon">
              <Sparkles size={25} />
            </div>

            <h2>Ask anything about this document</h2>

            <p>
              I'll search through <strong>{document.filename}</strong>{" "}
              and answer using only its contents.
            </p>

            <div className="suggestions">
              <button onClick={() => setQuestion("Summarize this document.")}>
                Summarize this document
              </button>
              <button onClick={() => setQuestion("What are the main topics discussed?")}>
                Main topics
              </button>
              <button onClick={() => setQuestion("What are the key takeaways?")}>
                Key takeaways
              </button>
            </div>

          </motion.div>

        ) : (

          <AnimatePresence initial={false}>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
          </AnimatePresence>

        )}

        {asking && (

          <motion.div
            className="typing-message"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="avatar assistant-avatar">✦</div>
            <div className="typing-bubble">
              <Loader2 size={17} className="spin" />
              Searching document...
            </div>
          </motion.div>

        )}

        <div ref={messagesEndRef} />

      </div>

      <div className="chat-input-area">

        <form className="chat-form" onSubmit={handleSubmit}>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask something about your document..."
            rows={1}
            disabled={asking}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                handleSubmit(event);
              }
            }}
          />

          <motion.button
            type="submit"
            className="send-button"
            disabled={!question.trim() || asking}
            whileTap={{ scale: 0.9 }}
          >
            <Send size={18} />
          </motion.button>

        </form>

        <p className="input-hint">
          Press Enter to send • Shift + Enter for a new line
        </p>

      </div>

    </motion.div>
  );
}

export default ChatWindow;