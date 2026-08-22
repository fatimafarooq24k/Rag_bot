export function formatFileSize(bytes) {
  if (!bytes) {
    return "Unknown size";
  }

  const units = ["B", "KB", "MB", "GB"];

  let size = bytes;
  let index = 0;

  while (size >= 1024 && index < units.length - 1) {
    size /= 1024;
    index++;
  }

  return `${size.toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}


export function formatDateTime(date) {
  if (!date) {
    return "";
  }

  const parsedDate = new Date(date);

  if (Number.isNaN(parsedDate.getTime())) {
    return String(date);
  }

  return parsedDate.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
  });
}


/* -----------------------------
   METADATA BAR HELPERS
----------------------------- */

/*
  These fields should not appear in the metadata bar.

  - doc_id is internal
  - filename is already displayed in the header
  - processing_time is intentionally hidden
*/

const HIDDEN_METADATA_KEYS = new Set([
  "doc_id",
  "filename",
  "file_upload",
  "processing_time"
]);


export function getDisplayableMetadata(document) {
  if (!document) {
    return [];
  }

  return Object.entries(document)
    .filter(([key, value]) => {

      // Hide unwanted metadata
      if (HIDDEN_METADATA_KEYS.has(key)) {
        return false;
      }

      // Hide empty values
      if (value === null || value === undefined) {
        return false;
      }

      // Skip nested objects
      if (typeof value === "object") {
        return false;
      }

      return true;
    })
    .map(([key, value]) => ({
      key,
      label: formatMetaKey(key),
      value: formatMetaValue(key, value)
    }));
}


export function formatMetaKey(key) {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
}


export function formatMetaValue(key, value) {

  // Boolean values
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }


  // File size
  if (key.toLowerCase().includes("size")) {
    return formatFileSize(value);
  }


  /*
    Format upload time / timestamps.

    Example:
    2026-08-20T15:28:56.034399

    Becomes:
    Aug 20, 2026, 03:28 PM
  */
  if (
    key.toLowerCase().includes("date") ||
    key.toLowerCase().includes("time") ||
    key.toLowerCase().includes("_at")
  ) {
    return formatDateTime(value);
  }


  // Numbers such as chunks and embeddings
  if (typeof value === "number") {
    return value.toLocaleString();
  }


  return String(value);
}