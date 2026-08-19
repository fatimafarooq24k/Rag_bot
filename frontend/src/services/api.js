const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


async function handleResponse(response) {

  if (!response.ok) {

    let message = "Something went wrong.";

    try {
      const data = await response.json();

      if (data.detail) {
        message = data.detail;
      }

    } catch {
      // Ignore JSON parsing errors
    }

    throw new Error(message);
  }

  return response.json();
}


/* -----------------------------
   GET DOCUMENTS
----------------------------- */

export async function getDocuments() {

  const response = await fetch(
    `${API_URL}/documents`
  );

  return handleResponse(response);
}


/* -----------------------------
   GET DOCUMENT
----------------------------- */

export async function getDocument(docId) {

  const response = await fetch(
    `${API_URL}/documents/${docId}`
  );

  return handleResponse(response);
}


/* -----------------------------
   UPLOAD DOCUMENT
----------------------------- */

export async function uploadDocument(file) {

  const formData = new FormData();

  formData.append(
    "file_upload",
    file
  );

  const response = await fetch(
    `${API_URL}/documents`,
    {
      method: "POST",
      body: formData
    }
  );

  return handleResponse(response);
}


/* -----------------------------
   DELETE DOCUMENT
----------------------------- */

export async function deleteDocument(docId) {

  const response = await fetch(
    `${API_URL}/documents/${docId}`,
    {
      method: "DELETE"
    }
  );

  return handleResponse(response);
}


/* -----------------------------
   ASK QUESTION
----------------------------- */

export async function askQuestion(
  docId,
  question
) {

  const response = await fetch(
    `${API_URL}/documents/${docId}/ask`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        question
      })
    }
  );

  return handleResponse(response);
}