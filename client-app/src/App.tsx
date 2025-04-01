import { Routes, Route } from "react-router-dom";
import { Box, CssBaseline } from "@mui/material";
import Sidebar from "./components/Sidebar";
import ResearchSummarizer from "./pages/ResearchSummarizer";
import Appbar from "./components/Appbar";
import GuideList from "./components/GuideList";
import GuideDetails from "./components/GuideDetails";
import CreateGuide from "./pages/CreateGuide";
import './App.css'; // Import your CSS file for global styles

const drawerWidth = 240; // Sidebar width
const appBarHeight = 64; // Adjust based on Appbar height

function App() {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <CssBaseline />

      {/* Appbar - Fixed at the top */}
      <Box sx={{ width: "100%", position: "fixed", zIndex: 1200 }}>
        <Appbar />
      </Box>

      {/* Content Wrapper */}
      <Box sx={{ display: "flex", flexGrow: 1, marginTop: `${appBarHeight}px` }}>
        
        {/* Sidebar - Fixed on the left */}
        <Box sx={{
          width: `${drawerWidth}px`,
          flexShrink: 0,
          paddingTop: `${appBarHeight}px`, // Adjust padding to start below Appbar
          position: "fixed",
          height: `calc(100vh - ${appBarHeight}px)`, // Adjust height after Appbar
          top: `${appBarHeight}px`, // Start below Appbar
          left: 0,
          overflowY: "auto",
          backgroundColor: "background.paper",
          zIndex: 1100, // Ensures Sidebar is below Appbar but above content
        }}>
          <Sidebar />
        </Box>

        {/* Main Content - Positioned properly */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            marginLeft: `${drawerWidth}px`, // Push content to the right of Sidebar
            overflowY: "auto",
          }}
        >
          <Routes>
            <Route path="/" element={<ResearchSummarizer />} />
            <Route path="/guides" element={<GuideList />} />
            <Route path="/guides/:taskId" element={<GuideDetails />} />
            <Route path="/guides/create" element={<CreateGuide />} />
          </Routes>
        </Box>

      </Box>
    </Box>
  );
}

export default App;
