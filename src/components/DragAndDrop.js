import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';

const DragAndDrop = ({ onFilesAdded, resetFiles }) => {
  // Local state for accepted and rejected files
  const [acceptedFileItems, setAcceptedFileItems] = useState([]);
  const [fileRejectionItems, setFileRejectionItems] = useState([]);

  // Set the onDrop callback
  const onDrop = useCallback(
    (acceptedFiles, rejectedFiles) => {
      // Pass the accepted files to the parent component
      if (onFilesAdded) {
        onFilesAdded(acceptedFiles);
      }
      // Update local state
      setAcceptedFileItems(acceptedFiles);
      setFileRejectionItems(rejectedFiles);
    },
    [onFilesAdded]
  );

  // UseDropzone hook
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf'],
    },
    multiple: true,
  });

  // Reset files when resetFiles changes
  useEffect(() => {
    if (resetFiles) {
      setAcceptedFileItems([]);
      setFileRejectionItems([]);
    }
  }, [resetFiles]);

  // Display accepted files
  const acceptedFilesList = acceptedFileItems.map((file) => (
    <li key={file.path || file.name} className="text-green-600">
      {file.name}
    </li>
  ));

  // Display rejected files
  const fileRejectionItemsList = fileRejectionItems.map(({ file, errors }) => (
    <li key={file.path || file.name} className="text-red-600">
      {file.name}
      <ul>
        {errors.map((e) => (
          <li key={e.code} className="text-red-500">
            {e.message}
          </li>
        ))}
      </ul>
    </li>
  ));

  return (
    <div
      {...getRootProps()}
      className={`border-dashed border-4 p-6 rounded-md text-center cursor-pointer relative z-0 ${
        isDragActive ? 'border-secondary-500' : 'border-gray-400'
      }`}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p className="text-gray-700">Suelta los archivos aquí...</p>
      ) : (
        <p className="text-gray-700">
          Arrastra y suelta archivos aquí, o haz click para seleccionar archivos
        </p>
      )}
      <aside className="mt-4">
        {acceptedFileItems.length > 0 && (
          <>
            <h4 className="font-semibold">Archivos aceptados</h4>
            <ul>{acceptedFilesList}</ul>
          </>
        )}
        {fileRejectionItems.length > 0 && (
          <>
            <h4 className="font-semibold mt-2">Archivos rechazados</h4>
            <ul>{fileRejectionItemsList}</ul>
          </>
        )}
      </aside>
    </div>
  );
};

export default DragAndDrop;
