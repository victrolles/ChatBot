import React from 'react'
import "./Home.css"
import Sidebar from '../../components/Sidebar'
import Chat from '../../components/Chat'

export const Home = () => {
  return (
    <div className="home">
      <div className="home-container">
        <Sidebar />
        <Chat />
      </div>
    </div>
  )
}
