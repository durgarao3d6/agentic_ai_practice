import { Drawer, List, ListItem, ListItemText } from "@mui/material";
import { Link } from "react-router-dom";

const drawerWidth = 240;
const appBarHeight = 64; // Adjust based on Appbar height

const Sidebar = () => {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          marginTop: `${appBarHeight}px`, // Push below Appbar
          height: `calc(100vh - ${appBarHeight}px)`, // Adjust height
          overflowY: "auto",
        },
      }}
    >
      <List>
        <ListItem component={Link} to="/">
          <ListItemText primary="Research Summarizer" />
        </ListItem>
        <ListItem component={Link} to="/guides">
          <ListItemText primary="Guides" />
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;
