import { motion } from "framer-motion";

import { getDisplayableMetadata } from "../utils/format";


function MetadataBar({ document }) {

  const metadata = getDisplayableMetadata(document);

  if (!metadata.length) {
    return null;
  }

  return (

    <motion.div
      className="metadata-bar"
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
    >

      {metadata.map((item) => (

        <div className="metadata-pill" key={item.key}>

          <span className="metadata-label">
            {item.label}
          </span>

          <span className="metadata-value">
            {item.value}
          </span>

        </div>

      ))}

    </motion.div>
  );
}

export default MetadataBar;