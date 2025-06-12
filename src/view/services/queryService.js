import api from './api';

export const searchIndex = async (projectId, query, limit = 10) => {
  try {
    const response = await api.post(`/api/v1/nlp/index/search/${projectId}`, {
      text: query,
      limit: limit
    });
    return response.data;
  } catch (error) {
    console.error('Error searching index:', error);
    throw error;
  }
};

export const answerQuestion = async (projectId, query, limit = 10) => {
  try {
    const response = await api.post(`/api/v1/nlp/index/answer/${projectId}`, {
      text: query,
      limit: limit
    });
    return response.data;
  } catch (error) {
    console.error('Error getting answer:', error);
    throw error;
  }
};