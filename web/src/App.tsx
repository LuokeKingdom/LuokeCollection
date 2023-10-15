import React from 'react';
import './App.css';
import SplitBox from './components/split_box';
import Collection3x3 from './components/collection3x3';
import Square from './components/square';
import Background from './components/background';

function App() {
  return (
    <div className='App'>
    <Background width='1200px' height='800px' $image_url='training.png' >
      <SplitBox 
        left={<Collection3x3 items={new Array(9).fill(0).map(x=><Square />)} />} 
        right={<Collection3x3 items={new Array(9).fill(0).map(x=><Square />)} start_key={9} />} 
      />
    </Background>
    </div>
  );
}

export default App;
