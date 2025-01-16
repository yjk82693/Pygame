"use client";

import { Typography } from 'antd';
import ClientLayout from '../../components/ClientLayout'; // Adjust the relative path as needed

const { Title, Paragraph } = Typography;

const Phase2 = () => {
  return (
    <ClientLayout>
      <div
        style={{
          padding: '40px',
          maxWidth: '1000px',
          margin: '0 auto',
          textAlign: 'left',
          border: '2px solid #001529', // Add border
          borderRadius: '10px', // Rounded corners
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)', // Add subtle shadow
        }}
      >
        {/* Image at the top */}
        <img
          src="/images/phase2.jpg" // Add your image path here
          alt="Phase 2: High School Life"
          style={{
            width: '100%', // Stretch to fit the container width
            height: 'auto', // Maintain the aspect ratio
            maxWidth: '100%', // Prevent exceeding the original dimensions
            marginBottom: '20px',
            borderRadius: '8px', // Round corners of the image
            border: '1px solid #ccc', // Thin border around the image
          }}
        />

        {/* Title and content */}
        <div style={{ padding: '0 20px' }}>
        <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
          Even after returning to Korea, my desire to explore new cultures only intensified. This yearning led me to take a bold step and enroll in an international school in Singapore—UWCSEA—hoping to immerse myself in a fresh and diverse environment. However, my journey did not unfold as smoothly as I had envisioned. Starting directly in Grade 10, I skipped Grade 9 due to the academic differences between Korea and Singapore, which left me little time to adapt to the rigorous International Baccalaureate (IB) curriculum. I soon found myself struggling in an unfamiliar setting, feeling isolated and homesick as I navigated life in a dormitory far from family and friends. The cultural and language barriers felt overwhelming, and I couldn't help but feel it was unfair to compete academically with native English speakers. Envying the ease with which they communicated, I grew frustrated, often questioning my decision and longing for the familiar comfort of home.
        </Paragraph>

        <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
          Watching my grade report was a wake-up call that struck me deeply. The realization that friends who once had similar or even lower grades were now excelling far beyond me was hard to accept. Seeing the stark difference between their achievements and my own filled me with a desire to change. I knew I couldn’t continue in the same way if I wanted to grow. This experience made me confront my own shortcomings and motivated me to push beyond my comfort zone. With this new determination, I began seeking ways to improve. I had many discussions with my parents, who encouraged me to focus on self-discovery rather than dwelling on comparisons. I gradually came to understand that my setbacks were an opportunity to redefine my path and grow stronger.
        </Paragraph>

        <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
          Embracing this mindset shift, I started paying more attention to what I genuinely enjoyed, like storytelling. I experimented with writing fan-fiction, which gathered an unexpectedly positive response online and even reached over a million views. This creative outlet was one of the few things that brought me joy during that period, and it reminded me of the passion I had for creating stories that could resonate with others.
        </Paragraph>

        <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
          During this period, I watched Frozen 2, which brought back memories of my time in America and the joy Disney films had brought me as a child. I realized that my dream was to create animated films that could inspire and bring happiness to people of all ages, just as Disney had done for me. Specifically, I wanted to craft stories like those of Disney or Studio Ghibli—narratives that touch the hearts of both children and adults alike. However, knowing that science-based majors would be advantageous for admission to U.S. universities, I decided to pursue a field that was both close to animation and grounded in science: computer science. This way, I could still work towards my dream while building a strong academic foundation.
        </Paragraph>
        </div>
      </div>
    </ClientLayout>
  );
};

export default Phase2;
