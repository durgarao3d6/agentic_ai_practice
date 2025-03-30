import React, { useEffect, useState } from "react";
import { getGuideList, Guide } from "../services/guideService";
import {
  Container,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const GuideList: React.FC = () => {
  const [guides, setGuides] = useState<Guide[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchGuides = async () => {
      const data = await getGuideList();
      setGuides(data);
      setLoading(false);
    };
    fetchGuides();
  }, []);

  const handleClick = (taskId: string) => {
    navigate(`/guides/${taskId}`);
  };


  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Guide List
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <Container sx={{ marginTop: 4 }}>
          <Typography variant="h4">Guide List</Typography>
          <List>
            {guides.map((guide) => (
              <ListItem
                component="button"
                key={guide.task_id}
                onClick={() => handleClick(guide.task_id)}
                sx={{
                  textAlign: "left",
                  width: "100%",
                  cursor: "pointer",
                  border: "none",
                  background: "none",
                }}
              >
                <ListItemText primary={guide.title || "Untitled Guide"} />
              </ListItem>
            ))}
          </List>
        </Container>
      )}
    </Container>
  );
};

export default GuideList;
