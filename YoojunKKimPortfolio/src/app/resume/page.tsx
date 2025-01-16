"use client";

import { Typography } from 'antd';
import ClientLayout from '../components/ClientLayout'; // Ensure correct path to your layout component

const { Title } = Typography;

const Resume = () => {
  return (
    <ClientLayout>
      <div style={{ padding: '40px', textAlign: 'center', maxWidth: '1200px', margin: '0 auto' }}>
        {/* Large Font Label */}
        <Title level={2}>Here's my resume:</Title>

        {/* Enlarge Online Preview */}
        <div style={{ marginTop: '40px' }}>
          <iframe
            src="/resume/Resume.pdf" // Correct path to the PDF
            width="100%"
            height="1000px" // Increased height for larger display
            style={{ border: 'none' }}
            title="Resume"
          />
        </div>
      </div>
    </ClientLayout>
  );
};

export default Resume;
