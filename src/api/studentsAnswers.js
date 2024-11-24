import axios from 'axios';
import { configFile } from '../config';

// Get all tests of a guideline
export const getAllStudentsAnswerByTestId = async (testId) => {
  try {
    const requestOptions = {
      params: {
        test_id: testId
      }
    }
    const response = await axios.get(`${configFile.API_BASE_URL}/students_answers/${testId}`, requestOptions);
    return response.data;
  } catch (error) {
    console.error(`Error al obtener los tests de la pauta con id ${testId}: ${error}`);
    return null;
  }
}
