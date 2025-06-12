import api from './api';

export const getAllProjects = async (page = 1, pageSize = 10) => {
  try {
    const response = await api.get(`/api/v1/projects?page=${page}&page_size=${pageSize}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
};

export const getProjectById = async (projectId) => {
  try {
    const response = await api.get(`/api/v1/projects/${projectId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching project ${projectId}:`, error);
    throw error;
  }
};

export const getProjectIndexInfo = async (projectId) => {
  try {
    const response = await api.get(`/api/v1/nlp/index/info/${projectId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching project index info ${projectId}:`, error);
    throw error;
  }
};