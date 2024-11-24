import axios from 'axios';
import { configFile } from '../config';

// Get all guidelines
export const getAllGuidelines = async () => {
  try {
    const response = await axios.get(`${configFile.API_BASE_URL}/guidelines/`);
    return response.data;
  } catch (error) {
    console.error(`Error al obtener todas las pautas: ${error}`);
    return null;
  }
}

// Get a guideline by id
// This is going to be used to get the insights of the guideline
export const getGuidelineById = async (id) => {
  try {
    const response = await axios.get(`${configFile.API_BASE_URL}/guidelines/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error al obtener la pauta con id ${id}: ${error}`);
    return null;
  }
}

// Create a guideline
// This is not strictly necessary
export const createGuideline = async (formData) => {
  try {
    const headers = axios.defaults.headers.common;
    headers['Content-Type'] = 'multipart/form-data';
    headers['Access-Control-Allow-Origin'] = '*';
    const response = await axios.post(`${configFile.API_BASE_URL}/guidelines`, data, { headers });
    return response.data;
  } catch (error) {
    console.error(`Error al crear la pauta: ${error}`);
    return null;
  }
}

// Update a guideline
export const updateGuideline = async (id, data) => {
  try {
    const response = await axios.put(`${configFile.API_BASE_URL}/guidelines/${id}`, data);
    return response.data;
  } catch (error) {
    console.error(`Error al actualizar la pauta con id ${id}: ${error}`);
    return null;
  }
}

// Delete a guideline
export const deleteGuideline = async (id) => {
  try {
    const response = await axios.delete(`${configFile.API_BASE_URL}/guidelines/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error al eliminar la pauta con id ${id}: ${error}`);
    return null;
  }
}