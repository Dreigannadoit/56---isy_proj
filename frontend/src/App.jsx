import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Test from './test/Test'

function App() {
  return (
    <>
      <BrowserRouter >
        <Routes>
          <Route path='/' element={<Test />}/>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
