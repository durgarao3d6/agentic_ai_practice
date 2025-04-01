import React, { useState } from "react";
import Accordion, { AccordionProps } from "@mui/material/Accordion";
import AccordionSummary, { AccordionSummaryProps } from "@mui/material/AccordionSummary";
import AccordionDetails, { AccordionDetailsProps } from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

interface IVDLAccordionItem {
  title: string;
  content: React.ReactNode;
  accordionProps?: Partial<AccordionProps>; // Allow extra customization
  summaryProps?: Partial<AccordionSummaryProps>;
  detailsProps?: Partial<AccordionDetailsProps>;
}

interface IVDLAccordionProps {
  items: IVDLAccordionItem[];
  multiple?: boolean; // Allow multiple sections to be open
}

const VDLAccordion: React.FC<IVDLAccordionProps> = ({ items, multiple = false }) => {
  const [expanded, setExpanded] = useState<string | string[] | null>(
    multiple ? [] : null
  );

  const handleChange = (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
    setExpanded((prev) => {
      if (multiple) {
        return isExpanded ? [...(prev as string[]), panel] : (prev as string[]).filter((p) => p !== panel);
      }
      return isExpanded ? panel : null;
    });
  };

  return (
    <div>
      {items.map((item, index) => (
        <Accordion
          key={index}
          expanded={multiple ? (expanded as string[]).includes(`panel${index}`) : expanded === `panel${index}`}
          onChange={handleChange(`panel${index}`)}
          {...item.accordionProps} // Spread custom props
        >
          <AccordionSummary expandIcon={<ExpandMoreIcon />} {...item.summaryProps}>
            <Typography>{item.title}</Typography>
          </AccordionSummary>
          <AccordionDetails {...item.detailsProps}>
            <Typography>{item.content}</Typography>
          </AccordionDetails>
        </Accordion>
      ))}
    </div>
  );
};

export default VDLAccordion;
