import ReactMarkdown from "react-markdown";

import {
  motion
} from "framer-motion";

import {
  User,
  Sparkles
} from "lucide-react";


function MessageBubble({
  message
}) {

  const isUser =
    message.role === "user";


  return (

    <motion.div
      className={`message-row ${
        isUser
          ? "message-user"
          : "message-assistant"
      }`}
      initial={{
        opacity: 0,
        y: 12
      }}
      animate={{
        opacity: 1,
        y: 0
      }}
      transition={{
        duration: 0.25
      }}
    >

      <div
        className={`avatar ${
          isUser
            ? "user-avatar"
            : "assistant-avatar"
        }`}
      >

        {isUser
          ? <User size={17} />
          : <Sparkles size={17} />}

      </div>


      <div
        className={`message-bubble ${
          message.error
            ? "message-error"
            : ""
        }`}
      >

        <div className="message-content">

          {isUser ? (
            message.content
          ) : (
            <ReactMarkdown>
              {message.content}
            </ReactMarkdown>
          )}

        </div>

      </div>

    </motion.div>
  );
}

export default MessageBubble;