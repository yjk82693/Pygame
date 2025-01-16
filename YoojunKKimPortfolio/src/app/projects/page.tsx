"use client";

import React from 'react';
import ClientLayout from '../components/ClientLayout';
import { Card, Button } from 'antd';

const projects = [
  { 
    name: 'Tetris', 
    description: 'A classic Tetris game built with Pygame, featuring block rotation, line clearing, and increasing difficulty.', 
    githubLink: 'https://github.com/yjk82693/Pygame/blob/main/Tetris/Tetris.py', 
    image: '/images/tetris.jpg' // Add your image path here
  },
  { 
    name: 'Snake Game', 
    description: 'A modern twist on the classic Snake game, where players navigate a growing snake to eat food while avoiding collisions.', 
    githubLink: 'https://github.com/yjk82693/Pygame/tree/main/Snake', 
    image: '/images/snake.jpg' // Add your image path here
  },
  { 
    name: 'Orca\'s Rush', 
    description: 'A Flappy Bird-inspired game with an Orca navigating underwater obstacles while collecting points.', 
    githubLink: 'https://github.com/yjk82693/Pygame/tree/main/OrcasRush', 
    image: '/images/orca.jpg' // Add your image path here
  },
];

const ProjectsPage = () => {
  return (
    <ClientLayout>
      <div style={{ padding: '20px' }}>
        <h1 style={{ fontSize: '36px', textAlign: 'center', marginBottom: '40px' }}>My Projects</h1>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
          {projects.map((project, index) => (
            <Card 
              key={index} 
              style={{
                width: 300, 
                display: 'flex', 
                flexDirection: 'column', 
                justifyContent: 'space-between',
                textAlign: 'center',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                borderRadius: '8px',
              }}
            >
              {/* Game Screenshot */}
              <img 
                src={project.image} 
                alt={project.name} 
                style={{ width: '100%', height: '150px', objectFit: 'cover', marginBottom: '15px', borderRadius: '8px 8px 0 0' }} 
              />
              <div style={{ padding: '10px' }}>
                <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px' }}>{project.name}</h2>
                <p style={{ fontSize: '16px', lineHeight: '1.6', color: '#555', marginBottom: '20px' }}>{project.description}</p>
              </div>
              <Button
                type="primary"
                href={project.githubLink}
                target="_blank"
                rel="noopener noreferrer"
                style={{ alignSelf: 'center', marginBottom: '10px' }}
              >
                View on GitHub
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </ClientLayout>
  );
};

export default ProjectsPage;
