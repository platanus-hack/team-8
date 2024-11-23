import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const DragAndDrop = ({ onFilesAdded }) => {
  const onDrop = useCallback(
    (acceptedFiles, rejectedFiles) => {
      // Pass the accepted files to the parent component
      if (onFilesAdded) {
        onFilesAdded(acceptedFiles);
      }
    },
    [onFilesAdded]
  );

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    acceptedFiles,
    fileRejections,
  } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf'],
    },
    multiple: true,
  });

  const acceptedFileItems = acceptedFiles.map((file) => (
    <li key={file.path} className="text-green-600">
      {file.path} - {file.size} bytes
    </li>
  ));

  const fileRejectionItems = fileRejections.map(({ file, errors }) => (
    <li key={file.path} className="text-red-600">
      {file.path} - {file.size} bytes
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
      className={`border-dashed border-4 p-6 rounded-md text-center cursor-pointer ${
        isDragActive ? 'border-blue-500' : 'border-gray-400'
      }`}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p className="text-gray-700">Drop the files here ...</p>
      ) : (
        <p className="text-gray-700">
          Drag and drop some files here, or click to select files
        </p>
      )}
      <aside className="mt-4">
        {acceptedFiles.length > 0 && (
          <>
            <h4 className="font-semibold">Accepted files</h4>
            <ul>{acceptedFileItems}</ul>
          </>
        )}
        {fileRejections.length > 0 && (
          <>
            <h4 className="font-semibold mt-2">Rejected files</h4>
            <ul>{fileRejectionItems}</ul>
          </>
        )}
      </aside>
    </div>
  );
};

export default DragAndDrop;
