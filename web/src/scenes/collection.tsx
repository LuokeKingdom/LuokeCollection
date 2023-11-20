import React from 'react';
import Collection3x3 from '../components/collection3x3';
import Background from '../components/background';
import Position from '../components/position';
import Center from '../components/center';
import Loader from '../components/loading';
import PetIcon from '../components/PetIcon';


const CollectionScene = () => {
    return (
        <Center>
        <Background width='1200px' height='800px' $image_url='training.png' >
        <Position x={130} y={180}>
            <Collection3x3 
                width={450} 
                height={450} 
                items={new Array(9).fill(0).map(x=><PetIcon width={100} height={100} $image_url='display.png'/>)} 
            />
        </Position>
        </Background>
        </Center>
    )
}

export default CollectionScene