import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Container, Typography, CircularProgress } from "@mui/material";
import { fetchGuideContent } from "../services/guideService";
import MarkdownRenderer from "./MarkdownEditor";

interface GuideContent {
  task_id: string;
  content: string;
}

const GuideDetails: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const [guide, setGuide] = useState<GuideContent | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadGuide = async () => {
      try {
        const data = await fetchGuideContent(taskId!);
        setGuide(data);
      } catch (error) {
        console.error("Error fetching guide:", error);
      } finally {
        setLoading(false);
      }
    };

    loadGuide();
  }, [taskId]);

  if (loading) return <CircularProgress />;
  if (!guide) return <Typography variant="h6">Guide not found</Typography>;

  return (
    <Container sx={{ marginTop: 4 }}>
      <Typography variant="h4">{guide.task_id}</Typography>
      <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
        
        <MarkdownRenderer content={guide.content} />
      </Typography>
    </Container>
  );
};

export default GuideDetails;
