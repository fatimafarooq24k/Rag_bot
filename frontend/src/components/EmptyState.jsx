import {
  motion
} from "framer-motion";

import {
  Sparkles,
  FileText,
  Search
} from "lucide-react";


function EmptyState() {

  return (

    <div className="empty-state">

      <motion.div
        className="hero-icon"
        animate={{
          y: [0, -7, 0],
          rotate: [0, 2, -2, 0]
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >

        <Sparkles size={32} />

      </motion.div>


      <motion.h1
        initial={{
          opacity: 0,
          y: 10
        }}
        animate={{
          opacity: 1,
          y: 0
        }}
      >

        Your documents,
        <br />

        <span>
          made searchable.
        </span>

      </motion.h1>


      <motion.p
        initial={{
          opacity: 0
        }}
        animate={{
          opacity: 1
        }}
        transition={{
          delay: 0.15
        }}
      >

        Upload a PDF and chat with it using
        AI-powered semantic search.

      </motion.p>


      <div className="feature-row">

        <div className="feature">

          <FileText size={18} />

          <span>
            Your documents
          </span>

        </div>


        <div className="feature">

          <Search size={18} />

          <span>
            Semantic search
          </span>

        </div>


        <div className="feature">

          <Sparkles size={18} />

          <span>
            AI answers
          </span>

        </div>

      </div>

    </div>
  );
}

export default EmptyState;