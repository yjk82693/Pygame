"use client";

import { Typography } from 'antd';
import ClientLayout from '../../components/ClientLayout'; // Adjust the relative path as needed

const { Title, Paragraph } = Typography;

const Phase1 = () => {
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
          src="/images/phase1.jpg" // Add your image path here
          alt="Phase 1: Elementary Years"
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
            Phase 1: Elementary Years
          </Title>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            Growing up, I was like the proverbial frog in the well, believing my small neighborhood in Seoul was the whole world. My life was confined to familiar streets and familiar faces, and I never thought much beyond them. This changed when, unexpectedly, my parents told me that I would be going to the United States—not with them, but alone, to experience a new culture. I found myself in North Carolina for three months, living with a host family and trying to navigate a world where I barely understood the language. Adapting to this new environment was not easy. The unfamiliar language and customs were overwhelming, but over time, through my homestay experience, I gradually became more accustomed to American culture. The initial feelings of loneliness and negativity began to fade, replaced by a budding sense of curiosity and resilience. Despite this, I returned to Korea with lingering doubts, wondering, "Do I really have to do this again?"
          </Paragraph>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            The following year, my family and I moved together to Williamsburg, Virginia, for a longer stay. This time, with my family by my side, I found it easier to embrace the changes. Together, we traveled around North America, and each journey brought new sights and experiences that continued to expand my worldview. The vastness and beauty of North America left a lasting impression on me, transforming my initial reluctance into a genuine appreciation. I realized how much more there was to see beyond the narrow scope of my previous life. As I discovered more of this fascinating world, I found myself longing to uncover new places and perspectives, becoming captivated by the idea of constantly seeking out the unknown.
          </Paragraph>

          <Paragraph style={{ fontSize: '18px', lineHeight: '1.8', textAlign: 'justify' }}>
            Even after returning to Korea, this fascination with exploring didn’t fade. In fact, my desire to experience new cultures and environments only grew stronger. This led me to seek out another adventure, choosing to attend an international school in Singapore. I wanted to immerse myself in yet another culture that was both fresh and different from anything I’d known. My time in Singapore exposed me to a rich tapestry of people and ideas, each experience further broadening my understanding and helping me develop a more global perspective.
          </Paragraph>
        </div>
      </div>
    </ClientLayout>
  );
};

export default Phase1;
