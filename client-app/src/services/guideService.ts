import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export interface Guide {
  task_id: string;
  title: string;
  file: string;
}

export interface GuideContent {
  task_id: string;
  content: string;
}

interface CreateGuideRequest {
  topic: string;
  audience_level: string;
}

interface CreateGuideResponse {
  success: boolean;
  message: string;
}

export const getGuideList = async (): Promise<Guide[]> => {
  try {
    const response = await axios.get<Guide[]>(
      `${API_BASE_URL}/flow/list_guides`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching guide list:", error);
    return [];
  }
};

export const fetchGuideContent = async (taskId: string) => {
  try {
    const response = await axios.get<GuideContent>(
      `${API_BASE_URL}/flow/guide_content/${taskId}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching guide content:", error);
    return null;
  }
};

export const createGuide = async (
  data: CreateGuideRequest
): Promise<CreateGuideResponse> => {
  try {
    const response = await axios.post<CreateGuideResponse>(
      `${API_BASE_URL}/flow/create_guide`,
      data
    );
    return response.data;
  } catch (error) {
    console.error("Error creating guide:", error);
    throw new Error("Failed to create guide");
  }
};
