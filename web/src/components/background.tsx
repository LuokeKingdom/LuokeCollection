import React, { ReactNode, CSSProperties } from 'react';

interface BackgroundImageProps {
  imageUrl: string;
  fallbackColor?: string;
  children?: ReactNode;
}

const BackgroundImage: React.FC<BackgroundImageProps> = ({ imageUrl, fallbackColor = 'grey', children }) => {
  const imageStyle: CSSProperties = {
    backgroundImage: `url(${imageUrl})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    width: '100%',
    height: '100%',
    position: 'absolute',
    top: 0,
    left: 0,
  };

  const fallbackStyle: CSSProperties = {
    backgroundColor: fallbackColor,
    width: '100%',
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
  };

  return (
    <div style={fallbackStyle}>
      <div style={imageStyle} />
      {children}
    </div>
  );
};

export default BackgroundImage;
