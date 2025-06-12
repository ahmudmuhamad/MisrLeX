import api from './api';

export const uploadFile = async (projectId, file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/api/v1/data/upload/${projectId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};

export const processFile = async (projectId, fileId, chunkSize = 1000, overlapSize = 200, doReset = 0) => {
  try {
    const response = await api.post(`/api/v1/data/process/${projectId}`, {
      file_id: fileId,
      chunk_size: chunkSize,
      overlap_size: overlapSize,
      do_reset: doReset
    });
    return response.data;
  } catch (error) {
    console.error('Error processing file:', error);
    throw error;
  }
};

export const indexProject = async (projectId, doReset = 0) => {
  try {
    const response = await api.post(`/api/v1/nlp/index/push/${projectId}`, {
      do_reset: doReset
    });
    return response.data;
  } catch (error) {
    console.error('Error indexing project:', error);
    throw error;
  }
};