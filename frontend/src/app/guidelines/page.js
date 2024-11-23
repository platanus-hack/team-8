'use client'
import React, { useState } from 'react';
import DragAndDrop from '@/components/DragAndDrop';

const UploadPage = () => {
  const [files, setFiles] = useState([]);

  const handleFilesAdded = (newFiles) => {
    setFiles((currentFiles) => [...currentFiles, ...newFiles]);
  };

  // Set formData and send to backend
  const handleUpload = async () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    // TODO: Change to backend endpoint
    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert('Archivos subidos correctamente!');
        setFiles([]); // Clear the files after successful upload
      } else {
        alert('No se pudieron subir los archivos.');
      }
    } catch (error) {
      console.error('Error al subir archivos:', error);
      alert('Error al subir archivos.');
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Sube tus pautas</h1>
      <DragAndDrop onFilesAdded={handleFilesAdded} />
      {files.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Archivos a subir:</h2>
          <ul className="list-disc list-inside">
            {files.map((file) => (
              <li key={file.path || file.name}>
                {file.name} - {file.size} bytes
              </li>
            ))}
          </ul>
          <button
            onClick={handleUpload}
            className="mt-4 bg-primary hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Subir archivos
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadPage;
