"use client";

import { Typography } from 'antd';
import ClientLayout from '../../components/ClientLayout'; // Adjust the relative path as needed

const { Title, Paragraph } = Typography;

const Phase4 = () => {
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
          src="/images/phase4.jpg" // Add your image path here
          alt="Phase 4: Army Experience"
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
          <Title level={1} style={{ fontSize: '36px', marginBottom: '20px' }}>
            Phase 4: Army Experience
          </Title>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            My time in the army was a challenging period, both physically and mentally. The structured environment was unlike anything I had experienced before; there was little freedom to pursue my interests, go out as I pleased, or study what I wanted. Initially, this lack of control felt stifling, and the demanding routines left me exhausted. However, amid these difficulties, I discovered an invaluable lesson in time management. With my free time so limited, I learned to make the most of each moment, using any opportunity to focus on my goals and passions. I began carrying a notebook with me, jotting down ideas whenever I could, capturing thoughts that would later fuel my ambitions. Over time, I developed ten Game Design Documents (GDDs) and drafted outlines for animation scripts, laying the foundation for future projects.
          </Paragraph>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            Despite the restrictions, I was determined not to lose touch with my interest in computer science. I continued to study whenever I could, diving deeper into the field I loved. One area that particularly captured my attention was artificial intelligence. The army environment, while limiting in some ways, provided me the space to reflect on the potential of AI and its role in shaping the future of technology. Through books, articles, and online resources, I explored how AI was transforming industries, especially gaming and animation—fields close to my heart. I became increasingly intrigued by the possibilities AI offered, imagining ways it could be integrated into my own projects to enhance creativity and streamline processes.
          </Paragraph>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            As my understanding of AI deepened, so did my excitement about its potential to revolutionize the creative world. I realized that AI could democratize access to game and animation development, making these fields more approachable for creators who may lack traditional technical expertise. This idea resonated deeply with me, as I had always dreamed of building imaginative worlds and telling stories but often felt constrained by limited resources. AI, I discovered, had the power to bridge that gap, enabling people like me—and countless others—to bring their ideas to life more easily. The thought of using AI to remove barriers and empower other creators was inspiring, and it motivated me to think beyond my own projects.
          </Paragraph>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            Looking to the future, I am driven by the goal of developing AI tools specifically tailored for creative industries. My time in the army taught me resilience, discipline, and the importance of maximizing limited resources—all qualities that I believe will help me in this mission. By creating AI-driven tools that support artists, writers, and designers, I hope to make it easier for anyone with a dream to bring their imagination into reality. This path not only aligns with my personal ambitions but also fulfills a greater purpose: empowering others to tell their stories and share their unique visions with the world.
          </Paragraph>
        </div>
      </div>
    </ClientLayout>
  );
};

export default Phase4;
