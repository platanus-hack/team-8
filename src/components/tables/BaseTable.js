'use client';
import { FaTrash, FaEdit, FaEye } from 'react-icons/fa';

const Table = ({ data, styleVariant = 'style1', onView, onEdit, onDelete, headersToIgnore = [], headersMapping = {} }) => {
  if (!data || data.length === 0) {
    return <p className="text-center">No data available.</p>;
  }

  // Extract table headers from object keys
  const headers = Object.keys(data[0]);

  // Remove headers to ignore
  const filteredHeaders = headers.filter(header => !headersToIgnore.includes(header));

  // Map headers to custom names
  const mappedHeaders = filteredHeaders.map(header => headersMapping[header] || header);

  return (
    <div className="overflow-x-auto mx-10">
      <table className={`min-w-full ${getTableStyles(styleVariant)}`}>
        <thead>
          <tr>
            {mappedHeaders.map((header) => (
              <th key={header} className={getHeaderCellStyles(styleVariant)}>
                {header.charAt(0).toUpperCase() + header.slice(1)}
              </th>
            ))}
            <th className={getHeaderCellStyles(styleVariant)}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              className={getRowStyles(styleVariant, idx)}
            >
              {filteredHeaders.map((header) => (
                <td key={header} className={getCellStyles(styleVariant)}>
                  {row[header]}
                </td>
              ))}
              <td className={getCellStyles(styleVariant)}>
                <div className="flex justify-center space-x-2">
                  <button
                    onClick={() => onView(row)}
                    className="text-secondary hover:text-primary text-xl"
                    title="Ver"
                  >
                    <FaEye />
                  </button>
                  <button
                    onClick={() => onEdit(row)}
                    className="text-secondary hover:text-primary text-xl"
                    title="Editar"
                  >
                    <FaEdit />
                  </button>
                  {/* <button
                    onClick={() => onDownload(row)}
                    className="text-green-600 hover:text-green-800 text-lg"
                    title="Download"
                  >
                    <FaDownload />
                  </button> */}
                  <button
                    onClick={() => onDelete(row)}
                    className="text-secondary hover:text-primary text-xl"
                    title="Eliminar"
                  >
                    <FaTrash />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Helper functions to get styles based on variant
const getTableStyles = (variant) => {
  switch (variant) {
    case 'style2':
      return 'border-collapse border border-gray-300';
    case 'style3':
      return '';
    default:
      return 'divide-y divide-gray-200';
  }
};

const getHeaderCellStyles = (variant) => {
  switch (variant) {
    case 'style2':
      return 'px-6 py-3 border border-gray-300 bg-gray-100 text-left text-sm font-medium text-gray-700';
    case 'style3':
      return 'px-6 py-3 bg-primary text-white text-left text-sm font-semibold';
    default:
      return 'px-6 py-3 bg-gray-50 text-left text-sm font-medium text-gray-700';
  }
};

const getCellStyles = (variant) => {
  switch (variant) {
    case 'style2':
      return 'px-6 py-4 border border-gray-300 text-sm text-gray-700';
    case 'style3':
      return 'px-6 py-4 text-sm text-gray-800';
    default:
      return 'px-6 py-4 text-sm text-gray-700';
  }
};

const getRowStyles = (variant, idx) => {
  switch (variant) {
    case 'style3':
      return 'hover:bg-gray-100';
    default:
      return idx % 2 === 0 ? 'bg-white' : 'bg-gray-50';
  }
};

export { Table };
