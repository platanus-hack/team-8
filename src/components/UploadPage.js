'use client'
import axios from 'axios';
import React, { useState } from 'react';
import Confetti from 'react-confetti';
import DragAndDrop from '../components/DragAndDrop';
import { useParams } from 'next/navigation';

const UploadPage = ({ apiEndpoint, method, elementToDrop, isMultipleFiles = false, fetchFunction }) => {
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [resetDropzone, setResetDropzone] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const params = useParams();

  const handleFilesAdded = (newFiles) => {
    setFiles((currentFiles) => [...currentFiles, ...newFiles]);
  };

  // Set formData and send to backend
  const handleUpload = async () => {
    const formData = new FormData();
    if (isMultipleFiles) {
      files.forEach((file) => {
        formData.append('files', file);
        formData.append('guideline_id', params.guideline_id);
      });
    } else {
      formData.append('file', files[0]);
    }

    // Get the axios headers
    const headers = axios.defaults.headers.common;
    
    // Add the Content-Type, Access-Control-Allow-Origin header to the headers object
    headers['Content-Type'] = 'multipart/form-data';
    headers['Access-Control-Allow-Origin'] = '*';

    try {
      setIsLoading(true);
      const requestOptions = {
        method: method,
        data: formData,
        url: apiEndpoint,
        headers: headers
      }
      const response = await axios(requestOptions);

      if (response.status === 200) {
        setShowConfetti(true);
        setFiles([]); // Clear the files after successful upload
        setResetDropzone(true);
        fetchFunction();
        setTimeout(() => {
          setShowConfetti(false);
        }, 3000);
      } else {
        alert('Error al subir archivos.');
      }
    } catch (error) {
      console.error('Error al subir archivos:', error);
      setResetDropzone(prev => !prev);
      setFiles([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRemoveFile = (fileToRemove) => {
    setFiles(currentFiles => 
      currentFiles.filter(file => file.path !== fileToRemove.path || file.name !== fileToRemove.name)
    );
  };

  return (
    <div className="container mx-auto p-6">

      {showConfetti && (
        <Confetti
          width={window.innerWidth}
          height={window.innerHeight}
          numberOfPieces={200}
          recycle={false}
          style={{ position: 'fixed', top: 0, left: 0, zIndex: 100 }}
        />
      )}

      <h1 className="text-2xl font-bold mb-4">Sube tus {elementToDrop}</h1>

      
      {/* Wrap DragAndDrop in a div that will show the loading animation */}
      <div className={`relative rounded-lg ${isLoading ? 'border-2 border-primary animate-pulse' : ''}`}>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-70 z-10">
            <div className="flex flex-col items-center">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
              <p className="mt-2 text-primary font-semibold">Subiendo archivos...</p>
            </div>
          </div>
        )}
        <DragAndDrop onFilesAdded={handleFilesAdded} resetFiles={resetDropzone} />
      </div>

      {files.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Archivos a subir:</h2>
          <ul className="list-disc list-inside">
            {files.map((file) => (
              <li key={file.path || file.name} className="flex items-center justify-start mb-2">
                <span>{file.name}</span>
                <button 
                  onClick={() => handleRemoveFile(file)}
                  className="ml-2 text-red-500 hover:text-red-700 text-xl text-bold"
                  aria-label="Eliminar archivo"
                >
                  ✕
                </button>
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

export { UploadPage };

// // ... existing imports ...
// const UploadPage = ({ apiEndpoint, method, elementToDrop, isMultipleFiles = false }) => {
//   const [files, setFiles] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const [resetDropzone, setResetDropzone] = useState(false);
//   const [loadingStage, setLoadingStage] = useState(0);
//   const [currentMessage, setCurrentMessage] = useState('');

//   const loadingMessages = {
//     0: [
//       "Iniciando el proceso de carga...",
//       "Preparando tus archivos...",
//       "Alistando todo para la subida...",
//       "Comenzando la transferencia..."
//     ],
//     1: [
//       "Procesando los archivos...",
//       "Analizando el contenido...",
//       "Verificando la información...",
//       "Organizando los datos..."
//     ],
//     2: [
//       "Finalizando la carga...",
//       "Últimos detalles...",
//       "Casi terminamos...",
//       "Confirmando la transferencia..."
//     ]
//   };

//   // Add this new function
//   const updateLoadingMessage = () => {
//     const messages = loadingMessages[loadingStage];
//     const randomIndex = Math.floor(Math.random() * messages.length);
//     setCurrentMessage(messages[randomIndex]);
//   };

//   // Modify the handleUpload function
//   const handleUpload = async () => {
//     setIsLoading(true);
//     setLoadingStage(0);
//     updateLoadingMessage();

//     const formData = new FormData();
//     // ... existing FormData setup ...

//     try {
//       // Stage 1
//       setTimeout(() => {
//         setLoadingStage(1);
//         updateLoadingMessage();
//       }, 2000);

//       // Stage 2
//       setTimeout(() => {
//         setLoadingStage(2);
//         updateLoadingMessage();
//       }, 4000);

//       const response = await axios(requestOptions);
//       // ... rest of the existing try block ...

//     } catch (error) {
//       // ... existing error handling ...
//     } finally {
//       setIsLoading(false);
//       setLoadingStage(0);
//     }
//   };

//   // Update the loading message display in the JSX
//   // ... existing code until the loading message ...
//           <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-70 z-10">
//             <div className="flex flex-col items-center">
//               <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
//               <p className="mt-2 text-primary font-semibold">{currentMessage}</p>
//             </div>
//           </div>