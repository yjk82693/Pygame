"use client";

import { Row, Col, Input, Button } from 'antd';
import ClientLayout from './components/ClientLayout';
import Image from 'next/image'; // Using Next.js Image optimization

const HomePage = () => (
  <ClientLayout>
    <div style={{ padding: '60px 20px', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Two Column Layout */}
      <Row gutter={32} align="middle">
        {/* Left Column: Introduction */}
        <Col xs={24} md={14}>
          <h1 style={{ fontSize: '48px', fontWeight: 'bold' }}>
            Hello, I’m Yoojun Kim.
          </h1>
          <p style={{ fontSize: '24px', lineHeight: '1.5' }}>
            Inspired by the creativity of Disney and Nintendo, I pursued computer science to develop innovative technologies. My focus is on using AI to make creativity more accessible, empowering people to bring their stories and ideas to life.
          </p>

          {/* Contact Form */}
          <div style={{ marginTop: '20px' }}>
            <Row gutter={8}>
              <Col xs={24} sm={12}>
                <Input placeholder="Your Name" />
              </Col>
              <Col xs={24} sm={12}>
                <Input placeholder="Your Email Address" />
              </Col>
              <Col xs={24} sm={24} style={{ marginTop: '10px' }}>
                <Button type="primary" block>
                  Submit
                </Button>
              </Col>
            </Row>
          </div>
        </Col>

        {/* Right Column: Profile Image */}
        <Col xs={24} md={10}>
          <Image
            src="/images/logo.png" // Updated image path
            alt="Yoojun Kim"
            width={400}         // Adjust the width as needed
            height={400}        // Adjust the height as needed
            style={{ borderRadius: '50%', objectFit: 'cover' }} // Circular image styling
          />
        </Col>
      </Row>
    </div>
  </ClientLayout>
);

export default HomePage;
