import React from 'react';
import styled from 'styled-components';


interface PetIconProps {
    width: number;
    height: number;
    $image_url: string;
}

interface ImageProps {
    $image_url: string;
}

const ImageLayer = styled.div<ImageProps>`
  background-image: url(${props=>props.$image_url});
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
`;

const PetIcon: React.FC<PetIconProps> = ({width, height, $image_url}) => {
    return (
        <div style={{width: width, height: height}}>
            <ImageLayer $image_url={$image_url}/>
        </div>
    )
}


export default PetIcon
