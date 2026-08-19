import {
  motion
} from "framer-motion";


function Loading() {

  return (

    <div className="loading-document">

      <motion.div
        className="loading-icon"
        animate={{
          opacity: [0.4, 1, 0.4]
        }}
        transition={{
          duration: 1.4,
          repeat: Infinity
        }}
      />

      <div className="loading-lines">

        <motion.div
          className="loading-line"
          animate={{
            opacity: [0.4, 1, 0.4]
          }}
          transition={{
            duration: 1.4,
            repeat: Infinity
          }}
        />

        <div className="loading-line-small" />

      </div>

    </div>
  );
}

export default Loading;