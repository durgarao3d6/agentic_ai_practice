// import React from "react";
// import ReactMarkdown from "react-markdown";
// import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
// import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
// import type { Components } from "react-markdown";
// import remarkGfm from "remark-gfm";
// import rehypeRaw from "rehype-raw";

// interface MarkdownRendererProps {
//   content: string;
// }

// interface CodeProps extends React.HTMLAttributes<HTMLElement> {
//   inline?: boolean;
//   className?: string;
//   children?: React.ReactNode;
// }

// const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
//   const components: Components = {
//     p: (props) => <div className="markdown-p" {...props} />,
//     ul: (props) => <ul className="markdown-ul" {...props} />,
//     ol: (props) => <ol className="markdown-ol" {...props} />,
//     li: (props) => <li className="markdown-li" {...props} />,
    
//     code: ({ inline, className, children, ...props }: CodeProps) => {
//       const match = /language-(\w+)/.exec(className || "");
      
//       if (!inline && match) {
//         return (
//           <SyntaxHighlighter 
//             style={atomDark} 
//             language={match[1]} 
//             PreTag="div"
//             wrapLongLines
//             showLineNumbers
//           >
//             {String(children).replace(/\n$/, "")}
//           </SyntaxHighlighter>
//         );
//       }
      
//       return (
//         <code className={className} {...props}>
//           {children}
//         </code>
//       );
//     },

//     a: (props) => (
//       <a {...props} target="_blank" rel="noopener noreferrer" className="markdown-a" />
//     ),
//     img: ({ alt, ...props }) => (
//       <img {...props} alt={alt || ""} className="markdown-img" loading="lazy" />
//     ),
//   };

//   return (
//     <ReactMarkdown
//       components={components}
//       remarkPlugins={[remarkGfm]}
//       rehypePlugins={[rehypeRaw]}
//       skipHtml={false}
//     >
//       {content}
//     </ReactMarkdown>
//   );
// };

// export default MarkdownRenderer;


import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import type { Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

interface MarkdownRendererProps {
  content: string;
  isNested?: boolean;
  nestingLevel?: number;
}

interface CodeProps extends React.HTMLAttributes<HTMLElement> {
  inline?: boolean;
  className?: string;
  children?: React.ReactNode;
}

const MAX_NESTING_LEVEL = 9;

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ 
  content, 
  isNested = false,
  nestingLevel = 0 
}) => {
  const [activeTabs, setActiveTabs] = useState<Record<string, "preview" | "source">>({});

  const toggleTab = (blockId: string) => {
    setActiveTabs(prev => ({
      ...prev,
      [blockId]: prev[blockId] === "preview" ? "source" : "preview"
    }));
  };

  const components = createComponents(nestingLevel);

  function createComponents(currentNestingLevel: number): Components {
    return {
      // Basic markdown elements
      p: (props) => <div className="markdown-p" {...props} />,
      ul: (props) => <ul className="markdown-ul" {...props} />,
      ol: (props) => <ol className="markdown-ol" {...props} />,
      li: (props) => <li className="markdown-li" {...props} />,
      a: (props) => (
        <a {...props} target="_blank" rel="noopener noreferrer" className="markdown-a" />
      ),
      img: ({ alt, ...props }) => (
        <img {...props} alt={alt || ""} className="markdown-img" loading="lazy" />
      ),
      
      // Headings
      h1: (props) => <h1 className="markdown-h1" {...props} />,
      h2: (props) => <h2 className="markdown-h2" {...props} />,
      h3: (props) => <h3 className="markdown-h3" {...props} />,
      h4: (props) => <h4 className="markdown-h4" {...props} />,
      h5: (props) => <h5 className="markdown-h5" {...props} />,
      h6: (props) => <h6 className="markdown-h6" {...props} />,
      
      // Other block elements
      blockquote: (props) => <blockquote className="markdown-blockquote" {...props} />,
      hr: (props) => <hr className="markdown-hr" {...props} />,
      table: (props) => <table className="markdown-table" {...props} />,
      thead: (props) => <thead {...props} />,
      tbody: (props) => <tbody {...props} />,
      tr: (props) => <tr {...props} />,
      th: (props) => <th {...props} />,
      td: (props) => <td {...props} />,

      // Special code block handling with recursive rendering
      code: ({ inline, className, children, ...props }: CodeProps) => {
        if (inline) {
          return <code className={className} {...props}>{children}</code>;
        }

        const match = /language-(\w+)/.exec(className || "");
        const language = match?.[1] || "text";
        const codeContent = String(children).replace(/\n$/, "");
        const isMarkdownBlock = language.toLowerCase() === "markdown";
        
        // Generate a unique ID for this block
        const blockId = `codeblock-${Math.random().toString(36).slice(2, 9)}`;
        const currentTab = activeTabs[blockId] || (isMarkdownBlock ? "preview" : "source");

        // Handle nested markdown rendering
        if (isMarkdownBlock && currentNestingLevel < MAX_NESTING_LEVEL) {
          return (
            <div className={`nested-markdown level-${currentNestingLevel}`}>
              <div className="tab-buttons">
                <button
                  className={`tab-button ${currentTab === "preview" ? "active" : ""}`}
                  onClick={() => toggleTab(blockId)}
                >
                  Preview
                </button>
                <button
                  className={`tab-button ${currentTab === "source" ? "active" : ""}`}
                  onClick={() => toggleTab(blockId)}
                >
                  Source
                </button>
              </div>
              
              <div className="tab-content">
                {currentTab === "preview" ? (
                  <div className="markdown-preview">
                    <MarkdownRenderer
                      content={codeContent}
                      isNested={true}
                      nestingLevel={currentNestingLevel + 1}
                    />
                  </div>
                ) : (
                  <SyntaxHighlighter
                    style={atomDark}
                    language="markdown"
                    PreTag="div"
                    showLineNumbers
                  >
                    {codeContent}
                  </SyntaxHighlighter>
                )}
              </div>
            </div>
          );
        }

        // Regular code block
        return (
          <SyntaxHighlighter
            style={atomDark}
            language={language}
            PreTag="div"
            showLineNumbers
          >
            {codeContent}
          </SyntaxHighlighter>
        );
      }
    };
  }

  return (
    <div className={`markdown-renderer ${isNested ? "nested" : "root"}`}>
      <ReactMarkdown
        components={components}
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        skipHtml={false}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;