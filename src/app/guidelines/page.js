'use client';
import { UploadPage } from '@/components/UploadPage';
import { Table } from '@/components/tables';
import { configFile } from '../../config';
import { useRouter } from 'next/navigation';
import { getAllGuidelines } from '../../api';
import { useEffect, useState } from 'react';

export default function GuidelinesPage() {
  const router = useRouter();
  const [allGuidelines, setAllGuidelines] = useState([]);

  // Table actions
  const handleView = (guideline) => {
    // Go to the guideline page
    router.push(`/guidelines/${guideline.id}/tests`);
  }
  const handleEdit = (guideline) => {
    console.log("Editing guideline:", guideline);
  }
  const handleDownload = (guideline) => {
    console.log("Downloading guideline:", guideline);
  };
  const handleDelete = (guideline) => {
    console.log("Deleting guideline:", guideline);
  }

  // Rename the function to avoid conflict with the imported function
  const fetchGuidelines = async () => {
    try {
      const guidelines = await getAllGuidelines();
      setAllGuidelines(guidelines);
      console.log("Guidelines:", guidelines);
    } catch (error) {
      console.error('Error fetching guidelines:', error);
    }
  }

  useEffect(() => {
    fetchGuidelines();
  }, []);

  const showTable = allGuidelines?.data?.length > 0;

  const headersToIgnore = ['id', 'created_at', 's3_link', 'professor_id', 's3_filename'];
  const headersMapping = {
    "max_score": "Puntaje máximo",
    "title": "Título",
    "topic": "Tema",
  }

  return (
    <div className='mb-5'>

      {/* Drag and Drop Upload */}
      <UploadPage 
        apiEndpoint={`${configFile.API_BASE_URL}/saveFile/`} 
        method="POST"
        elementToDrop="pautas"
        fetchFunction={fetchGuidelines}
      />

      {/* Guidelines Table */}
      <div className="flex justify-center items-center my-4">
        <h1 className="text-2xl font-bold">Tus pautas</h1>
      </div>

      {showTable && ( 
        <Table 
          data={allGuidelines.data} 
          styleVariant="style2" 
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
          headersToIgnore={headersToIgnore}
          headersMapping={headersMapping}
        />
      )}
    </div>
  )
}