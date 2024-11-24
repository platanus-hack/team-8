import axios from 'axios';
import { configFile } from '../config';

// Get all tests of a guideline
export const getAllTestsByGuidelineId = async (guidelineId) => {
  try {
    const requestOptions = {
      params: {
        guideline_id: parseInt(guidelineId)
      }
    }
    const response = await axios.get(`${configFile.API_BASE_URL}/tests/`, requestOptions);
    return response.data;
  } catch (error) {
    console.error(`Error al obtener los tests de la pauta con id ${guidelineId}: ${error}`);
    return null;
  }
}
