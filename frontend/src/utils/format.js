export function formatFileSize(bytes) {

  if (!bytes) {
    return "Unknown size";
  }

  const units = [
    "B",
    "KB",
    "MB",
    "GB"
  ];

  let size = bytes;
  let index = 0;

  while (
    size >= 1024 &&
    index < units.length - 1
  ) {

    size /= 1024;
    index++;

  }

  return `${size.toFixed(
    index === 0 ? 0 : 1
  )} ${units[index]}`;
}


export function formatDate(date) {

  if (!date) {
    return "";
  }

  return new Date(date).toLocaleDateString(
    undefined,
    {
      year: "numeric",
      month: "short",
      day: "numeric"
    }
  );
}