// import React from "react";
// import ReactMarkdown from "react-markdown";
// import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
// import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
// import { Components } from "react-markdown/lib/ast-to-react";

// interface MarkdownRendererProps {
//   content: string;
// }

// const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
//   const components: Components = {
//     code({ node, inline, className, children, ...props }) {
//       const match = /language-(\w+)/.exec(className ?? "");
//       if (!inline && match) {
//         return (
//           <SyntaxHighlighter style={atomDark} language={match[1]} PreTag="div">
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
//   };

//   return <ReactMarkdown components={components}>{content}</ReactMarkdown>;
// };

// export default MarkdownRenderer;
