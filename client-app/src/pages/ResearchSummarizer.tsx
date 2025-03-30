import { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  CircularProgress,
} from "@mui/material";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type TokenUsage = {
  total_tokens: number;
  prompt_tokens: number;
  cached_prompt_tokens: number;
  completion_tokens: number;
  successful_requests: number;
};

type TaskOutput = {
  description: string;
  name: string | null;
  expected_output: string;
  summary: string;
  raw: string;
  pydantic: unknown | null;
  json_dict: unknown | null;
  agent: string;
  output_format: string;
};

type Summary = {
  raw: string;
  pydantic: unknown | null;
  json_dict: unknown | null;
  tasks_output: TaskOutput[];
  token_usage: TokenUsage;
};

type AgenticAIReport = {
  topic: string;
  summary: Summary;
};

const ResearchSummarizer = () => {
  const [topic, setTopic] = useState("");
  const [summary, setSummary] = useState<AgenticAIReport>();
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!topic) return;

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8045/run-research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic }),
      });

      const data = await response.json();
      setSummary(data);
    } catch (error) {
      console.error("Error fetching summary:", error);
      setSummary(undefined);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        maxWidth: "100%",
        maxHeight: "95%",
        margin: "auto",
        mt: 2,
        textAlign: "center",
        border: "1px solid #ddd",
        overflowY: "auto", // Enable vertical scrolling
        overflowX: "hidden", // Hide horizontal scrolling
        borderRadius: 2,
        padding: 3,
      }}
    >
      <Typography variant="h4" gutterBottom>
        Research Summarizer
      </Typography>
      <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
        <TextField
          label="Enter a topic"
          variant="outlined"
          fullWidth
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSummarize}
          disabled={loading}
          sx={{ whiteSpace: "nowrap" }} // Prevents text from wrapping
        >
          {loading ? <CircularProgress size={24} /> : "Summarize"}
        </Button>
      </Box>

      {summary && (
        <Box
          mt={3}
          sx={{
            textAlign: "left",
            p: 2,
            border: "1px solid #ddd",
            borderRadius: 2,
            height: "calc(100vh - 300px)", // Adjust height based on your layout needs
            overflowY: "auto", // Enable vertical scrolling
            overflowX: "hidden", // Hide horizontal scrolling
          }}
        >
          <Typography variant="h6">Summary:</Typography>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {summary.summary.raw}
          </ReactMarkdown>
        </Box>
      )}
    </Box>
  );
};

export default ResearchSummarizer;
