import DocumentCard from "./DocumentCard";
import Loading from "./Loading";


function DocumentList({
  documents,
  selectedDocument,
  onSelect,
  onDelete,
  loading
}) {

  if (loading) {

    return (

      <div className="document-list">

        <Loading />
        <Loading />
        <Loading />

      </div>

    );
  }


  if (!documents.length) {

    return (

      <div className="no-documents">

        <div className="no-documents-icon">
          ◇
        </div>

        <p>No documents yet</p>

        <span>
          Upload a PDF to get started
        </span>

      </div>

    );
  }


  return (

    <div className="document-list">

      {documents.map((document) => (

        <DocumentCard
          key={document.doc_id}
          document={document}
          selected={
            selectedDocument?.doc_id ===
            document.doc_id
          }
          onSelect={onSelect}
          onDelete={onDelete}
        />

      ))}

    </div>
  );
}

export default DocumentList;