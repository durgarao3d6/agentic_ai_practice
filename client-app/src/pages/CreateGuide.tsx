import React, { useState } from "react";
import { TextField, Button, Container, Typography } from "@mui/material";
import { createGuide } from "../services/guideService";

const CreateGuide: React.FC = () => {
  const [topic, setTopic] = useState("");
  const [audienceLevel, setAudienceLevel] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await createGuide({ topic, audience_level: audienceLevel });
      setMessage(response.message);
      setTopic("");
      setAudienceLevel("");
    } catch (error) {
      setMessage("Error creating guide. Please try again.");
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom>Create a Guide</Typography>
      
      <TextField
        fullWidth
        label="Topic"
        variant="outlined"
        margin="normal"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />
      
      <TextField
        fullWidth
        label="Audience Level"
        variant="outlined"
        margin="normal"
        value={audienceLevel}
        onChange={(e) => setAudienceLevel(e.target.value)}
      />

      <Button 
        variant="contained" 
        color="primary" 
        fullWidth 
        onClick={handleSubmit} 
        disabled={loading}
        style={{ marginTop: 16 }}
      >
        {loading ? "Creating..." : "Create Guide"}
      </Button>

      {message && <Typography color="secondary" style={{ marginTop: 16 }}>{message}</Typography>}
    </Container>
  );
};

export default CreateGuide;
