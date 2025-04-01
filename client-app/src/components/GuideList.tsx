import React, { useEffect, useState } from "react";
import { getGuideList, Guide } from "../services/guideService";
import {
  Container,
  Typography,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Button,
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
      <Container
        sx={{
          marginTop: 4,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Typography variant="h4" gutterBottom>
          Guide List
        </Typography>
        <Button
          variant="contained"
          color="primary"
          sx={{ marginBottom: 2 }}
          title="Create New Guide"
          onClick={() => navigate("/guides/create")}
        >
          Create New Guide
        </Button>
      </Container>
      {loading ? (
        <CircularProgress />
      ) : (
        <Container sx={{ marginTop: 4 }}>
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
                  border: "1px solid #ccc",
                  borderRadius: 1,
                  backgroundColor: "rgba(0, 0, 0, 0.05)",
                  // background: "none",
                  marginBottom: 1,
                  padding: 1,
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
